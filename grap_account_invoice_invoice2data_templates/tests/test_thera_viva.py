# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestTheraViva(TestModule):
    def test_thera_viva_01(self):
        self._test_supplier_template(
            "thera-viva__2023-06-20__294762.pdf",
            line_qty=17,
            expected_values={
                "issuer": "Thera Viva",
                "date": datetime(day=20, month=6, year=2023),
                "date_due": datetime(day=20, month=7, year=2023),
                "invoice_number": "294762",
                "amount_untaxed": 351.34,
                "amount": 370.66,
            },
            expected_lines=[
                {
                    "product_code": "151754",
                    "product_name": "YOGI THE VERT JASMIN",
                    "vat_code": "2",
                    "quantity": 6.0,
                    "price_unit": 2.44,
                    "price_subtotal": 14.64,
                }
            ],
        )
