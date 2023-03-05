# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestCafesDagobert(TestModule):
    def test_cafes_dagobert(self):
        self._test_supplier_template(
            "cafes-dagobert__2023-01-18__FR0001OP-2301022.pdf",
            line_qty=3,
            expected_values={
                "issuer": "Les Cafés Dagobert",
                "date": datetime(day=18, month=1, year=2023),
                "date_due": datetime(day=18, month=1, year=2023),
                "invoice_number": "FR0001OP-2301022",
                "amount_untaxed": 157.00,
                "amount": 165.64,
            },
            expected_lines=[
                {
                    "product_code": "CHICO200",
                    "product_name": "Chicoree torrefiee soluble bio 200 gr",
                    "vat_code": "5.5%",
                    "quantity": 14,
                    "price_unit": 4.95,
                    "price_subtotal": 69.30,
                },
            ],
        )
