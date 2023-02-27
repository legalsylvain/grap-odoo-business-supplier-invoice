# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64

from odoo import tools

from odoo.addons.account_invoice_invoice2data_templates.tests.test import TestModule


class TestFullWorkflow(TestModule):
    def setUp(self):
        super().setUp()
        self.AccountInvoice = self.env["account.invoice"]
        self.Wizard = self.env["wizard.invoice2data.import"]
        self.invoice_relais_vert = self.env.ref(
            "account_invoice_invoice2data_test.invoice_relais_vert"
        )
        self.partner_relais_vert = self.env.ref(
            "account_invoice_invoice2data.partner_relais_vert"
        )

        tools.config["invoice2data_templates_dir"] = self.local_templates_dir

        # Prepare binary data
        self.invoice_name = "unknown-supplier.pdf"
        invoice_file = open(str(self._get_invoice_path(self.invoice_name)), "rb")
        self.base64_data = base64.b64encode(invoice_file.read())

    def _get_attachments(self, invoice):
        return self.env["ir.attachment"].search(
            [("res_model", "=", "account.invoice"), ("res_id", "=", invoice.id)]
        )

    def test_bad_invoice(self):
        # unlink previous attachment to make the test idempotens
        self._get_attachments(self.invoice_relais_vert).unlink()

        # #######################
        # Part 1 : Import Invoice
        # #######################
        wizard = self.Wizard.create(
            {
                "invoice_file": self.base64_data,
                "invoice_filename": self.invoice_name,
                "partner_id": self.partner_relais_vert.id,
                "invoice_id": self.invoice_relais_vert.id,
            }
        )
        self.assertEqual(wizard.state, "import")

        self.assertEqual(self.partner_relais_vert.vat, False)

        wizard.import_invoice()

        self.assertEqual(self.partner_relais_vert.vat, False)

        self.assertEqual(wizard.state, "import_failed")
