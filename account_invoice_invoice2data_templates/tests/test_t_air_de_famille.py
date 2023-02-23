# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestTAirDeFamille(TestModule):
    def test_t_air_de_famille(self):
        self._test_supplier_template(
            "t-air-de-famille__2023-02-01__FA20230020.pdf",
            line_qty=4,
            expected_values={
                "issuer": "T'air de Famille",
                "date": datetime(day=1, month=2, year=2023),
                "invoice_number": "FA20230020",
                "amount_untaxed": 83.76,
                "amount": 88.37,
            },
            expected_lines=[
                {
                    "product_code": "AR00101",
                    "product_name": "Purée de pomme 1kg x 6",
                    "vat_code": False,
                    "quantity": 1,
                    "price_unit": 20.28,
                    "price_subtotal": 20.28,
                }
            ],
        )
