# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestCompanyDuRiz(TestModule):
    def test_compagnie_du_riz(self):
        self._test_supplier_template(
            "compagnie-du-riz__2023-02-06__3PP__28227.pdf",
            line_qty=17,
            expected_values={
                "issuer": "Compagnie du Riz",
                "date": datetime(day=6, month=2, year=2023),
                "date_due": datetime(day=31, month=3, year=2023),
                "invoice_number": "28227",
                "amount_untaxed": 735.43,
                "amount": 775.88,
            },
            expected_lines=[
                {
                    "product_code": "1027",
                    "product_name": "TAGLIATELLES RIZ 1/2",
                    "vat_code": "TR",
                    "quantity": 12,
                    "price_unit": 3.2850,
                    "discount": 0.0,
                }
            ],
        )
