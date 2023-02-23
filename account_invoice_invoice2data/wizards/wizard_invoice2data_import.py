# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# Part of the code comes from
# OCA/edi/account_invoice_import_invoice2data Module.
# Copyright 2015 - Today Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class WizardInvoice2dataImport(models.TransientModel):
    _name = "wizard.invoice2data.import"
    _description = "Wizard to import Bill invoices via invoice2data"

    invoice_file = fields.Binary(string="PDF Invoice", required=True)

    invoice_filename = fields.Char(string="Filename", readonly=True)

    state = fields.Selection(
        selection=[
            ("import", "Import"),
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

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="invoice_id.currency_id",
        readonly=True,
    )

    line_ids = fields.One2many(
        comodel_name="wizard.invoice2data.import.line", inverse_name="wizard_id"
    )

    product_mapping_line_ids = fields.One2many(
        comodel_name="wizard.invoice2data.import.line",
        inverse_name="wizard_id",
        string="Product Mapping",
        domain=[("is_product_mapped", "=", False)],
    )

    invoice_difference_line_ids = fields.One2many(
        comodel_name="wizard.invoice2data.import.line",
        inverse_name="wizard_id",
        string="Invoice Lines Differences",
        domain=[("has_changes", "=", True)],
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

    pdf_amount_untaxed = fields.Float(readonly=True)

    pdf_amount = fields.Float(readonly=True)

    pdf_date = fields.Date(readonly=True)

    pdf_date_due = fields.Date(readonly=True)

    pdf_has_discount = fields.Boolean(compute="_compute_pdf_has_discount")

    has_discount = fields.Boolean(compute="_compute_has_discount")

    @api.depends("to_delete_invoice_line_ids")
    def _compute_to_delete_invoice_line_qty(self):
        for wizard in self:
            wizard.to_delete_invoice_line_qty = len(wizard.to_delete_invoice_line_ids)

    @api.depends("line_ids.pdf_discount")
    def _compute_pdf_has_discount(self):
        for wizard in self:
            self.pdf_has_discount = any(wizard.mapped("line_ids.pdf_discount"))

    @api.depends("invoice_id.invoice_line_ids.discount")
    def _compute_has_discount(self):
        for wizard in self:
            self.has_discount = any(
                wizard.mapped("invoice_id.invoice_line_ids.discount")
            )

    def _get_action_from_state(self, state):
        action = self.env["ir.actions.act_window"].for_xml_id(
            "account_invoice_invoice2data", "action_wizard_invoice2data_import"
        )
        self.state = state
        action["res_id"] = self.id
        return action
