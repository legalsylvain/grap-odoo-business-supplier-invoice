# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
from datetime import datetime

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
        self.invoice_name = "relais-vert__2023-02-06__FC11716389.pdf"
        self.product_kiwi = self.env.ref(
            "account_invoice_invoice2data.product_relais_vert_kiwi"
        )
        self.product_interfel = self.env.ref(
            "account_invoice_invoice2data.product_relais_vert_interfel"
        )
        self.product_yacon = self.env.ref(
            "account_invoice_invoice2data.product_relais_vert_yacon"
        )
        tools.config["invoice2data_templates_dir"] = self.local_templates_dir

    def _get_attachments(self, invoice):
        return self.env["ir.attachment"].search(
            [("res_model", "=", "account.invoice"), ("res_id", "=", invoice.id)]
        )

    def _get_supplierinfos(self, product):
        return self.env["product.supplierinfo"].search(
            [
                ("name", "=", self.partner_relais_vert.id),
                ("product_tmpl_id", "=", product.product_tmpl_id.id),
            ]
        )

    def test_full_workflow(self):
        # unlink previous attachment to make the test idempotens
        self._get_attachments(self.invoice_relais_vert).unlink()

        # Prepare binary data
        invoice_file = open(str(self._get_invoice_path(self.invoice_name)), "rb")
        binary_data = invoice_file.read()
        base64_data = base64.b64encode(binary_data)

        # #######################
        # Part 1 : Import Invoice
        # #######################
        wizard = self.Wizard.create(
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

        # Check that attachment has been added
        self.assertEqual(len(self._get_attachments(self.invoice_relais_vert)), 1)

        # Check that main invoice data has been analyzed correctly
        self.assertEqual(wizard.pdf_invoice_number, "FC11716389")
        self.assertEqual(wizard.pdf_amount, 127.66)
        self.assertEqual(wizard.pdf_date, datetime(day=6, month=2, year=2023).date())
        self.assertEqual(wizard.pdf_date_due, False)
        # Check 6 invoices lines + interfel tax = 7
        self.assertEqual(len(wizard.line_ids), 7)

        # #####################
        # Part 2 : Map Products
        # #####################
        self.assertEqual(len(wizard.product_mapping_line_ids), 3)
        self.assertEqual(len(wizard.to_delete_invoice_line_ids), 3)

        # Kiwi (KIJAIT) is not mapped. (supplierinfo doesn't exist)
        # We map with existing odoo product
        kiwi_line = wizard.product_mapping_line_ids.filtered(
            lambda x: x.pdf_product_code == "KIJAIT"
        )
        kiwi_line.product_id = self.product_kiwi.id
        self.assertEqual(len(self._get_supplierinfos(kiwi_line.product_id)), 0)
        wizard.map_products()
        self.assertEqual(
            len(self._get_supplierinfos(kiwi_line.product_id)),
            1,
            "Map product 'Kiwi' should have created a new supplierinfo"
            ", because it doesn't exist.",
        )
        self.assertEqual(wizard.state, "product_mapping")
        self.assertEqual(len(wizard.product_mapping_line_ids), 2)

        # Taxe Interfel (TPF) is not mapped. (supplierinfo doesn't exist)
        # We map with existing odoo product
        interfel_line = wizard.product_mapping_line_ids.filtered(
            lambda x: x.pdf_product_code == "TPF"
        )
        interfel_line.product_id = self.product_interfel.id
        self.assertEqual(len(self._get_supplierinfos(interfel_line.product_id)), 0)
        wizard.map_products()
        self.assertEqual(
            len(self._get_supplierinfos(interfel_line.product_id)),
            1,
            "Map product 'Interfel' should have created a new supplierinfo"
            ", because it doesn't exist.",
        )

        # Yacon (YAC) is bad mapped. (supplierinfo exists with different code) (YAC-YOC)
        # We map with existing odoo product
        yacon_line = wizard.product_mapping_line_ids.filtered(
            lambda x: x.pdf_product_code == "YAC"
        )
        yacon_line.product_id = self.product_yacon.id
        self.assertEqual(len(self._get_supplierinfos(yacon_line.product_id)), 1)
        wizard.map_products()
        yacon_supplierinfo = self._get_supplierinfos(yacon_line.product_id)
        self.assertEqual(
            len(yacon_supplierinfo),
            1,
            "Map product 'Yacon' should not have created a new supplierinfo"
            ", because it still exists.",
        )
        self.assertEqual(
            yacon_supplierinfo.product_code,
            "YAC",
            "Map product 'Yacon' should have updated the existing supplierinfo.",
        )

        self.assertEqual(wizard.state, "line_differences")
        self.assertEqual(len(wizard.product_mapping_line_ids), 0)
        self.assertEqual(len(wizard.to_delete_invoice_line_ids), 1)
        # ######################
        # Part 3 : Apply Changes
        # ######################

        # TODO Check the differences lines
        wizard.apply_changes()

        # Check impact on invoice
        self.assertEqual(self.invoice_relais_vert.reference, "FC11716389")

        # rerun the wizard, to check if attachment is not
        # added again
        wizard = self.Wizard.create(
            {
                "invoice_file": base64_data,
                "invoice_filename": self.invoice_name,
                "partner_id": self.partner_relais_vert.id,
                "invoice_id": self.invoice_relais_vert.id,
            }
        )
        wizard.import_invoice()

        # Check that attachment has been added
        self.assertEqual(len(self._get_attachments(self.invoice_relais_vert)), 1)
