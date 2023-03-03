# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestSenfas(TestModule):
    def test_senfas(self):
        self._test_supplier_template(
            "senfas__2022_04_22__FA226692.pdf",
            line_qty=12,
            expected_values={
                "issuer": "Senfas",
                "date": datetime(day=21, month=4, year=2022),
                "date_due": datetime(day=21, month=5, year=2022),
                "invoice_number": "FA226692",
                "amount_untaxed": 626.34,
                "amount": 666.97,
            },
            expected_lines=[
                {
                    "product_code": "N050132",
                    "product_name": "Sucre de fleur de coco Bio AB 20kg",
                    "vat_code": "C55",
                    "quantity": 20.00,
                    "price_unit": 6.19,
                    "discount": 25,
                    "price_subtotal": 92.85,
                }
            ],
        )
