# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestFermeDesGrandsNoyers(TestModule):
    def test_fermeDesGrandsNoyers(self):
        self._test_supplier_template(
            "ferme-des-grands-noyers__2022-12-31__EPV__FV-2022-146.pdf",
            line_qty=9,
            expected_values={
                "issuer": "La Ferme des Grands Noyers",
                "date": datetime(day=31, month=12, year=2022),
                "date_due": datetime(day=30, month=1, year=2023),
                "invoice_number": "FV 2022 146",
                "amount_untaxed": 532.32,
                "amount": 561.60,
            },
            expected_lines=[
                {
                    "product_name": "Oeufs par 30",
                    "vat_code": "5.50%",
                    "quantity": 36,
                    "price_unit": 9.48,
                    "discount": 0.0,
                    "price_subtotal": 341.23,
                }
            ],
        )
