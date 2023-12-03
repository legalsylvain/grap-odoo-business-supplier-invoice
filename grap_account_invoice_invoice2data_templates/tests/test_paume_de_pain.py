# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestPaumeDePain(TestModule):
    def test_paume_de_main_01(self):
        self._test_supplier_template(
            "paume-de-pain__2023-10-01__FAC-905.pdf",
            line_qty=8,
            expected_values={
                "issuer": "Paume de Pain",
                "date": datetime(day=1, month=10, year=2023),
                "date_due": datetime(day=3, month=10, year=2023),
                "invoice_number": "FAC-905",
                "amount_untaxed": 1291.72,
                "amount": 1362.77,
            },
            expected_lines=[
                {
                    "product_code": "ART-008",
                    "product_name": "Petit épeautre",
                    "vat_code": "5.5%",
                    "quantity": 15.5,
                    "price_unit": 10.34,
                    "price_subtotal": 160.27,
                }
            ],
        )
