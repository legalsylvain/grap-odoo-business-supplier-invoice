# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestCrocJBGSAS(TestModule):
    def test_croc_jbg_sas(self):
        self._test_supplier_template(
            "croc-jbg-sas__2023-01-26__FA4549.pdf",
            line_qty=5,
            expected_values={
                "issuer": "Croc JBG SAS",
                "date": datetime(day=26, month=1, year=2023),
                "date_due": datetime(day=25, month=2, year=2023),
                "invoice_number": "FA4549",
                "amount_untaxed": 772.75,
                "amount": 815.25,
            },
            expected_lines=[
                {
                    "product_code": "0937",
                    "product_name": "Graines de Courge nature 10 Kg",
                    "vat_code": "5.50",
                    "quantity": 10.00,
                    "price_unit": 13.20,
                    "discount": 21.59,
                    "price_subtotal": 103.50,
                }
            ],
        )
