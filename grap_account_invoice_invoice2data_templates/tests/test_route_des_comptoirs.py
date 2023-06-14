# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestRouteDesComptoirs(TestModule):
    def test_route_des_comptoirs(self):
        self._test_supplier_template(
            "route-des-comptoirs__2023-06-13__190852.pdf",
            # 10 lines, but a shitty one (20 INFU)
            line_qty=9,
            expected_values={
                "issuer": "La route des comptoirs",
                "date": datetime(day=13, month=6, year=2023),
                "date_due": datetime(day=13, month=7, year=2023),
                "invoice_number": "190852",
                "amount_untaxed": 224.63,
                "amount": 236.98,
            },
            expected_lines=[
                {
                    "product_code": "TVS129",
                    "product_name": "Thé vert GINGEMBRE CURCUMA 100G",
                    "vat_code": "5.5",
                    "quantity": 6.0,
                    "price_unit": 4.29,
                    "discount": 10.0,
                    "price_subtotal": 23.17,
                }
            ],
        )
