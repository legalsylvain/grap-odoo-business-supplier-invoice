# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# Part of the code comes from
# OCA/edi/account_invoice_import_invoice2data Module.
# Copyright 2015 - Today Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import jaro

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare
from odoo.tools.misc import formatLang


class WizardInvoice2dataImport(models.TransientModel):
    _name = "wizard.invoice2data.import"
    _description = "Wizard to import Bill invoices via invoice2data"

    _JARO_DIFFERENCE_THRESHOLD = 0.9
    _MAX_AMOUNT_UNTAXED_DIFFERENCE = 0.10

    invoice_file = fields.Binary(string="PDF Invoice", required=True)

    invoice_filename = fields.Char(string="Filename", readonly=True)

    state = fields.Selection(
        selection=[
            ("import", "Import"),
            ("import_failed", "Import Failed"),
            ("product_mapping", "Products Mapping"),
            ("line_differences", "Invoice Lines Differences"),
        ],
        default="import",
        required=True,
        readonly=True,
    )

    invoice_id = fields.Many2one(
        comodel_name="account.invoice",
        string="Supplier Invoice",
        required=True,
        readonly=True,
        ondelete="cascade",
    )

    partner_id = fields.Many2one(
        string="Supplier",
        comodel_name="res.partner",
        related="invoice_id.partner_id",
        readonly=True,
    )

    partner_vat = fields.Char(
        string="Supplier Vat Number", related="partner_id.vat", readonly=False
    )

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="invoice_id.currency_id",
        readonly=True,
    )

    invoice_amount_untaxed = fields.Monetary(
        currency_field="currency_id", related="invoice_id.amount_untaxed", readonly=True
    )

    invoice_amount = fields.Monetary(
        string="Amount Vat Incl",
        currency_field="currency_id",
        related="invoice_id.amount_total",
        readonly=True,
    )

    pdf_amount = fields.Monetary(currency_field="currency_id", readonly=True)

    line_ids = fields.One2many(
        comodel_name="wizard.invoice2data.import.line", inverse_name="wizard_id"
    )

    product_mapping_line_ids = fields.One2many(
        comodel_name="wizard.invoice2data.import.line",
        inverse_name="wizard_id",
        string="Product Mapping",
        domain=[("is_product_mapped", "=", False)],
    )

    invoice_difference_line_qty = fields.Integer(
        compute="_compute_invoice_difference_line_qty",
    )

    invoice_difference_line_ids = fields.One2many(
        comodel_name="wizard.invoice2data.import.line",
        inverse_name="wizard_id",
        string="Invoice Lines Differences",
        domain=[("changes_type", "!=", "no")],
    )

    not_found_invoice_line_ids = fields.Many2many(
        comodel_name="account.invoice.line",
        string="Invoice Lines not found",
        related="to_delete_invoice_line_ids",
        store=False,
        readonly=True,
    )

    to_delete_invoice_line_qty = fields.Integer(
        compute="_compute_to_delete_invoice_line_qty"
    )

    to_delete_invoice_line_ids = fields.Many2many(
        comodel_name="account.invoice.line",
        string="Invoice Lines to delete",
        readonly=True,
    )

    pdf_invoice_number = fields.Char(readonly=True)

    pdf_issuer = fields.Char(readonly=True)

    pdf_vat = fields.Char(readonly=True)

    supplier_name_different = fields.Boolean(compute="_compute_supplier_name_different")

    pdf_amount_untaxed = fields.Monetary(currency_field="currency_id", readonly=True)

    pdf_amount = fields.Monetary(currency_field="currency_id", readonly=True)

    pdf_date = fields.Date(readonly=True)

    pdf_date_due = fields.Date(readonly=True)

    pdf_has_product_code = fields.Boolean(compute="_compute_pdf_has_product_code")

    pdf_has_discount = fields.Boolean(compute="_compute_pdf_has_discount")

    pdf_has_discount2 = fields.Boolean(compute="_compute_pdf_has_discount2")

    pdf_has_vat_mapping = fields.Boolean(readonly=True)

    has_discount = fields.Boolean(compute="_compute_has_discount")

    has_discount2 = fields.Boolean(compute="_compute_has_discount2")

    amount_untaxed_difference = fields.Monetary(
        compute="_compute_fuzzy_message_amount_untaxed_difference",
        currency_field="currency_id",
    )

    fuzzy_message_amount_untaxed_difference = fields.Text(
        compute="_compute_fuzzy_message_amount_untaxed_difference"
    )

    message_vat_difference = fields.Html(
        compute="_compute_message_vat_difference",
    )

    @api.model
    def create(self, vals):
        wizard = super().create(vals)
        wizard._check_invoice_state()
        return wizard

    def _check_invoice_state(self):
        self.ensure_one()
        if self.invoice_id.state != "draft":
            raise UserError(_("You can not run this wizard on a non draft invoice"))

    @api.depends("line_ids.changes_type")
    def _compute_invoice_difference_line_qty(self):
        for wizard in self:
            wizard.invoice_difference_line_qty = len(wizard.invoice_difference_line_ids)

    @api.depends(
        "pdf_has_vat_mapping",
        "line_ids.pdf_vat_amount",
        "line_ids.product_id.supplier_taxes_id",
    )
    def _compute_message_vat_difference(self):
        for wizard in self.filtered(
            lambda x: x.pdf_has_vat_mapping and x.state != "import"
        ):
            message_list = []
            for line in wizard.line_ids.filtered(
                lambda x: len(x.mapped("product_id.supplier_taxes_id")) == 1
            ):
                if line.pdf_vat_amount != line.product_id.supplier_taxes_id[0].amount:
                    message_list.append(
                        _(
                            "The product %s has a VAT of <b>%s %%</b> at purchase,"
                            " but the supplier set a VAT of <b>%s %%</b>."
                        )
                        % (
                            line.product_id.display_name,
                            line.product_id.supplier_taxes_id[0].amount,
                            line.pdf_vat_amount,
                        )
                    )
            if message_list:
                wizard.message_vat_difference = (
                    "<ul>"
                    + "".join(["<li>" + x + "</li>" for x in message_list])
                    + "</ul>"
                    + _(
                        "<b>Please exit the wizard, change the VAT rate"
                        " for each product by opening each invoice line,"
                        " then relaunch the wizard.</b>"
                    )
                )
            else:
                wizard.message_vat_difference = False

        for wizard in self.filtered(
            lambda x: not x.pdf_has_vat_mapping or x.state == "import"
        ):
            wizard.message_vat_difference = False

    @api.depends("currency_id", "line_ids.pdf_price_subtotal", "pdf_amount_untaxed")
    def _compute_fuzzy_message_amount_untaxed_difference(self):
        for wizard in self:
            total_amount_lines = sum(wizard.line_ids.mapped("pdf_price_subtotal"))
            total_amount_invoice = wizard.pdf_amount_untaxed
            currency = wizard.currency_id
            if not total_amount_lines or not total_amount_invoice:
                wizard.amount_untaxed_difference = 0.0
                wizard.fuzzy_message_amount_untaxed_difference = False
                continue
            if not float_compare(
                total_amount_lines,
                total_amount_invoice,
                precision_digits=currency.decimal_places,
            ):
                wizard.amount_untaxed_difference = 0.0
                wizard.fuzzy_message_amount_untaxed_difference = False
                continue
            wizard.amount_untaxed_difference = total_amount_invoice - total_amount_lines
            wizard.fuzzy_message_amount_untaxed_difference = _(
                "The analysis of the PDF file for the supplier %s"
                " did not go completely well.\n"
                "- The amount of the analyzed lines is %s,"
                " but the total amount before tax is %s."
                " (Missing Amount : %s)\n"
                " - The analysis found %d lines."
            ) % (
                wizard.pdf_issuer,
                formatLang(wizard.env, total_amount_lines, currency_obj=currency),
                formatLang(wizard.env, total_amount_invoice, currency_obj=currency),
                formatLang(
                    wizard.env, wizard.amount_untaxed_difference, currency_obj=currency
                ),
                len(wizard.line_ids),
            )

    @api.depends("pdf_issuer", "partner_id.name", "pdf_vat")
    def _compute_supplier_name_different(self):
        for wizard in self:
            # We only check if the name is different if a vat number
            # is present as a static value, in the template file
            # If not present, it can be a generic template file, used
            # for many suppliers. It's the case in a multicompany context
            # to import sale invoices. (intercompany invoices)
            if wizard.pdf_issuer and wizard.pdf_vat:
                wizard.supplier_name_different = (
                    jaro.jaro_winkler_metric(
                        wizard.pdf_issuer.lower(), wizard.partner_id.name.lower()
                    )
                    < self._JARO_DIFFERENCE_THRESHOLD
                )
            else:
                wizard.supplier_name_different = False

    @api.depends("to_delete_invoice_line_ids")
    def _compute_to_delete_invoice_line_qty(self):
        for wizard in self:
            wizard.to_delete_invoice_line_qty = len(wizard.to_delete_invoice_line_ids)

    @api.depends("line_ids.pdf_product_code")
    def _compute_pdf_has_product_code(self):
        for wizard in self:
            self.pdf_has_product_code = any(wizard.mapped("line_ids.pdf_product_code"))

    @api.depends("line_ids.pdf_discount")
    def _compute_pdf_has_discount(self):
        for wizard in self:
            self.pdf_has_discount = any(wizard.mapped("line_ids.pdf_discount"))

    @api.depends("line_ids.pdf_discount2")
    def _compute_pdf_has_discount2(self):
        for wizard in self:
            self.pdf_has_discount2 = any(wizard.mapped("line_ids.pdf_discount2"))

    @api.depends("invoice_id.invoice_line_ids.discount")
    def _compute_has_discount(self):
        for wizard in self:
            self.has_discount = any(
                wizard.mapped("invoice_id.invoice_line_ids.discount")
            )

    @api.depends("invoice_id.invoice_line_ids.discount2")
    def _compute_has_discount2(self):
        for wizard in self:
            self.has_discount2 = any(
                wizard.mapped("invoice_id.invoice_line_ids.discount2")
            )

    def _get_action_from_state(self, state):
        action = self.env["ir.actions.act_window"].for_xml_id(
            "account_invoice_invoice2data", "action_wizard_invoice2data_import"
        )
        self.state = state
        action["res_id"] = self.id
        return action

    def action_close(self):
        self.ensure_one()
        return
