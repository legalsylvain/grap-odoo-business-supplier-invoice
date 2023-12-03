# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test_module import TestModule


class TestFermeBioMargerie(TestModule):
    def test_ferme_bio_margerie(self):
        self._test_supplier_template(
            "ferme-bio-margerie__2023-01-27__GAE__FA018307.pdf",
            line_qty=6,
            expected_values={
                "issuer": "Ferme Bio Margerie",
                "date": datetime(day=27, month=1, year=2023),
                "date_due": datetime(day=12, month=2, year=2023),
                "invoice_number": "FA018307",
                "amount_untaxed": 155.64,
                "amount": 164.20,
            },
            expected_lines=[
                {
                    "product_code": "JUBOAA000",
                    "product_name": "JUS POMME AB MARG 1L",
                    "vat_code": "5.5%",
                    "quantity": 30,
                    "price_unit": 2.31,
                    "price_subtotal": 69.30,
                },
                {
                    "product_code": "JUBOAA005",
                    "product_name": "JUS POMME AB MARG 25CL",
                    "vat_code": "5.5%",
                    "quantity": 12,
                    "price_unit": 1.26,
                    "price_subtotal": 15.12,
                },
            ],
        )
