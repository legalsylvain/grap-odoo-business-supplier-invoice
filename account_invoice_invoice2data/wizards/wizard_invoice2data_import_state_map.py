# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models


class WizardInvoice2dataImportStateMap(models.TransientModel):
    _inherit = "wizard.invoice2data.import"

    def map_products(self):
        self.line_ids._create_or_update_supplierinfos()
        self._analyze_invoice_lines()
        if not all(self.mapped("line_ids.is_product_mapped")):
            return self._get_action_from_state("product_mapping")
        else:
            return self._get_action_from_state("line_differences")

    def _analyze_invoice_lines(self):
        self.line_ids._analyze_invoice_lines()
        mapped_line_ids = self.mapped("line_ids.invoice_line_id").ids
        self.to_delete_invoice_line_ids = self.mapped(
            "invoice_id.invoice_line_ids"
        ).filtered(lambda x: x.id not in mapped_line_ids and x.quantity != 0)
