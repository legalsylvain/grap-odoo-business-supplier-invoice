# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    # Fix Pural supplierinfo for HAL
    request = """
        UPDATE account_invoice2data_template
        SET file_name = replace(file_name, '-', '_')
        WHERE file_name ilike '%-%';
    """
    cr.execute(request)
