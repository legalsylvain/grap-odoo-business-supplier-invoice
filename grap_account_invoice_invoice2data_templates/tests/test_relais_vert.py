# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestRelaisVert(TestModule):
    def test_relais_vert_01(self):
        self._test_supplier_template(
            "relais-vert__2023-02-06__FC11716389.pdf",
            line_qty=6,
            expected_values={
                "issuer": "Relais Vert",
                "date": datetime(day=6, month=2, year=2023),
                "invoice_number": "FC11716389",
                "amount_untaxed": 120.90,
                "amount": 127.66,
                "amount_extra_parafiscal_tax_interfel_200": 0.25,
            },
            expected_lines=[
                {
                    "product_code": "KIJAIT",
                    "product_name": "KIWI JAUNE VRAC CAT II",
                    "vat_code": "1",
                    "quantity": 10.0,
                    "price_unit": 3.73,
                    "price_subtotal": 37.30,
                }
            ],
        )

    def test_relais_vert_02(self):
        self._test_supplier_template(
            "relais-vert__2023-03-25__FC11741819.pdf",
            line_qty=51,
            expected_values={
                "issuer": "Relais Vert",
                "date": datetime(day=25, month=3, year=2023),
                "invoice_number": "FC11741819",
                "amount_untaxed": 1000.85,
                "amount": 1056.48,
                "amount_extra_parafiscal_tax_interfel_200": 0.0,
            },
            expected_lines=[
                {
                    "product_code": "16061",
                    "product_name": "VEGE’ORIENTALES X5 (200G) WHEATY",
                    "vat_code": "1",
                    "quantity": 5.0,
                    "price_unit": 2.76,
                    "price_subtotal": 13.80,
                }
            ],
        )

    def test_relais_vert_03(self):
        self._test_supplier_template(
            "relais-vert__2023-11-22__PRE__FC11879919.pdf",
            line_qty=58,
            expected_values={
                "issuer": "Relais Vert",
                "date": datetime(day=22, month=11, year=2023),
                "invoice_number": "FC11879919",
                "amount_untaxed": 982.57,
                "amount": 1049.25,
                "amount_extra_parafiscal_tax_interfel_200": 0.38,
            },
            expected_lines=[
                {
                    "product_code": "39817",
                    "product_name": "LENTILLES VERTES FRANCE (5KG) NATUR'AVENIR",
                    "vat_code": "1",
                    "quantity": 1.0,
                    "price_unit": 19.18,
                    "price_subtotal": 19.18,
                }
            ],
        )
