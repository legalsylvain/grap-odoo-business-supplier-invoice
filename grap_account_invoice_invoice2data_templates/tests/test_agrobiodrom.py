# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestAgrobiodrom(TestModule):
    def test_agrobiodrom_01(self):
        self._test_supplier_template(
            "agrobiodrom__2023-05-27__HAL__264951.pdf",
            line_qty=31,
            expected_values={
                "issuer": "Agrobiodrom",
                "date": datetime(day=27, month=5, year=2023),
                "date_due": datetime(day=17, month=6, year=2023),
                "invoice_number": "264951",
                "amount_untaxed": 928.16,
                "amount": 980.18,
                "amount_extra_parafiscal_tax_interfel_200": 0.19,
            },
            expected_lines=[
                {
                    "product_name": "POMME DE TERRE GRENAILLE",
                    "vat_code": "1",
                    "quantity": 10.00,
                    "price_unit": 1.65,
                    "discount": 0.0,
                    "price_subtotal": 16.50,
                }
            ],
        )

    def test_agrobiodrom_02(self):
        self._test_supplier_template(
            "agrobiodrom__2024-02-24__COT__282376.pdf",
            line_qty=22,
            expected_values={
                "issuer": "Agrobiodrom",
                "date": datetime(day=26, month=2, year=2024),
                "date_due": datetime(day=27, month=3, year=2024),
                "invoice_number": "282376",
                "amount_untaxed": 354.90,
                "amount": 374.42,
            },
            expected_lines=[
                {
                    "product_name": "NAVET VIOLET FR X 5 KG 150-300",
                    "vat_code": "1",
                    "quantity": 5.0,
                    "price_unit": 2.16,
                    "price_subtotal": 10.80,
                }
            ],
        )
