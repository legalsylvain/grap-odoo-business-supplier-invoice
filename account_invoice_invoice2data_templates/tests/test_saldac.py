# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestSaldac(TestModule):
    def test_saldac(self):
        self._test_supplier_template(
            "saldac__2022_12_07__FA22-4381.pdf",
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
