# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestPural(TestModule):
    def test_pural_01(self):
        self._test_supplier_template(
            "pural__2023-04-13__805551.pdf",
            # there is 35 lines, but one is not found
            line_qty=34,
            expected_values={
                "issuer": "Pural",
                "date": datetime(day=13, month=4, year=2023),
                "date_due": datetime(day=13, month=5, year=2023),
                "invoice_number": "805551",
                "amount_untaxed": 644.89,
                "amount": 693.76,
                "amount_extra_energy_cost_055": 2.20,
                "amount_extra_energy_cost_200": 0.37,
            },
            expected_lines=[
                {
                    "product_code": "747/110010",
                    "product_name": "Fil Dentaire Vegan",
                    "vat_code": "2",
                    "quantity": 6.0,
                    "price_unit": 1.31,
                    "discount": 0.0,
                    "price_subtotal": 7.86,
                }
            ],
        )

    def test_pural_02(self):
        self._test_supplier_template(
            "pural__2023-05-12__809155.pdf",
            line_qty=25,
            expected_values={
                "issuer": "Pural",
                "date": datetime(day=16, month=5, year=2023),
                "date_due": datetime(day=15, month=6, year=2023),
                "invoice_number": "809155",
                "amount_untaxed": 576.89,
                "amount": 610.07,
                "amount_extra_energy_cost_055": 2.26,
                "amount_extra_energy_cost_200": 0.04,
            },
            expected_lines=[
                {
                    "product_code": "690/16105",
                    "product_name": "Crusty chia                                 200 g",
                    "vat_code": "1",
                    "quantity": 10.0,
                    "price_unit": 2.22,
                    "discount": 0.0,
                    "price_subtotal": 22.20,
                }
            ],
        )
