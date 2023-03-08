# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestBiodis(TestModule):
    def test_biodis(self):
        self._test_supplier_template(
            "biodis__2022-09-23__592740.pdf",
            line_qty=11,
            expected_values={
                "issuer": "Biodis",
                "date": datetime(day=23, month=9, year=2022),
                "date_due": datetime(day=14, month=10, year=2022),
                "invoice_number": "592740",
                "amount_untaxed": 759.65,
                "amount": 831.05,
                "amount_extra_fuel_surcharge_200": 3.25,
            },
            expected_lines=[
                {
                    "product_code": "400724",
                    "product_name": "Sauce pizza aux tomates de France. 290g",
                    "vat_code": "1",
                    "quantity": 12,
                    "price_unit": 1.81,
                    "price_subtotal": 21.72,
                }
            ],
        )
