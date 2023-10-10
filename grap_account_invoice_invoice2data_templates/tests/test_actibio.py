# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestAgrosourcing(TestModule):
    def test_actibio_01(self):
        self._test_supplier_template(
            "actibio__2022-06-01__EPV__22FV06621.pdf",
            line_qty=6,
            expected_values={
                "issuer": "Actibio",
                "date": datetime(day=1, month=6, year=2022),
                "date_due": datetime(day=1, month=7, year=2022),
                "invoice_number": "22FV06621",
                "amount_untaxed": 399.75,
                "amount": 421.74,
            },
            expected_lines=[
                {
                    "product_code": "08115",
                    "product_name": "CHANVRE BIO° 5 KG - FRANCE",
                    "vat_code": "V05",
                    "quantity": 5.00,
                    "price_unit": 4.06,
                    "discount": 0.0,
                    "price_subtotal": 20.30,
                }
            ],
        )

    def test_actibio_02(self):
        self._test_supplier_template(
            "actibio__2023-03-07__3PP__23FV02108.pdf",
            line_qty=25,
            expected_values={
                "issuer": "Actibio",
                "date": datetime(day=7, month=3, year=2023),
                "date_due": datetime(day=6, month=4, year=2023),
                "invoice_number": "23FV02108",
                "amount_untaxed": 1002.17,
                "amount": 1057.29,
            },
            expected_lines=[
                {
                    "product_code": "07475",
                    "product_name": "PATES SPIRALES COMPLÈTES BIO° 5KG NOUV 01/23",
                    "vat_code": "V05",
                    "quantity": 10.0,
                    "price_unit": 1.91,
                    "discount": 0.0,
                    "price_subtotal": 19.10,
                }
            ],
        )
