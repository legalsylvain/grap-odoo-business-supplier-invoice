# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestBiodis(TestModule):
    def test_biodis_01(self):
        self._test_supplier_template(
            "biodis__2022-09-23__EPV__592740.pdf",
            line_qty=11,
            expected_values={
                "issuer": "Biodis",
                "date": datetime(day=23, month=9, year=2022),
                "date_due": datetime(day=14, month=10, year=2022),
                "invoice_number": "592740",
                "amount_untaxed": 759.65,
                "amount_untaxed_055": 555.39,
                "amount_untaxed_200": 204.26,
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

    def test_biodis_02(self):
        self._test_supplier_template(
            "biodis__2024-01-12__CC__670682.pdf",
            line_qty=14 + 20 + 19 + 20 + 20 + 19 + 19 + 12,
            expected_values={
                "issuer": "Biodis",
                "date": datetime(day=12, month=1, year=2024),
                "date_due": datetime(day=12, month=2, year=2024),
                "invoice_number": "670682",
                "amount_untaxed": 3407.62,
                "amount_untaxed_055": 2957.88,
                "amount_untaxed_200": 449.74,
                "amount": 3660.25,
                "amount_extra_parafiscal_tax_interfel_no_fr_055": 0.49,
                "amount_extra_parafiscal_tax_interfel_fr_055": 0.95,
            },
            expected_lines=[
                {
                    "product_code": "39400",
                    "product_name": "Noix de cajou W320 - Origine : Viet Nam",
                    "vat_code": "1",
                    "quantity": 5.0,
                    "price_unit": 9.46,
                    "price_subtotal": 47.30,
                }
            ],
        )
