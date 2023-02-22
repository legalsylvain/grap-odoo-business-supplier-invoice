# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestGonuts(TestModule):
    def test_gonuts(self):
        self._test_supplier_template(
            "gonuts__2022-12-19__FC002092.pdf",
            line_qty=3,
            expected_values={
                "issuer": "Gonuts",
                "date": datetime(day=19, month=12, year=2022),
                "invoice_number": "FC002092",
                "amount_untaxed": 116.28,
                "amount": 122.68,
            },
            expected_lines=[
                {
                    "product_code": "00076",
                    "product_name": "PUREE AMANDE COMPLETE TOASTEE 270G",
                    "vat_code": "TR",
                    "quantity": 9,
                    "price_unit": 6.30,
                    "discount": 0,
                    "price_subtotal": 56.70,
                }
            ],
        )
