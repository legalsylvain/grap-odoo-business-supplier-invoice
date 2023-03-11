# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
import logging

from .test_module import TestModule

_logger = logging.getLogger(__name__)


class TestAllTemplates(TestModule):
    def setUp(self):
        super().setUp()
        self.AccountInvoice = self.env["account.invoice"]
        self.Wizard = self.env["wizard.invoice2data.import"]
        self.random_draft_invoice = self.env.ref(
            "account_invoice_invoice2data.invoice_wood_corner"
        )

    def _test_import_file(self, invoice_name):
        _logger.info("Importing %s Files ..." % invoice_name)

        # Prepare binary data
        invoice_file = open(str(self._get_invoice_path(invoice_name)), "rb")
        binary_data = invoice_file.read()

        wizard = self.Wizard.create(
            {
                "invoice_file": base64.b64encode(binary_data),
                "invoice_filename": invoice_name,
                "partner_id": self.random_draft_invoice.partner_id.id,
                "invoice_id": self.random_draft_invoice.id,
            }
        )
        wizard.import_invoice()

    def test_all_import(self):
        for file in self.pdf_folder_path.iterdir():
            if file.name.endswith(".pdf.encrypted") and not file.name.startswith("_"):
                invoice_name = file.name.replace(".encrypted", "")
                self._test_import_file(invoice_name)
