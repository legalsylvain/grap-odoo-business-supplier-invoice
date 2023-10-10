# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestSaldac(TestModule):
    def test_saldac_01(self):
        self._test_supplier_template(
            "saldac__2022-12-07__ECS__FA22-4381.pdf",
            line_qty=5,
            expected_values={
                "issuer": "Saldac",
                "date": datetime(day=7, month=12, year=2022),
                "date_due": datetime(day=6, month=1, year=2023),
                "invoice_number": "FA22/4381",
                "amount_untaxed": 430.10,
                "amount": 453.76,
            },
            expected_lines=[
                {
                    "product_code": "COUV70",
                    "product_name": "Chocolat de couverture biologique 70%. pure origine",
                    "vat_code": "2",
                    "quantity": 1.0,
                    "price_unit": 34.90,
                    "price_subtotal": 34.90,
                }
            ],
        )

    def test_saldac_02(self):
        self._test_supplier_template(
            "saldac__2023-01-27__3PP__FA23-0391.pdf",
            line_qty=10,
            expected_values={
                "issuer": "Saldac",
                "date": datetime(day=27, month=1, year=2023),
                "date_due": datetime(day=26, month=2, year=2023),
                "invoice_number": "FA23/0391",
                "amount_untaxed": 668.33,
                "amount": 710.81,
            },
            expected_lines=[
                {
                    "product_code": "SUCRE5KG",
                    "product_name": "Sucre de canne complet Pérou. bio sac de 5 kg. certifié",
                    "vat_code": "2",
                    "quantity": 3.0,
                    "price_unit": 17.40,
                    "price_subtotal": 52.20,
                }
            ],
        )

    def test_saldac_03(self):
        self._test_supplier_template(
            "saldac__2023-03-01__ACR__FA23-0825.pdf",
            line_qty=12,
            expected_values={
                "issuer": "Saldac",
                "date": datetime(day=1, month=3, year=2023),
                "date_due": datetime(day=31, month=3, year=2023),
                "invoice_number": "FA23/0825",
                "amount_untaxed": 984.95,
                "amount": 1039.12,
            },
            expected_lines=[
                {
                    "product_code": "GOUTTE63",
                    "product_name": "Couverture noir 63 %. bio. en gouttes."
                    " prix du sac de 2 kg.",
                    "vat_code": "2",
                    "quantity": 15.0,
                    "price_unit": 25.50,
                    "price_subtotal": 382.50,
                }
            ],
        )
