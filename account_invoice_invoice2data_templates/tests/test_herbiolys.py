# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestHerbiolys(TestModule):
    def test_herbiolys(self):
        self._test_supplier_template(
            "herbiolys__2023-02-13__FC_228723.pdf",
            line_qty=15,
            expected_values={
                "issuer": "Herbiolys",
                "date": datetime(day=13, month=2, year=2023),
                "date_due": datetime(day=17, month=3, year=2023),
                "invoice_number": "FC_228723",
                "amount_untaxed": 190.30,
                "amount": 207.96,
            },
            expected_lines=[
                {
                    "product_code": "00002908",
                    "product_name": "Herbiolys Huile bien-être Millepertuis 30mL COSMOS",
                    "vat_code": "20.00%",
                    "quantity": 2,
                    "price_unit": 6.20,
                    "discount": 0.0,
                    "price_subtotal": 12.40,
                }
            ],
        )
