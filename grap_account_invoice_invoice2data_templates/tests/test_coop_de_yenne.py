# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestCoopDeYenne(TestModule):
    def test_coop_de_yenne_01(self):
        self._test_supplier_template(
            "coop-de-yenne__2023-01-09__ECS__30101035.pdf",
            line_qty=2,
            expected_values={
                "issuer": "Coop de Yenne",
                "date": datetime(day=9, month=1, year=2023),
                "date_due": datetime(day=10, month=2, year=2023),
                "invoice_number": "30101035",
                "amount_untaxed": 189.68,
                "amount": 200.11,
            },
            expected_lines=[
                {
                    "product_code": "RACBIO",
                    "product_name": "1/2 RACLETTE BIOLOGIQUE FUMEE x2",
                    "vat_code": "V5",
                    "quantity": 4.438,
                    "price_unit": 14.550,
                    "discount": 0,
                    "price_subtotal": 64.57,
                }
            ],
        )

    def test_coop_de_yenne_02(self):
        self._test_supplier_template(
            "coop-de-yenne__2023-02-28__ACR__30202038.pdf",
            line_qty=5,
            expected_values={
                "issuer": "Coop de Yenne",
                "date": datetime(day=28, month=2, year=2023),
                "date_due": datetime(day=31, month=3, year=2023),
                "invoice_number": "30202038",
                "amount_untaxed": 1294.90,
                "amount": 1366.12,
            },
            expected_lines=[
                {
                    "product_code": "T28",
                    "product_name": "TOMME DE SAVOIE AU LAIT ENTIER CRU 28%MG",
                    "vat_code": "V5",
                    "quantity": 39.63,
                    "price_unit": 9.12,
                    "discount": 0,
                    "price_subtotal": 361.43,
                }
            ],
        )

    def test_coop_de_yenne_03(self):
        self._test_supplier_template(
            "coop-de-yenne__2023-11-13__HAL__31101277.pdf",
            line_qty=4,
            expected_values={
                "issuer": "Coop de Yenne",
                "date": datetime(day=13, month=11, year=2023),
                "date_due": datetime(day=20, month=12, year=2023),
                "invoice_number": "31101277",
                "amount_untaxed": 297.44,
                "amount": 313.80,
            },
            expected_lines=[
                {
                    "product_code": "RAPE3",
                    "product_name": "RAPE 3 FROMAGES SPECIAL FONDUE x10",
                    "vat_code": "V5",
                    "quantity": 10.0,
                    "price_unit": 5.4,
                    "discount": 0,
                    "price_subtotal": 54.0,
                }
            ],
        )
