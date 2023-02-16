# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
from datetime import datetime

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
        self.invoice_name = "relais-vert__2023-02-06__FC11716389.pdf"
        self.product_kiwi = self.env.ref(
            "account_invoice_invoice2data.product_relais_vert_kiwi"
        )
        self.product_interfel = self.env.ref(
            "account_invoice_invoice2data.product_relais_vert_interfel"
        )

    def test_full_workflow(self):
        invoice_file = open(str(self._get_invoice_path(self.invoice_name)), "rb")
        binary_data = invoice_file.read()
        base64_data = base64.b64encode(binary_data)

        # Part 1 : Import Invoice
        wizard = self.Wizard.with_context(
            invoice2data_templates_dir=self.local_templates_dir
        ).create(
            {
                "invoice_file": base64_data,
                "invoice_filename": self.invoice_name,
                "partner_id": self.partner_relais_vert.id,
                "invoice_id": self.invoice_relais_vert.id,
            }
        )
        self.assertEqual(wizard.state, "import")

        wizard.import_invoice()
        self.assertEqual(wizard.state, "product_mapping")

        # Check that main invoice data has been analyzed correctly
        self.assertEqual(wizard.pdf_invoice_number, "FC11716389")
        self.assertEqual(wizard.pdf_amount, 127.66)
        self.assertEqual(wizard.pdf_date, datetime(day=6, month=2, year=2023).date())
        self.assertEqual(wizard.pdf_date_due, False)
        # Check 6 invoices lines + interfel tax = 7
        self.assertEqual(len(wizard.line_ids), 7)
        self.assertEqual(len(wizard.product_mapping_line_ids), 2)

        kiwi_line = wizard.product_mapping_line_ids.filtered(
            lambda x: x.pdf_product_code == "KIJAIT"
        )
        kiwi_line.product_id = self.product_kiwi.id

        wizard.map_products()
        self.assertEqual(wizard.state, "product_mapping")
        self.assertEqual(len(wizard.product_mapping_line_ids), 1)

        interfel_line = wizard.product_mapping_line_ids.filtered(
            lambda x: x.pdf_product_code == "TPF"
        )
        interfel_line.product_id = self.product_interfel.id

        wizard.map_products()
        self.assertEqual(wizard.state, "line_differences")
        self.assertEqual(len(wizard.product_mapping_line_ids), 0)
        # TODO Check the differences lines

        wizard.apply_changes()

        # Check impact on invoice
        self.assertEqual(self.invoice_relais_vert.reference, "FC11716389")
