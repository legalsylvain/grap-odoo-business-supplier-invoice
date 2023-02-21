# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, models


class WizardInvoice2dataImportStateApply(models.TransientModel):
    _inherit = "wizard.invoice2data.import"

    def apply_changes(self):
        self.ensure_one()
        lines_vals = [x._prepare_invoice_line_vals() for x in self.line_ids]

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

        vals = {
            "invoice_line_ids": lines_vals,
        }
        if self.pdf_date:
            vals.update(
                {
                    "date_invoice": self.pdf_date,
                }
            )
        if self.pdf_date_due:
            vals.update(
                {
                    "date_due": self.pdf_date_due,
                }
            )
        if self.pdf_invoice_number:
            vals.update(
                {
                    "reference": self.pdf_invoice_number,
                }
            )

        self.invoice_id.write(vals)
