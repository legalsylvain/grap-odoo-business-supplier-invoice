# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestComptoirDesLys(TestModule):
    def test_comptoir_des_lys(self):
        self._test_supplier_template(
            "comptoir-des-lys__2022_12_21__155753.pdf",
            line_qty=11,
            expected_values={
                "issuer": "Comptoir des Lys",
                "date": datetime(day=21, month=12, year=2022),
                "date_due": datetime(day=21, month=12, year=2022),
                "invoice_number": "155753",
                "amount_untaxed": 308.16,
                "amount": 369.79,
                "amount_extra_trade_discount_200": -34.24,
            },
            expected_lines=[
                {
                    "product_code": "0200030",
                    "product_name": "FILTRES A CAFE N°4 NON BLANCHI FSC100 U.",
                    "vat_code": "20",
                    "quantity": 24,
                    "price_unit": 1.63,
                    "discount": 12.0,
                    "price_subtotal": 34.43,
                }
            ],
        )
