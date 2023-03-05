# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestCds(TestModule):
    def test_cds(self):
        self._test_supplier_template(
            "cds__2023-01-30__37136.pdf",
            line_qty=4,
            expected_values={
                "issuer": "CDS",
                "date": datetime(day=30, month=1, year=2023),
                "invoice_number": "37136",
                "amount_untaxed": 694.46,
                "amount": 833.35,
            },
            expected_lines=[
                {
                    "product_code": "63JE001BV",
                    "product_name": "DESINFECTANT SANS RINCAGE 5L Colis de 4",
                    "vat_code": "1",
                    "quantity": 3,
                    "quantity2": 4,
                    "price_unit": 33.08,
                    "price_subtotal": 397.08,
                },
                {
                    "product_code": "24JE003BV",
                    "product_name": "SAVON NOIR 20KG",
                    "vat_code": "1",
                    "quantity": 2,
                    "price_unit": 73.93,
                    "price_subtotal": 147.86,
                },
            ],
        )
