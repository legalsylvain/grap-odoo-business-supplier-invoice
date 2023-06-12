# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re

from psycopg2.extensions import AsIs

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare
from odoo.tools.misc import formatLang

from odoo.addons import decimal_precision as dp


class WizardInvoice2dataImportLine(models.TransientModel):
    _name = "wizard.invoice2data.import.line"
    _description = "Wizard Line to import Bill invoices via invoice2data"

    sequence = fields.Integer(
        string="#", readonly=True, help="Line number in the pdf invoice."
    )

    wizard_id = fields.Many2one(comodel_name="wizard.invoice2data.import")

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="wizard_id.invoice_id.currency_id",
        readonly=True,
    )

    product_id = fields.Many2one(comodel_name="product.product")

    invoice_line_id = fields.Many2one(
        comodel_name="account.invoice.line", readonly=True
    )

    is_product_mapped = fields.Boolean(readonly=True)

    pdf_product_code = fields.Char(readonly=True)

    pdf_product_name = fields.Char(readonly=True)

    pdf_quantity = fields.Float(
        readonly=True, digits=dp.get_precision("Product Unit of Measure")
    )

    pdf_price_unit = fields.Monetary(currency_field="currency_id", readonly=True)

    pdf_price_subtotal = fields.Monetary(currency_field="currency_id", readonly=True)

    pdf_discount = fields.Float(readonly=True)

    pdf_discount2 = fields.Float(readonly=True)

    pdf_vat_amount = fields.Float(readonly=True)

    data = fields.Text(readonly=True)

    has_changes = fields.Boolean(
        compute="_compute_change_description",
        store=True,
    )
    changes_description = fields.Text(
        compute="_compute_change_description",
        store=True,
    )

    current_uom_id = fields.Many2one(
        string="current UoM",
        comodel_name="uom.uom",
        related="invoice_line_id.uom_id",
        readonly=True,
    )

    new_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="New UoM",
    )

    @api.depends(
        "invoice_line_id",
        "invoice_line_id.quantity",
        "pdf_quantity",
        "invoice_line_id.price_unit",
        "pdf_price_unit",
        "invoice_line_id.discount",
        "pdf_discount",
        "invoice_line_id.discount2",
        "pdf_discount2",
        "current_uom_id",
        "new_uom_id",
    )
    def _compute_change_description(self):
        for line in self:
            invoice_line = line.invoice_line_id
            changes = []
            if not invoice_line:
                changes.append(_("New Line Creation"))
            else:
                changes = [x["description"] for x in line._analyse_differences()]

            line.changes_description = changes and "\n".join(changes) or ""
            line.has_changes = bool(changes)

    def _analyse_differences(self):
        self.ensure_one()
        changes = []
        invoice_line = self.invoice_line_id
        if float_compare(
            invoice_line.quantity,
            self.pdf_quantity,
            precision_digits=dp.get_precision("Product Unit of Measure")(self.env.cr)[
                1
            ],
        ):
            changes.append(
                {
                    "field_name": "quantity",
                    "name": _("Quantity"),
                    "current_value": invoice_line.quantity,
                    "new_value": self.pdf_quantity,
                }
            )

        if float_compare(
            invoice_line.price_unit,
            self.pdf_price_unit,
            precision_digits=self.currency_id.decimal_places,
        ):
            changes.append(
                {
                    "field_name": "price_unit",
                    "name": _("Unit Price"),
                    "current_value": invoice_line.price_unit,
                    "new_value": self.pdf_price_unit,
                    "format_lang": True,
                }
            )

        if float_compare(
            invoice_line.discount,
            self.pdf_discount,
            precision_digits=dp.get_precision("Discount")(self.env.cr)[1],
        ):
            changes.append(
                {
                    "field_name": "discount",
                    "name": _("Discount"),
                    "current_value": invoice_line.discount,
                    "new_value": self.pdf_discount,
                    "suffix": "%",
                }
            )

        if float_compare(
            invoice_line.discount2,
            self.pdf_discount2,
            precision_digits=dp.get_precision("Discount")(self.env.cr)[1],
        ):
            changes.append(
                {
                    "field_name": "discount2",
                    "name": _("Discount n°2"),
                    "current_value": invoice_line.discount2,
                    "new_value": self.pdf_discount2,
                    "suffix": "%",
                }
            )

        if invoice_line.uom_id != self.new_uom_id:
            changes.append(
                {
                    "field_name": "uom_id",
                    "name": _("UoM"),
                    "current_value": invoice_line.uom_id,
                    "new_value": self.new_uom_id,
                    "many2one": True,
                }
            )

        for change in changes:
            if change.get("format_lang"):
                current_value_text = formatLang(
                    self.env, change["current_value"], currency_obj=self.currency_id
                )
                new_value_text = formatLang(
                    self.env, change["new_value"], currency_obj=self.currency_id
                )
            elif change.get("many2one"):
                current_value_text = change["current_value"].name
                new_value_text = change["new_value"].name
            else:
                current_value_text = change["current_value"]
                new_value_text = change["new_value"]
            change["description"] = _("%s : %s%s -> %s%s") % (
                change["name"],
                current_value_text,
                change.get("suffix", ""),
                new_value_text,
                change.get("suffix", ""),
            )
        return changes

    @api.model
    def _guess_product(self, partner, line_data):
        """
        Guess the product given a partner and a dict with product_code
        and product_name.
        If defined, the search will be done by product_code,
        Otherwise, the search will be done by product_name that is
        in that case, required.
        An error is raised if 0 or many products are found.

        Parameters
        ----------
            partner : res.partner
                Current supplier
            line_data : dict
                {'product_code': 'xxx', 'product_name': 'yyy'}
        """

        products = self.env["product.product"]
        product_code = line_data.get("product_code", False)
        if product_code:
            # Search supplierinfo by product_code
            # regex pattern for removing leading zeros from an input string
            regexPattern = "^0+(?!$)"
            clean_product_code = re.sub(regexPattern, "", product_code)
            # Search for productinfo
            self.env.cr.execute(
                """
                SELECT id
                FROM product_supplierinfo
                WHERE name = %s
                AND product_code SIMILAR TO '0*%s'
                """,
                (
                    partner.id,
                    AsIs(clean_product_code),
                ),
            )
            supplierinfo_ids = self.env.cr.fetchall()

            supplierinfos = self.env["product.supplierinfo"].search(
                [("id", "in", supplierinfo_ids)]
            )
        elif line_data.get("product_name", False):
            # Search supplierinfo by product_name
            supplierinfos = self.env["product.supplierinfo"].search(
                [
                    ("product_name", "=", line_data["product_name"]),
                    ("name", "=", partner.id),
                ]
            )
        else:
            raise UserError(
                _("Unable to search product without product code neither product name.")
            )

        products = supplierinfos.filtered(lambda x: x.product_id).mapped("product_id")

        products |= supplierinfos.filtered(lambda x: not x.product_id).mapped(
            "product_tmpl_id.product_variant_ids"
        )

        if len(products) > 1:
            raise UserError(
                _("Many products found for the supplier %s and the code '%s'. \n - %s")
                % (
                    partner.name,
                    product_code,
                    "\n - ".join(products.mapped("display_name")),
                )
            )
        return products and products[0]

    @api.model
    def _get_extra_products(self):
        return {
            "amount_extra_energy_cost_055": {
                "product_code": "ENERGY055",
                "product_name": _("Contribution to Additional Energy Costs (5,5%)"),
                "vat_amount": 5.5,
            },
            "amount_extra_energy_cost_200": {
                "product_code": "ENERGY200",
                "product_name": _("Contribution to Additional Energy Costs (20,0%)"),
                "vat_amount": 20.0,
            },
            "amount_extra_shipping_costs_200": {
                "product_code": "PORT",
                "product_name": _("Shipping Cost"),
                "vat_amount": 20.0,
            },
            "amount_extra_fuel_surcharge_200": {
                "product_code": "CARBURANT",
                "product_name": _("Fuel Surcharge"),
                "vat_amount": 20.0,
            },
            "amount_extra_parafiscal_tax_interfel_200": {
                "product_code": "TPF",
                "product_name": _("Taxe Interfel TPF"),
                "vat_amount": 20.0,
            },
            "amount_extra_trade_discount_055": {
                "product_code": "TRADE-DISC-05.5",
                "product_name": _("Trade Discount on products with 05.5% VAT"),
                "vat_amount": 5.5,
            },
            "amount_extra_trade_discount_200": {
                "product_code": "TRADE-DISC-20.0",
                "product_name": _("Trade Discount on products with 20.0% VAT"),
                "vat_amount": 20.0,
            },
        }

    @api.model
    def _get_vat_amount(self, wizard, pdf_data, line_data):
        if not wizard.pdf_has_vat_mapping:
            return False
        pdf_vat_code = line_data["vat_code"]
        vat_mapping = {
            vat_code: vat_name
            for vat_name, vat_code in pdf_data.items()
            if vat_name.startswith("vat_code_")
        }
        vat_name = vat_mapping.get(pdf_vat_code, False)
        if not vat_name:
            raise UserError(_("Unable to map the vat code '%s'") % (pdf_vat_code))
        return float(vat_name.replace("vat_code_", "")) / 10

    @api.model
    def _prepare_from_pdf_data(self, wizard, pdf_data):
        result = []
        sequence = 0
        # Create regular product lines
        for line_data in pdf_data["lines"]:
            sequence += 1
            product = self._guess_product(wizard.partner_id, line_data)
            quantity = line_data["quantity"]
            if line_data.get("quantity2"):
                quantity *= line_data["quantity2"]
            result.append(
                {
                    "sequence": sequence,
                    "wizard_id": wizard.id,
                    "is_product_mapped": bool(product),
                    "product_id": product and product.id,
                    "pdf_product_code": line_data.get("product_code", False),
                    "pdf_product_name": line_data["product_name"],
                    "pdf_vat_amount": self._get_vat_amount(wizard, pdf_data, line_data),
                    "pdf_quantity": quantity,
                    "pdf_price_unit": line_data["price_unit"],
                    "pdf_price_subtotal": line_data.get("price_subtotal", 0.0),
                    "pdf_discount": line_data.get("discount", 0.0),
                    "pdf_discount2": line_data.get("discount2", 0.0),
                    "data": str(line_data),
                }
            )
        for key, value in self._get_extra_products().items():
            if key in pdf_data.keys():
                sequence += 1
                product = self._guess_product(wizard.partner_id, value)
                result.append(
                    {
                        "sequence": sequence,
                        "wizard_id": wizard.id,
                        "is_product_mapped": bool(product),
                        "product_id": product and product.id,
                        "pdf_product_code": value["product_code"],
                        "pdf_product_name": value["product_name"],
                        "pdf_vat_amount": value["vat_amount"],
                        "pdf_quantity": 1,
                        "pdf_price_unit": pdf_data[key],
                        "pdf_price_subtotal": pdf_data[key],
                        "pdf_discount": 0.0,
                        "pdf_discount2": 0.0,
                        "data": str(pdf_data[key]),
                    }
                )
        return result

    def _create_or_update_supplierinfos(self):
        for line in self.filtered(lambda x: not x.is_product_mapped and x.product_id):
            supplierinfos = self.env["product.supplierinfo"].search(
                [
                    ("name", "=", line.wizard_id.partner_id.id),
                    ("product_tmpl_id", "=", line.product_id.product_tmpl_id.id),
                ]
            )
            if len(supplierinfos) == 0:
                self.env["product.supplierinfo"].create(
                    {
                        "name": line.wizard_id.partner_id.id,
                        "product_tmpl_id": line.product_id.product_tmpl_id.id,
                        "product_id": (
                            line.product_id.product_tmpl_id.product_variant_count > 1
                        )
                        and line.product_id.id,
                        "product_code": line.pdf_product_code,
                        "product_name": line.pdf_product_name,
                        "price": line.pdf_price_unit,
                        "discount": line.pdf_discount,
                        "discount2": line.pdf_discount2,
                    }
                )
            elif len(supplierinfos) == 1:
                supplierinfos.write(
                    {
                        "product_code": line.pdf_product_code,
                        "product_name": line.pdf_product_name,
                    }
                )
            else:
                raise UserError(
                    _(
                        "Unimplemented feature : Product %s is still related many times"
                        " with the supplier %s.\n"
                        " Please update manually the information on the product form view."
                    )
                    % (line.product_id.complete_name, line.wizard_id.partner_id.name)
                )
            line.is_product_mapped = True

    def _analyze_invoice_lines(self):
        mapped_invoice_line_ids = []
        for wizard_line in self:
            invoice_lines = wizard_line.wizard_id.invoice_id.invoice_line_ids.filtered(
                lambda x: x.product_id == wizard_line.product_id
                and x.id not in mapped_invoice_line_ids
            )
            if invoice_lines:
                mapped_invoice_line_ids.append(invoice_lines[0].id)
            wizard_line.write(
                {
                    "invoice_line_id": invoice_lines and invoice_lines[0].id or False,
                    "new_uom_id": invoice_lines
                    and invoice_lines[0].uom_id.id
                    or (wizard_line.product_id and wizard_line.product_id.uom_po_id.id)
                    or False,
                }
            )

    def _prepare_invoice_lines_vals(self):
        lines_vals = []
        for line in self:
            if line.invoice_line_id:
                vals = {}
                # Update an existing invoice line
                for change in line._analyse_differences():
                    if change.get("many2one"):
                        vals.update({change["field_name"]: change["new_value"].id})
                    else:
                        vals.update({change["field_name"]: change["new_value"]})

                if line.changes_description:
                    extra_text = _("[PDF analysis] %s") % (
                        " ; ".join(line.changes_description.split("\n"))
                    )
                    vals.update(
                        {"name": "%s\n%s" % (line.invoice_line_id.name, extra_text)}
                    )

                if line.invoice_line_id.sequence != line.sequence:
                    vals.update(
                        {
                            "sequence": line.sequence,
                        }
                    )

                if vals:
                    lines_vals.append((1, line.invoice_line_id.id, vals))
            else:
                # Create a new invoice line
                fiscal_position = line.wizard_id.invoice_id.fiscal_position_id
                account = self.env["account.invoice.line"].get_invoice_line_account(
                    "in_invoice",
                    line.product_id,
                    fiscal_position,
                    line.env.user.company_id,
                )
                taxes = fiscal_position.map_tax(
                    line.product_id.supplier_taxes_id,
                    line.product_id,
                    line.wizard_id.invoice_id.partner_id,
                )
                name = line.product_id.with_context(
                    partner_id=line.wizard_id.partner_id.id
                ).partner_ref
                if line.product_id.description_purchase:
                    name += "\n" + line.product_id.description_purchase
                vals = {
                    "sequence": line.sequence,
                    "product_id": line.product_id.id,
                    "name": name,
                    "origin": _("PDF Analysis"),
                    "account_id": account.id,
                    "quantity": line.pdf_quantity,
                    "price_unit": line.pdf_price_unit,
                    "uom_id": line.new_uom_id.id,
                    "discount": line.pdf_discount,
                    "discount2": line.pdf_discount2,
                    "invoice_line_tax_ids": [(6, 0, taxes.ids)],
                }
                lines_vals.append((0, 0, vals))

        return lines_vals
