# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestGravier(TestModule):
    def test_gravier(self):
        self._test_supplier_template(
            "gravier__2022-11-16__FA1375938.pdf",
            line_qty=4,
            expected_values={
                "issuer": "Gravier",
                "date": datetime(day=16, month=11, year=2022),
                "invoice_number": "FA1375938",
                "amount": 349.38,
                "amount_untaxed": 291.15,
            },
            expected_lines=[
                {
                    "product_code": "LE00001402",
                    "product_name": "LIQUIDE VAISSELLE MAIN ULTRA DEGRAISSANT 5L",
                    "quantity": 4.0,
                    "price_unit": 14.19,
                    "discount": 20.0,
                    "price_subtotal": 45.41,
                }
            ],
        )
