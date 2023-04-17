# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestCelnat(TestModule):
    def test_celnat_01(self):
        self._test_supplier_template(
            "celnat__2023-04-06__23003014.pdf",
            line_qty=10,
            expected_values={
                "issuer": "Celnat",
                "date": datetime(day=6, month=4, year=2023),
                "date_due": datetime(day=10, month=5, year=2023),
                "invoice_number": "23 003014",
                "amount_untaxed": 752.91,
                "amount": 794.32,
            },
            expected_lines=[
                {
                    "product_code": "LHR/10",
                    "product_name": "Haricots Rouges Biologique",
                    "vat_code": "1",
                    "quantity": 10.00,
                    "quantity2": 2.00,
                    "price_unit": 4.994,
                    "discount": 0.0,
                    "price_subtotal": 99.88,
                }
            ],
        )
