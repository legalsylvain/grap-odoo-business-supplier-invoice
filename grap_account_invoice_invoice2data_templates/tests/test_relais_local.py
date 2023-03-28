# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestRelaisLocal(TestModule):
    def test_relais_local_01(self):
        self._test_supplier_template(
            "relais-local__2023-01-03__FC230116989.pdf",
            line_qty=13,
            expected_values={
                "issuer": "Relais Local",
                "date": datetime(day=3, month=1, year=2023),
                "date_due": datetime(day=24, month=1, year=2023),
                "invoice_number": "FC230116989",
                "amount_untaxed": 319.39,
                "amount": 336.96,
            },
            expected_lines=[
                {
                    "product_code": "102355",
                    "product_name": "TOME DE BREBIS VRAC",
                    "vat_code": "3",
                    "quantity": 3.0,
                    "price_unit": 24.38,
                    "price_subtotal": 73.14,
                }
            ],
        )

    def test_relais_local_02(self):
        self._test_supplier_template(
            "relais-local__2023-02-27__FC230217945.pdf",
            line_qty=21,
            expected_values={
                "issuer": "Relais Local",
                "date": datetime(day=27, month=2, year=2023),
                "date_due": datetime(day=20, month=3, year=2023),
                "invoice_number": "FC230217945",
                "amount_untaxed": 696.45,
                "amount": 748.73,
            },
            expected_lines=[
                {
                    "product_code": "120145",
                    "product_name": "POIRE SELENA 55/60 vrac 13kg",
                    "vat_code": "3",
                    "quantity": 13.0,
                    "price_unit": 2.50,
                    "price_subtotal": 32.50,
                }
            ],
        )

    def test_relais_local_03(self):
        self._test_supplier_template(
            "relais-local__2023-03-28__FC230318459.pdf",
            # 21 lines in the real life, but the
            # salade lines is bad, so we enable
            # fuzzy_total_amount_untaxed
            line_qty=20,
            expected_values={
                "issuer": "Relais Local",
                "date": datetime(day=28, month=3, year=2023),
                "date_due": datetime(day=18, month=4, year=2023),
                "invoice_number": "FC230318459",
                "amount_untaxed": 426.06,
                "amount": 449.49,
            },
            expected_lines=[
                {
                    "product_code": "120517",
                    "product_name": "GINGEMBRE",
                    "vat_code": "3",
                    "quantity": 2.0,
                    "price_unit": 5.20,
                    "price_subtotal": 10.40,
                }
            ],
        )
