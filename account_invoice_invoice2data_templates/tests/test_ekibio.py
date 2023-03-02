# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestEkibio(TestModule):
    def test_ekibio_01(self):
        self._test_supplier_template(
            "ekibio__2023-02-02__791601.pdf",
            line_qty=35,
            expected_values={
                "issuer": "Ekibio",
                "date": datetime(day=2, month=2, year=2023),
                "date_due": datetime(day=4, month=3, year=2023),
                "invoice_number": "791601",
                "amount_untaxed": 965.60,
                "amount": 1020.81,
            },
            expected_lines=[
                {
                    "product_code": "005844",
                    "product_name": "PROTEGE SLIP 24u",
                    "vat_code": "1",
                    "quantity": 12.0,
                    "price_unit": 2.780,
                    "price_subtotal": 33.36,
                }
            ],
        )

    def test_ekibio_02(self):
        self._test_supplier_template(
            "ekibio__2023-02-07__792437.pdf",
            line_qty=18,
            expected_values={
                "issuer": "Ekibio",
                "date": datetime(day=7, month=2, year=2023),
                "date_due": datetime(day=9, month=3, year=2023),
                "invoice_number": "792437",
                "amount_untaxed": 625.55,
                "amount": 671.37,
            },
            expected_lines=[
                {
                    "product_code": "010118",
                    "product_name": "COUSCOUS DEMI COMPLET FILIERE FRANCE 5KG",
                    "vat_code": "1",
                    "quantity": 10.0,
                    "price_unit": 2.56,
                    "price_subtotal": 25.60,
                }
            ],
        )
