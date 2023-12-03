# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Invoice - Invoice2data import (GRAP)",
    "version": "12.0.1.0.12",
    "category": "Accounting",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-business-supplier-invoice",
    "license": "AGPL-3",
    "depends": [
        "account",
        # OCA
        "account_invoice_recompute_tax",
        "account_invoice_supplier_ref_unique",
        "account_invoice_triple_discount",
        "purchase_discount",
        "purchase_triple_discount",
        "web_notify",
        "web_tree_dynamic_colored_field",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/wizard_invoice2data_import.xml",
        "views/view_account_invoice.xml",
        "views/view_account_invoice2data_template.xml",
    ],
    "external_dependencies": {
        "python": ["invoice2data", "jaro"],
        "deb": ["tesseract-ocr", "poppler-utils", "imagemagick"],
    },
    "demo": [
        "demo/res_groups.xml",
        "demo/uom_uom.xml",
        "demo/res_company.xml",
        "demo/account_account.xml",
        "demo/ir_property.xml",
        "demo/account_journal.xml",
        "demo/res_partner.xml",
        "demo/account_tax_group.xml",
        "demo/account_tax.xml",
        "demo/product_product.xml",
        "demo/account_invoice.xml",
    ],
    "installable": True,
}
