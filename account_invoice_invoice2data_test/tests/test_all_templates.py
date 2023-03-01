# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
import logging

from odoo import tools

from odoo.addons.account_invoice_invoice2data_templates.tests.test import TestModule

_logger = logging.getLogger(__name__)

_INVOICE_FILES = [
    "agrosourcing__2023-01-11__082083.pdf",
    "comptoir-des-lys__2022_12_21__155753.pdf",
    "coop-de-yenne__2023-01-09__30101035.pdf",
    "croc-jbg-sas__2023-01-26__FA4549.pdf",
    "ekibio__2023-02-07__792437.pdf",
    "gonuts__2022-12-19__FC002092.pdf",
    "gravier__2022-11-16__FA1375938.pdf",
    "markal__2023-02-14__00368375.pdf",
    "papilles-sauvages__2022-11-16__FAC00002114.pdf",
    "relais-local__2023-01-03__FC230116989.pdf",
    "relais-local__2023-02-27__FC230217945.pdf",
    "relais-vert__2023-02-06__FC11716389.pdf",
    "t-air-de-famille__2023-02-01__FA20230020.pdf",
    "vitafrais__2023-02-13__23013043.pdf",
]


class TestAllTemplates(TestModule):
    def setUp(self):
        super().setUp()
        self.AccountInvoice = self.env["account.invoice"]
        self.Wizard = self.env["wizard.invoice2data.import"]
        self.random_draft_invoice = self.env.ref("l10n_generic_coa.demo_invoice_0")
        tools.config["invoice2data_templates_dir"] = self.local_templates_dir

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
        for invoice_name in _INVOICE_FILES:
            self._test_import_file(invoice_name)
