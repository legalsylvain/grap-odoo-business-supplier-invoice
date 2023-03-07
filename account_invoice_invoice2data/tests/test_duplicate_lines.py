# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64

from .test_module import TestModule


class TestDuplicatesLines(TestModule):
    def setUp(self):
        super().setUp()
        self.AccountInvoice = self.env["account.invoice"]
        self.Wizard = self.env["wizard.invoice2data.import"]
        self.invoice_teddy_beer = self.env.ref(
            "account_invoice_invoice2data.invoice_teddy_beer"
        )
        # Prepare binary data
        self.invoice_name = "brasserie-teddy-beer__2222-12-01__FA2212-3445.pdf"
        invoice_file = open(str(self._get_invoice_path(self.invoice_name)), "rb")
        self.base64_data = base64.b64encode(invoice_file.read())

    def test_duplicate_lines(self):

        self.assertEqual(len(self.invoice_teddy_beer.invoice_line_ids), 2)

        # #######################
        # Part 1 : Import Invoice (1/2)
        # #######################
        wizard = self.Wizard.create(
            {
                "invoice_file": self.base64_data,
                "invoice_filename": self.invoice_name,
                # "partner_id": self.partner_relais_vert.id,
                "invoice_id": self.invoice_teddy_beer.id,
            }
        )
        self.assertEqual(wizard.state, "import")

        wizard.import_invoice()

        self.assertEqual(wizard.state, "line_differences")
        self.assertEqual(len(wizard.line_ids.filtered(lambda x: x.invoice_line_id)), 2)
        self.assertEqual(len(wizard.line_ids), 4)

        # ######################
        # Part 2 : Apply Changes (1/2)
        # ######################

        wizard.apply_changes()

        # Check Impact on invoice lines
        self.assertEqual(len(self.invoice_teddy_beer.invoice_line_ids), 4)

        # #######################
        # Part 3 : Import Invoice (2/2)
        # #######################
        wizard = self.Wizard.create(
            {
                "invoice_file": self.base64_data,
                "invoice_filename": self.invoice_name,
                "invoice_id": self.invoice_teddy_beer.id,
            }
        )
        self.assertEqual(wizard.state, "import")

        wizard.import_invoice()

        self.assertEqual(wizard.state, "line_differences")
        self.assertEqual(len(wizard.line_ids.filtered(lambda x: x.invoice_line_id)), 4)
        self.assertEqual(len(wizard.line_ids), 4)

        # ######################
        # Part 4 : Apply Changes (2/2)
        # ######################

        wizard.apply_changes()
