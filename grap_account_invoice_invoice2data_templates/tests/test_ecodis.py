# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestEcodis(TestModule):
    def test_ecodis(self):
        self._test_supplier_template(
            "ecodis__2022-08-11__ECS__338035.pdf",
            line_qty=17,
            expected_values={
                "issuer": "Ecodis",
                "date": datetime(day=11, month=8, year=2022),
                "date_due": datetime(day=11, month=9, year=2022),
                "invoice_number": "338035",
                "amount_untaxed": 434.30,
                "amount": 510.22,
            },
            expected_lines=[
                {
                    "product_code": "DO013",
                    "product_name": "Terre de Diatomée amorphe 250 g tube",
                    "vat_code": "1",
                    "quantity": 1.0,
                    "quantity2": 6.0,
                    "price_unit": 3.45,
                    "discount": 0.0,
                    "price_subtotal": 20.70,
                }
            ],
        )
