# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestCafesDagobert(TestModule):
    def test_cafes_dagobert(self):
        self._test_supplier_template(
            "cafes-dagobert__2023-03-03__HAL__FC222028.pdf",
            line_qty=4,
            expected_values={
                "issuer": "Les Cafés Dagobert",
                "date": datetime(day=3, month=3, year=2023),
                "date_due": datetime(day=2, month=4, year=2023),
                "invoice_number": "FC222028",
                "amount_untaxed": 280.50,
                "amount": 295.93,
            },
            expected_lines=[
                {
                    "product_code": "MPTBFTO250F",
                    "product_name": "MELANGE MON P'TIT BIO FAIR FOR LIFE 250 GR FILTRE",
                    "vat_code": "5.5",
                    "quantity": 15,
                    "price_unit": 3.20,
                    "price_subtotal": 48.0,
                },
            ],
        )
