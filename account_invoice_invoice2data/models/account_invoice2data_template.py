# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from pathlib import Path

import yaml

from odoo import fields, models, tools

_logger = logging.getLogger(__name__)


class AccountInvoice2dataTemplate(models.Model):
    _name = "account.invoice2data.template"
    _description = "Template for invoice2data Supplier Invoices"

    name = fields.Char(required=True)

    vat = fields.Char(string="Supplier Vat Number")

    vat_values = fields.Char()

    file_name = fields.Char()

    json_content = fields.Text()

    _sql_constraints = [
        (
            "unique_file_name",
            "unique(file_name)",
            "File name should be unique for invoice2data templates.",
        ),
        (
            "unique_vat",
            "unique(vat)",
            "Vat Number should be unique for invoice2data templates.",
        ),
    ]

    def init(self):
        local_templates_dir = tools.config.get("invoice2data_templates_dir", False)

        if not local_templates_dir:
            _logger.error(
                "'invoice2data_templates_dir' not set in the odoo Config File"
            )
            return

        local_templates_path = Path(local_templates_dir)

        if not local_templates_path.exists():
            _logger.error("Path %s doesn't exist." % local_templates_path)
            return

        existing_templates = self.search([])
        for file in sorted(local_templates_path.iterdir()):
            if file.name.endswith(".yml") and not file.name.startswith("_"):
                stream = open(str(file), "r")
                try:
                    _logger.info("Parsing '%s' supplier template file." % file.name)
                    self._create_or_update_template(
                        file.name, yaml.safe_load(stream), existing_templates
                    )
                except yaml.YAMLError:
                    _logger.error(
                        "Unable to parse correctly %s supplier template file."
                        % file.name
                    )
                    continue

    def _prepare_template(self, file_name, yaml_vals):
        vat_values_list = [
            str(float(k.replace("vat_code_", "")) / 10) + "%"
            for k in yaml_vals["fields"].keys()
            if k.startswith("vat_code_")
        ]
        return {
            "name": yaml_vals.get("issuer"),
            "vat": yaml_vals.get("fields").get("vat", {}).get("value"),
            "file_name": file_name,
            "json_content": str(yaml_vals),
            "vat_values": " - ".join(vat_values_list),
        }

    def _create_or_update_template(self, file_name, yaml_vals, existing_templates):
        template_vals = self._prepare_template(file_name, yaml_vals)
        existing_template = existing_templates.filtered(
            lambda x: x.file_name == template_vals["file_name"]
        )

        if existing_template:
            existing_template.write(template_vals)
            return existing_template
        else:
            return self.create(template_vals)
