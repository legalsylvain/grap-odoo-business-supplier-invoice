# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestBrasserieTeddyBear(TestModule):
    def test_brasserie_teddy_bear_01(self):
        self._test_supplier_template(
            "brasserie-teddy-beer__2022-12-01__FA2212-3445.pdf",
            line_qty=4,
            expected_values={
                "issuer": "Brasserie Teddy Bear",
                "date": datetime(day=1, month=12, year=2022),
                "date_due": datetime(day=31, month=12, year=2022),
                "invoice_number": "FA2212-3445",
                "amount_untaxed": 44.04,
                "amount": 52.84,
            },
            expected_lines=[
                {
                    "product_code": "miel75",
                    "product_name": "Ô Miel - 75cl",
                    "vat_code": "20%",
                    "quantity": 6,
                    "price_unit": 3.7533,
                    "price_subtotal": 22.52,
                }
            ],
        )

    def test_brasserie_teddy_bear_02(self):
        self._test_supplier_template(
            "brasserie-teddy-beer__2023-05-30__FA2305-3709.pdf",
            line_qty=14,
            expected_values={
                "issuer": "Brasserie Teddy Bear",
                "date": datetime(day=30, month=5, year=2023),
                "date_due": datetime(day=30, month=6, year=2023),
                "invoice_number": "FA2305-3709",
                "amount_untaxed": 122.68,
                "amount": 147.20,
            },
            expected_lines=[
                {
                    "product_code": "Stout33",
                    "product_name": "Complètement Stout - 33cl",
                    "vat_code": "20%",
                    "quantity": 12,
                    "price_unit": 1.68833,
                    "price_subtotal": 20.26,
                }
            ],
        )
