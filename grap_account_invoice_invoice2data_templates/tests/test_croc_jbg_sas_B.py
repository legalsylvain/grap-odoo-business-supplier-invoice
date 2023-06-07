# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestCrocJBGSASB(TestModule):
    def test_croc_jbg_sas_B(self):
        self._test_supplier_template(
            "croc-jbg-sas_B__2023-05-04__FA5044.pdf",
            line_qty=5,
            expected_values={
                "issuer": "Croc JBG SAS",
                "date": datetime(day=4, month=5, year=2023),
                "date_due": datetime(day=31, month=5, year=2023),
                "invoice_number": "FA5044",
                "amount_untaxed": 321.10,
                "amount": 338.76,
            },
            expected_lines=[
                {
                    "product_code": "VKAMPOT110",
                    "product_name": "CROC cajou Kampot 110g",
                    "vat_code": "5.50",
                    "quantity": 6.00,
                    "price_unit": 3.30,
                    "discount": 0.0,
                    "price_subtotal": 19.80,
                }
            ],
        )
