# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestJeanHerve(TestModule):
    def test_jean_herve_01(self):
        self._test_supplier_template(
            "jean-herve__2023-03-06__3PP__0230791.pdf",
            line_qty=14,
            expected_values={
                "issuer": "Jean Hervé",
                "date": datetime(day=6, month=3, year=2023),
                "date_due": datetime(day=20, month=4, year=2023),
                "invoice_number": "0230791",
                "amount_untaxed": 1045.76,
                "amount": 1115.37,
                "amount_extra_shipping_costs_200": 41.66,
            },
            expected_lines=[
                {
                    "product_code": "ERABLE5",
                    "product_name": "SIROP D'ERABLE BIO 5L",
                    "vat_code": "1",
                    "quantity": 2.0,
                    "price_unit": 73.14,
                    "price_subtotal": 146.28,
                }
            ],
        )
