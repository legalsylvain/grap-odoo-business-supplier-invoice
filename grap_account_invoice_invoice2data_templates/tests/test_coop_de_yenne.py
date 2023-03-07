# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestCoopDeYenne(TestModule):
    def test_coop_de_yenne(self):
        self._test_supplier_template(
            "coop-de-yenne__2023-01-09__30101035.pdf",
            line_qty=2,
            expected_values={
                "issuer": "Coop de Yenne",
                "date": datetime(day=9, month=1, year=2023),
                "date_due": datetime(day=10, month=2, year=2023),
                "invoice_number": "30101035",
                "amount_untaxed": 189.68,
                "amount": 200.11,
            },
            expected_lines=[
                {
                    "product_code": "RACBIO",
                    "product_name": "1/2 RACLETTE BIOLOGIQUE FUMEE x2",
                    "vat_code": "V5",
                    "quantity": 4.438,
                    "price_unit": 14.550,
                    "discount": 0,
                    "price_subtotal": 64.57,
                }
            ],
        )
