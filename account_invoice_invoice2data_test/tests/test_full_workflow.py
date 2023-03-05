# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
from datetime import datetime

from odoo import tools
from odoo.exceptions import UserError

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
        self.product_kiwi = self.env.ref(
            "account_invoice_invoice2data.product_relais_vert_kiwi"
        )
        self.product_interfel = self.env.ref(
            "account_invoice_invoice2data.product_relais_vert_interfel"
        )
        self.product_yacon = self.env.ref(
            "account_invoice_invoice2data.product_relais_vert_yacon"
        )
        self.product_arachide = self.env.ref(
            "account_invoice_invoice2data.product_relais_vert_arachide"
        )
        self.invoice_line_1_arachide = self.env.ref(
            "account_invoice_invoice2data_test.invoice_line_relais_vert_1_arachide"
        )
        self.tax_055 = self.env.ref("account_invoice_invoice2data_test.tax_055")
        self.tax_200 = self.env.ref("account_invoice_invoice2data_test.tax_200")

        self.product_uom_kgm = self.env.ref("uom.product_uom_kgm")
        tools.config["invoice2data_templates_dir"] = self.local_templates_dir

        # Prepare binary data
        self.invoice_name = "relais-vert__2023-02-06__FC11716389.pdf"
        invoice_file = open(str(self._get_invoice_path(self.invoice_name)), "rb")
        self.base64_data = base64.b64encode(invoice_file.read())

        self.bad_invoice_name = "comptoir-des-lys__2022_12_21__155753.pdf"
        bad_invoice_file = open(
            str(self._get_invoice_path(self.bad_invoice_name)), "rb"
        )
        self.bad_base64_data = base64.b64encode(bad_invoice_file.read())

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
        self.partner_relais_vert.vat = False

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

        wizard.import_invoice()

        self.assertEqual(
            self.partner_relais_vert.vat,
            "FR72352867493",
            "Import invoice should set vat on supplier.",
        )

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

        # Check the message if vat are incorrect
        self.product_arachide.supplier_taxes_id = [(6, 0, [self.tax_200.id])]
        wizard._compute_message_vat_difference()
        self.assertTrue("rachide" in wizard.message_vat_difference)

        self.product_arachide.supplier_taxes_id = [(6, 0, [self.tax_055.id])]
        wizard._compute_message_vat_difference()
        self.assertEqual(wizard.message_vat_difference, False)

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

        arachide_line = wizard.line_ids.filtered(
            lambda x: x.pdf_product_code == "39518"
        )
        arachide_line.new_uom_id = self.product_uom_kgm
        wizard.apply_changes()

        # Check impact on invoice
        self.assertEqual(self.invoice_relais_vert.reference, "FC11716389")

        # Check Impact on invoice lines
        self.assertEqual(self.invoice_line_1_arachide.uom_id, self.product_uom_kgm)

        # #######################################
        # Part 4 : rerun the wizard with same pdf
        # #######################################
        wizard = self.Wizard.create(
            {
                "invoice_file": self.base64_data,
                "invoice_filename": self.invoice_name,
                "partner_id": self.partner_relais_vert.id,
                "invoice_id": self.invoice_relais_vert.id,
            }
        )
        wizard.import_invoice()

        self.assertEqual(wizard.supplier_name_different, False)

        # Check that attachment has not been added again
        self.assertEqual(len(self._get_attachments(self.invoice_relais_vert)), 1)

        # ############################################
        # Part 5 : rerun the wizard with incorrect pdf
        # ############################################
        wizard = self.Wizard.create(
            {
                "invoice_file": self.bad_base64_data,
                "invoice_filename": self.bad_invoice_name,
                "partner_id": self.partner_relais_vert.id,
                "invoice_id": self.invoice_relais_vert.id,
            }
        )
        wizard.import_invoice()

        self.assertNotEqual(wizard.supplier_name_different, False)

        # ################################################
        # Part 6 : rerun the wizard with confirmed invoice
        # ################################################
        self.invoice_relais_vert.action_invoice_open()
        with self.assertRaises(UserError):
            wizard = self.Wizard.create(
                {
                    "invoice_file": self.base64_data,
                    "invoice_filename": self.invoice_name,
                    "partner_id": self.partner_relais_vert.id,
                    "invoice_id": self.invoice_relais_vert.id,
                }
            )
