# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from pathlib import Path

import invoice2data

from odoo import tools

from .test_abstract import TestAbstract


class TestModule(TestAbstract):
    def setUp(self):
        super().setUp()

        # Load Templates
        self.local_templates_dir = str(
            Path(os.path.realpath(__file__)).parent / "templates"
        )
        tools.config["invoice2data_templates_dir"] = self.local_templates_dir

        self.templates = invoice2data.extract.loader.read_templates(
            self.local_templates_dir
        )
        self.pdf_folder_path = Path(os.path.realpath(__file__)).parent / "invoices"
        self.env["account.invoice2data.template"].init()
