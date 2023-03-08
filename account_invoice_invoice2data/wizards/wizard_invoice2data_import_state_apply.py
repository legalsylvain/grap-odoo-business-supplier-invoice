# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, models
from odoo.tools.float_utils import float_compare
from odoo.tools.misc import formatLang


class WizardInvoice2dataImportStateApply(models.TransientModel):
    _inherit = "wizard.invoice2data.import"

    def apply_changes(self):
        self.ensure_one()
        self._check_invoice_state()
        self._apply_write_invoice()
        self._apply_attach_file()
        self._check_totals()

    def _check_totals(self):
        self.ensure_one()
        if float_compare(
            self.pdf_amount_untaxed,
            self.invoice_id.amount_untaxed,
            precision_digits=self.currency_id.decimal_places,
        ):
            difference = abs(self.pdf_amount_untaxed - self.invoice_id.amount_untaxed)
            if difference < 0.10:
                self.env.user.notify_warning(
                    _(
                        "The total amount untaxed is a bit different from the PDF amount.\n\n"
                        " Diferrences : (%s)"
                        % formatLang(
                            self.env, difference, currency_obj=self.currency_id
                        )
                    ),
                    sticky=True,
                )
            else:
                self.env.user.notify_danger(
                    _(
                        "The total amount untaxed is different from the PDF amount.\n\n"
                        " Diferrences : (%s)"
                        % formatLang(
                            self.env, difference, currency_obj=self.currency_id
                        )
                    ),
                    sticky=True,
                )

    def _apply_write_invoice(self):
        lines_vals = self.line_ids._prepare_invoice_lines_vals()

        sequence = len(lines_vals)
        for line in self.to_delete_invoice_line_ids:
            sequence += 1
            line_vals = {
                "sequence": sequence,
                "price_unit": 0,
                "name": _(
                    "%s\n"
                    "[PDF analysis] Unit Price %s set to 0,"
                    " because the line is not present in the PDF."
                )
                % (line.name, line.quantity),
            }
            lines_vals.append((1, line.id, line_vals))

        invoice_vals = {
            "date_invoice": self.pdf_date,
            "reference": self.pdf_invoice_number,
            "invoice_line_ids": lines_vals,
        }

        if self.pdf_date_due:
            invoice_vals.update({"date_due": self.pdf_date_due})

        self.invoice_id.write(invoice_vals)

        self.invoice_id.button_reset_tax_line_ids()

    def _apply_attach_file(self):
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
            self.env["ir.attachment"].create(
                {
                    "name": self.invoice_filename,
                    "datas": self.invoice_file,
                    "datas_fname": self.invoice_filename,
                    "res_model": "account.invoice",
                    "res_id": self.invoice_id.id,
                }
            )
            self.env.user.notify_info(
                _("The PDF file %s has been attached to the current invoice.")
                % self.invoice_filename
            )
