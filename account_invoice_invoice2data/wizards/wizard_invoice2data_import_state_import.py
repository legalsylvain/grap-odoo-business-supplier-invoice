# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# Part of the code comes from
# OCA/edi/account_invoice_import_invoice2data Module.
# Copyright 2015 - Today Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import logging
import mimetypes
import os
import tempfile

import invoice2data

from odoo import _, models, tools
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare
from odoo.tools.misc import formatLang

_logger = logging.getLogger(__name__)


class WizardInvoice2dataImportStateImport(models.TransientModel):
    _inherit = "wizard.invoice2data.import"

    def import_invoice(self):
        self.ensure_one()
        result = self._extract_json_from_pdf()
        if not result:
            return self._get_action_from_state("import_failed")
        self._initialize_wizard_invoice(result)
        self._initialize_wizard_lines(result)
        self._check_import_correct()
        self._update_supplier()

        # We try to save a step, if all the products are mapped
        return self.map_products()

    def _extract_json_from_pdf(self):
        self.ensure_one()

        # Load Templates
        local_templates_dir = tools.config.get("invoice2data_templates_dir", False)

        if not local_templates_dir:
            raise UserError(
                _("'invoice2data_templates_dir' not set in the odoo Config File")
            )
        if not os.path.isdir(local_templates_dir):
            raise UserError(_("%s not available.") % str(local_templates_dir))
        templates = invoice2data.extract.loader.read_templates(local_templates_dir)
        if not len(templates):
            raise UserError(_("No Template found to for bill invoices analyze."))

        # Get data, and check filetype
        file_data = base64.b64decode(self.invoice_file)
        filetype = mimetypes.guess_type(self.invoice_filename)
        if not filetype or filetype[0] != "application/pdf":
            raise UserError(_("Unimplemented file type : '%s'") % str(filetype))

        # Attach the file if not yet attached
        attachments = self.env["ir.attachment"].search(
            [
                ("res_model", "=", "account.invoice"),
                ("res_id", "=", self.invoice_id.id),
            ]
        )
        if not any(
            [attachment.datas == self.invoice_file for attachment in attachments]
        ):
            _logger.info(
                "Attach PDF '%s' to the account invoice #%d"
                % (self.invoice_filename, self.invoice_id.id)
            )
            self.env["ir.attachment"].create(
                {
                    "name": self.invoice_filename,
                    "datas": self.invoice_file,
                    "datas_fname": self.invoice_filename,
                    "res_model": "account.invoice",
                    "res_id": self.invoice_id.id,
                }
            )

        # Write data in a temporary file
        fd, tmp_file_name = tempfile.mkstemp()
        try:
            os.write(fd, file_data)
        finally:
            os.close(fd)

        result = invoice2data.main.extract_data(tmp_file_name, templates=templates)

        return result

    def _initialize_wizard_invoice(self, result):
        for invoice_field in [
            "issuer",
            "amount_untaxed",
            "amount",
            "invoice_number",
            "date",
            "date_due",
            "vat",
        ]:
            if invoice_field in result:
                value = result[invoice_field]
                if "date" in invoice_field:
                    value = value.date()
                setattr(self, "pdf_%s" % invoice_field, value)

    def _initialize_wizard_lines(self, pdf_data):
        self.line_ids.unlink()
        WizardLine = self.env["wizard.invoice2data.import.line"]
        self.pdf_has_vat_mapping = any(
            [key.startswith("vat_code_") for key in pdf_data.keys()]
        )
        WizardLine.create(WizardLine._prepare_from_pdf_data(self, pdf_data))

    def _update_supplier(self):
        self.ensure_one()
        if self.pdf_vat and not self.partner_id.vat:
            self.partner_id.vat = self.pdf_vat

    def _check_import_correct(self):
        self.ensure_one()
        if float_compare(
            sum(self.line_ids.mapped("pdf_price_subtotal")),
            self.pdf_amount_untaxed,
            precision_digits=self.currency_id.decimal_places,
        ):
            raise UserError(
                _(
                    "The analysis of the PDF file for the supplier %s"
                    " did not go completely well.\n"
                    "- The amount of the analyzed lines is %s,"
                    " but the total amount before tax is %s."
                    " (Missing Amount : %s)\n"
                    " - The analysis found %d lines.\n\n"
                    " Please send the pdf to the IT department for correction.\n\n"
                    "At this time, you will need to manually verify the supplier invoice."
                )
                % (
                    self.pdf_issuer,
                    formatLang(
                        self.env,
                        sum(self.line_ids.mapped("pdf_price_subtotal")),
                        currency_obj=self.currency_id,
                    ),
                    formatLang(
                        self.env, self.pdf_amount_untaxed, currency_obj=self.currency_id
                    ),
                    formatLang(
                        self.env,
                        self.pdf_amount_untaxed
                        - sum(self.line_ids.mapped("pdf_price_subtotal")),
                        currency_obj=self.currency_id,
                    ),
                    len(self.line_ids),
                )
            )
