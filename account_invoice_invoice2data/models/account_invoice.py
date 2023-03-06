# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    invoice2data_situation = fields.Selection(
        compute="_compute_invoice2data_info",
        selection=[
            ("undefined", "Undefined"),
            ("available", "Available"),
            ("not_found", "Not Found"),
            ("no_vat", "Vat Number Not Set"),
        ],
    )

    invoice2data_message = fields.Text(
        compute="_compute_invoice2data_info",
    )

    @api.depends("partner_id.vat", "state")
    def _compute_invoice2data_info(self):
        for invoice in self.filtered(lambda x: x.state == "draft"):
            current_vat = (invoice.partner_id.vat or "").replace(" ", "")
            if current_vat:
                template = self.env["account.invoice2data.template"].search(
                    [("vat", "=", current_vat)]
                )
                if template:
                    invoice.invoice2data_situation = "available"
                    invoice.invoice2data_message = (
                        _(
                            "The supplier's electronic invoice analysis"
                            " is available to Supplier %s."
                        )
                        % template.name
                    )
                else:
                    invoice.invoice2data_situation = "not_found"
                    # For the time being, do not display anything
            else:
                invoice.invoice2data_situation = "no_vat"
                invoice.invoice2data_message = _(
                    "Please enter your supplier's VAT number,"
                    " to see if the supplier's electronic invoice"
                    " analysis is available."
                )

        for invoice in self.filtered(lambda x: x.state != "draft"):
            invoice.invoice2data_situation = "undefined"
            invoice.invoice2data_message = False
