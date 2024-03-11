# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestScopEpice(TestModule):
    def test_scop_epice_1(self):
        self._test_supplier_template(
            "scop-epice__2024-03-05__CHE__FV84123.pdf",
            line_qty=16,
            expected_values={
                "issuer": "Scop Epice",
                "version": 2,
                "date": datetime(day=5, month=3, year=2024),
                "date_due": datetime(day=4, month=4, year=2024),
                "invoice_number": "FV84123",
                "amount_untaxed": 433.92,
                "amount": 462.42,
            },
            expected_lines=[
                {
                    "product_code": "ROUDSA3L",
                    "product_name": "Vin ROUGE Saint Alban BIB 3 litres",
                    "vat_code": "C5",
                    "quantity": 3.0,
                    "price_unit": 10.65,
                    "price_subtotal": 31.95,
                },
                {
                    "product_code": "SVA2X8",
                    "product_name": "Sucre vanillé 2x8g",
                    "vat_code": "C2",
                    "quantity": 20.0,
                    "price_unit": 1.32,
                    "price_subtotal": 26.40,
                },
            ],
        )
