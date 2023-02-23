# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestPapillesSauvages(TestModule):
    def test_papilles_sauvages(self):
        self._test_supplier_template(
            "papilles-sauvages__2022-11-16__FAC00002114.pdf",
            line_qty=1,
            expected_values={
                "issuer": "Papilles Sauvages",
                "date": datetime(day=16, month=11, year=2022),
                "invoice_number": "FAC00002114",
                "amount_untaxed": 44.40,
                "amount": 46.84,
            },
            expected_lines=[
                {
                    "product_code": "ART00000001",
                    "product_name": "-crème de châtaigne 250g - FR-BIO-15",
                    "vat_code": "5.50",
                    "quantity": 12.00,
                    "price_unit": 3.70,
                    "discount": 0.0,
                    "price_subtotal": 44.40,
                }
            ],
        )
