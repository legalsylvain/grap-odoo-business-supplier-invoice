# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestGentilsNuages(TestModule):
    def test_gentils_nuages(self):
        self._test_supplier_template(
            "gentils-nuages__2024-04-15__INT__2324-032.pdf",
            line_qty=1,
            expected_values={
                "issuer": "Gentils Nuages",
                "date": datetime(day=15, month=4, year=2024),
                "date_due": datetime(day=19, month=4, year=2024),
                "invoice_number": "2324-032",
                "amount_untaxed": 6.66,
                "amount": 7.99,
            },
            expected_lines=[
                {
                    "product_name": "Hébergement mail",
                    "vat_code": "20 %",
                    "quantity": 0.666,
                    "price_unit": 10.0,
                    "discount": 0.0,
                    "price_subtotal": 6.66,
                }
            ],
        )
