# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, models


class WizardInvoice2dataImportStateApply(models.TransientModel):
    _inherit = "wizard.invoice2data.import"

    def apply_changes(self):
        self.ensure_one()
        self._check_invoice_state()

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
