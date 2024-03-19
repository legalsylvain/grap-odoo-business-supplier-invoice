# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestScopEpice(TestModule):
    def test_scop_epice(self):
        self._test_supplier_template(
            "scop-epice__2023-02-15__GAE__FV70067.pdf",
            line_qty=6,
            expected_values={
                "issuer": "Scop Epice",
                "date": datetime(day=15, month=2, year=2023),
                "date_due": datetime(day=17, month=3, year=2023),
                "invoice_number": "FV70067",
                "amount_untaxed": 174.19,
                "amount": 183.77,
            },
            expected_lines=[
                {
                    "product_code": "CNCSAL100",
                    "product_name": "Chocolat noir au café El Inti 100g",
                    "vat_code": "2",
                    "quantity": 19.000,
                    "price_unit": 2.19,
                    "discount": 0,
                    "price_subtotal": 41.61,
                }
            ],
        )
