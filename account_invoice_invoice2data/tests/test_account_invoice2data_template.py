# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from pathlib import Path

from .test_module import TestModule


class TestAccountInvoice2dataTemplate(TestModule):
    def setUp(self):
        super().setUp()
        self.Invoice2dataTemplate = self.env["account.invoice2data.template"]

        self.invoice_relais_vert = self.env.ref(
            "account_invoice_invoice2data.invoice_relais_vert"
        )
        self.partner_relais_vert = self.env.ref(
            "account_invoice_invoice2data.partner_relais_vert"
        )

    def test_init_model(self):
        self.Invoice2dataTemplate.search([]).unlink()
        self.assertEqual(len(self.Invoice2dataTemplate.search([])), 0)

        # Check that init model generate account.invoice2data.template items
        self.Invoice2dataTemplate.init()
        self.assertTrue(len(self.Invoice2dataTemplate.search([])) > 2)

        # Check that removing template files delete invoice2data.template items
        comptoir_des_lys_path = Path(self.local_templates_dir) / "comptoir_des_lys.yml"

        self.Invoice2dataTemplate._update_templates([comptoir_des_lys_path])
        templates = self.Invoice2dataTemplate.search([])
        self.assertTrue(len(templates) == 1)
        self.assertEqual(templates[0].vat, "FR67480737030")

        # Check itemPotens
        self.Invoice2dataTemplate.init()
        self.assertTrue(len(self.Invoice2dataTemplate.search([])) > 2)

        #  Check computation of 'invoice2data_state' field
        self.partner_relais_vert.vat = False
        self.assertEqual(self.invoice_relais_vert.invoice2data_state, "no_vat")

        self.partner_relais_vert.vat = "FR72352867493"
        self.assertEqual(self.invoice_relais_vert.invoice2data_state, "available")

        self.partner_relais_vert.vat = "XX123456789"
        self.assertEqual(self.invoice_relais_vert.invoice2data_state, "not_found")

        self.invoice_relais_vert.action_invoice_open()
        self.assertEqual(self.invoice_relais_vert.invoice2data_state, "not_applicable")
