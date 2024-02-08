# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from pathlib import Path

import yaml

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)


class AccountInvoice2dataTemplate(models.Model):
    _name = "account.invoice2data.template"
    _description = "Template for invoice2data Supplier Invoices"
    _order = "name"

    name = fields.Char(required=True, index=True, readonly=True)

    version = fields.Integer(required=True, default=1, readonly=True)

    vat = fields.Char(string="Supplier Vat Number", readonly=True)

    vat_values = fields.Char(readonly=True)

    file_name = fields.Char(readonly=True)

    json_content = fields.Text(readonly=True)

    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "unique_name",
            "unique(name, version)",
            "Name and version should be unique for invoice2data templates.",
        ),
        (
            "unique_file_name",
            "unique(file_name)",
            "File name should be unique for invoice2data templates.",
        ),
        (
            "unique_vat",
            "unique(vat, version)",
            "Vat Number and verison should be unique for invoice2data templates.",
        ),
    ]

    invoice_ids = fields.One2many(
        comodel_name="account.invoice",
        inverse_name="invoice2data_template_id",
    )

    invoice_qty = fields.Integer(
        string="Invoices Quantity",
        compute="_compute_invoice_qty_multi",
    )

    invoice_line_qty = fields.Integer(
        string="Invoice Lines Quantity",
        compute="_compute_invoice_qty_multi",
    )

    # Compute Section
    @api.depends("invoice_ids")
    def _compute_invoice_qty_multi(self):
        for template in self:
            template.invoice_qty = len(template.invoice_ids)
            template.invoice_line_qty = len(
                template.mapped("invoice_ids.invoice_line_ids")
            )

    # Core Section
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

        files = []
        for file in sorted(local_templates_path.iterdir()):
            if file.name.endswith(".yml") and not file.name.startswith("_"):
                files.append(file)

        self._update_templates(files)

    # Custom Section
    def _update_templates(self, files):

        up_to_date_template_ids = []
        existing_templates = self.with_context(active_test=False).search([])

        # Create new templates, or update existing ones
        for file in files:
            stream = open(str(file), "r")
            try:
                _logger.info("Parsing '%s' supplier template file." % file.name)
                yaml_vals = yaml.safe_load(stream)

            except yaml.YAMLError:
                _logger.error(
                    "Unable to parse correctly %s supplier template file." % file.name
                )
                continue

            template_vals = self._prepare_template(file, yaml_vals)
            existing_template = existing_templates.filtered(
                lambda x: x.file_name == template_vals["file_name"]
            )

            if existing_template:
                existing_template.write(template_vals)
                up_to_date_template_ids.append(existing_template.id)
            else:
                new_template = self.create(template_vals)
                existing_templates |= new_template
                up_to_date_template_ids.append(new_template.id)

        # Unlink obsolete templates
        self.search(
            [("id", "not in", up_to_date_template_ids), ("file_name", "!=", False)]
        ).unlink()

    def _prepare_template(self, file, yaml_vals):
        vat_values_list = [
            str(float(k.replace("vat_code_", "")) / 10) + "%"
            for k in yaml_vals["fields"].keys()
            if k.startswith("vat_code_")
        ]
        return {
            "name": yaml_vals.get("issuer"),
            "version": int(yaml_vals.get("version", "1")),
            "vat": yaml_vals.get("fields").get("vat", {}).get("value"),
            "file_name": file.name,
            "json_content": str(yaml_vals),
            "vat_values": " - ".join(vat_values_list),
        }
