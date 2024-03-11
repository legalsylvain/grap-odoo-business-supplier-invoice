# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestEcodis(TestModule):
    def test_ecodis_2_01(self):
        self._test_supplier_template(
            "ecodis__2023-12-22__HAL__371068.pdf",
            line_qty=13,
            expected_values={
                "issuer": "Ecodis",
                "version": 2,
                "date": datetime(day=22, month=12, year=2023),
                "date_due": datetime(day=22, month=1, year=2024),
                "invoice_number": "371068",
                "amount_untaxed": 440.00,
                "amount": 528.00,
            },
            expected_lines=[
                {
                    "product_code": "DO033",
                    "product_name": "Lot de 2 éponges grattantes écologiques",
                    "vat_code": "20.00",
                    "quantity": 2,
                    "quantity2": 24,
                    "price_unit": 1.15,
                    "discount": 0.0,
                    "price_subtotal": 55.20,
                }
            ],
        )
