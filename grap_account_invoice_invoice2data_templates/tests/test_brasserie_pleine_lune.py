# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestBrasseriePleineLune(TestModule):
    def test_brasserie_pleine_lune_01(self):
        self._test_supplier_template(
            "brasserie-pleine-lune__2023-04-20__VIN__VT-2023040152.pdf",
            line_qty=9,
            expected_values={
                "issuer": "Brasserie Pleine Lune",
                "date": datetime(day=20, month=4, year=2023),
                "date_due": datetime(day=20, month=6, year=2023),
                "invoice_number": "VT-2023040152",
                "amount_untaxed": 2002.20,
                "amount": 2384.20,
            },
            expected_lines=[
                {
                    "product_code": "CONT30",
                    "product_name": "CONTEUSE DE LUNE - SESSION PALE ALE - 30L",
                    "vat_code": "1",
                    "quantity": 4.00,
                    "price_unit": 75.2000,
                    "discount": 0.0,
                    "price_subtotal": 300.80,
                },
                {
                    "product_code": "LIMO33",
                    "product_name": "LIMOONADE - LIMONADE AU CITRON - BIO - 33CL",
                    "vat_code": "3",
                    "quantity": 120.00,
                    "price_unit": 1.06,
                    "discount": 0.0,
                    "price_subtotal": 127.20,
                },
            ],
        )

    def test_brasserie_pleine_lune_02(self):
        self._test_supplier_template(
            "brasserie-pleine-lune__2023-04-22__VIN__VT-2023040173.pdf",
            line_qty=9,
            expected_values={
                "issuer": "Brasserie Pleine Lune",
                "date": datetime(day=22, month=4, year=2023),
                "date_due": datetime(day=22, month=6, year=2023),
                "invoice_number": "VT-2023040173",
                "amount_untaxed": 714.97,
                "amount": 787.96,
            },
            expected_lines=[
                {
                    "product_code": "ECLSA75",
                    "product_name": "ECLIPSES 2022 SAISON EPEAUTRE BARRIQUES DE VIN -",
                    "vat_code": "1",
                    "quantity": 12.00,
                    "price_unit": 4.5040,
                    "discount": 0.0,
                    "price_subtotal": 54.05,
                },
                {
                    "product_code": "004091",
                    "product_name": "ECOCUP SÉRIGRAPHIÉS 25CL",
                    "vat_code": "4",
                    "quantity": 500.00,
                    "price_unit": 0.70,
                    "discount": 0.0,
                    "price_subtotal": 350.00,
                },
            ],
        )
