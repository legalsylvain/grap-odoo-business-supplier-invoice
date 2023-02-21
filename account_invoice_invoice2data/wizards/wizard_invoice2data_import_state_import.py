# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# Part of the code comes from
# OCA/edi/account_invoice_import_invoice2data Module.
# Copyright 2015 - Today Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import mimetypes
import os
import tempfile

import invoice2data

from odoo import _, models, tools
from odoo.exceptions import UserError


class WizardInvoice2dataImportStateImport(models.TransientModel):
    _inherit = "wizard.invoice2data.import"

    def import_invoice(self):
        self.ensure_one()
        result = self._extract_json_from_pdf()
        self._initialize_wizard_invoice(result)
        self._initialize_wizard_lines(result)
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

        # Write data in a temporary file
        fd, tmp_file_name = tempfile.mkstemp()
        try:
            os.write(fd, file_data)
        finally:
            os.close(fd)

        try:
            result = invoice2data.main.extract_data(tmp_file_name, templates=templates)
        except Exception as e:
            raise UserError(_("PDF Invoice parsing failed. Error message: %s") % e)
        if not result:
            raise UserError(_("This PDF invoice doesn't match a known templates"))

        return result

    def _initialize_wizard_invoice(self, result):
        for invoice_field in [
            "amount_untaxed",
            "amount",
            "invoice_number",
            "date",
            "date_due",
        ]:
            if invoice_field in result:
                value = result[invoice_field]
                if "date" in invoice_field:
                    value = value.date()
                setattr(self, "pdf_%s" % invoice_field, value)

    def _initialize_wizard_lines(self, pdf_data):
        self.line_ids.unlink()
        WizardLine = self.env["wizard.invoice2data.import.line"]
        WizardLine.create(WizardLine._prepare_from_pdf_data(self, pdf_data))
