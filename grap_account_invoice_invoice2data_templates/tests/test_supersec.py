# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestSupersec(TestModule):
    def test_supersec(self):
        self._test_supplier_template(
            "supersec__2023-01-11__SS-23-2638.pdf",
            line_qty=11,
            expected_values={
                "issuer": "Supersec",
                "date": datetime(day=11, month=1, year=2023),
                "date_due": datetime(day=11, month=2, year=2023),
                "invoice_number": "SS_23 2638",
                "amount_untaxed": 509.80,
                "amount": 509.80,
            },
            expected_lines=[
                {
                    "product_name": "Vrac - Tablette Blanc",
                    "quantity": 25,
                    "price_unit": 1.69,
                    "discount": 0.0,
                    "price_subtotal": 42.25,
                },
                {
                    "product_name": "Transport France Express",
                    "quantity": 1,
                    "price_unit": 19.0,
                    "discount": 0.0,
                    "price_subtotal": 19.0,
                },
            ],
        )
