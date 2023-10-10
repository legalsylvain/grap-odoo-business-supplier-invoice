# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestHelpac(TestModule):
    def test_helpac(self):
        self._test_supplier_template(
            "helpac__2023-02-17__EPV__127404.pdf",
            line_qty=13,
            expected_values={
                "issuer": "Helpac",
                "date": datetime(day=17, month=2, year=2023),
                "date_due": datetime(day=17, month=3, year=2023),
                "invoice_number": "127404",
                "amount_untaxed": 163.53,
                "amount": 184.96,
            },
            expected_lines=[
                {
                    "product_code": "HEB074B",
                    "product_name": "HE ORANGE DOUCE BIO 10ML",
                    "vat_code": "2",
                    "quantity": 2,
                    "price_unit": 2.51,
                    "discount": 0,
                    "price_subtotal": 5.02,
                }
            ],
        )
