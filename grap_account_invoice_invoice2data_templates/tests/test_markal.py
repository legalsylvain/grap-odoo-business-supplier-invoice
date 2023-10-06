# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestMarkal(TestModule):
    def test_markal_01(self):
        self._test_supplier_template(
            "markal__2023-02-14__00368375.pdf",
            line_qty=29,
            expected_values={
                "issuer": "Markal",
                "date": datetime(day=14, month=2, year=2023),
                "date_due": datetime(day=24, month=2, year=2023),
                "invoice_number": "00368375",
                "amount_untaxed": 818.89,
                "amount": 868.52,
                "amount_extra_trade_discount_055": -7.95,
                "amount_extra_trade_discount_200": -0.32,
            },
            expected_lines=[
                {
                    "product_code": "SPADCC500",
                    "product_name": "SPAGHETTI 1/2 COMPLET 500G/12",
                    "vat_code": "TR",
                    "quantity": 12.0,
                    "price_unit": 1.19,
                    "price_subtotal": 14.28,
                }
            ],
        )

    def test_markal_02(self):
        self._test_supplier_template(
            "markal__2023-10-04__00386108.pdf",
            line_qty=41,
            expected_values={
                "issuer": "Markal",
                "date": datetime(day=4, month=10, year=2023),
                "date_due": datetime(day=3, month=11, year=2023),
                "invoice_number": "00386108",
                "amount_untaxed": 1456.58,
                "amount": 1542.51,
            },
            expected_lines=[
                {
                    "product_code": "LUHUIOVEB5",
                    "product_name": "LU HUILE OLIVE VIERGE EXTR 5L",
                    "vat_code": "TR",
                    "quantity": 10.0,
                    "price_unit": 35.56,
                    "price_subtotal": 355.60,
                }
            ],
        )
