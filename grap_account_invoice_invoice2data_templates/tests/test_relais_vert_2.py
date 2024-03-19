# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestRelaisVert(TestModule):
    def test_relais_vert_2_01(self):
        self._test_supplier_template(
            "relais-vert__2023-12-11__LUC__FC11890790.pdf",
            line_qty=76,
            expected_values={
                "issuer": "Relais Vert",
                "version": 2,
                "date": datetime(day=11, month=12, year=2023),
                "invoice_number": "FC11890790",
                "amount_untaxed": 1825.81,
                "amount": 1945.11,
                "amount_extra_parafiscal_tax_interfel_200": 1.11,
            },
            expected_lines=[
                {
                    "product_code": "15461",
                    "product_name": "TARTARE D'ALGUES CLASSIQUE (1KG) BORD A",
                    "vat_code": "1",
                    "quantity": 1.0,
                    "price_unit": 23.09,
                    "price_subtotal": 23.09,
                }
            ],
        )
