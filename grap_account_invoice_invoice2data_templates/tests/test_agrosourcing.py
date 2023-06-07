# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestAgrosourcing(TestModule):
    def test_agrosourcing_01(self):
        self._test_supplier_template(
            "agrosourcing__2023-01-11__082083.pdf",
            line_qty=11,
            expected_values={
                "issuer": "Agrosourcing",
                "date": datetime(day=11, month=1, year=2023),
                "date_due": datetime(day=10, month=2, year=2023),
                "invoice_number": "082083",
                "amount_untaxed": 468.96,
                "amount": 501.00,
            },
            expected_lines=[
                {
                    "product_code": "000431",
                    "product_name": "Raisins de Turquie - Sultanine - 12.5 kg",
                    "vat_code": "1",
                    "quantity": 12.5,
                    "price_unit": 4.24,
                    "discount": 15,
                    "price_subtotal": 45.05,
                }
            ],
        )

    def test_agrosourcing_02(self):
        self._test_supplier_template(
            "agrosourcing__2023-06-03__088043.pdf",
            line_qty=8,
            expected_values={
                "issuer": "Agrosourcing",
                "date": datetime(day=3, month=6, year=2023),
                "date_due": datetime(day=3, month=7, year=2023),
                "invoice_number": "088043",
                "amount_untaxed": 435.27,
                "amount": 459.21,
            },
            expected_lines=[
                {
                    "product_code": "001048",
                    "product_name": "Pâte à tartiner - 75% - 4 kg x 2",
                    "vat_code": "1",
                    "quantity": 8.0,
                    "price_unit": 13.37,
                    "discount": 0.0,
                    "price_subtotal": 106.96,
                }
            ],
        )
