# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    # Fix Pural supplierinfo for HAL
    request = """
        UPDATE product_supplierinfo
        SET product_code =
            split_part(product_code, '/', 1)
            || '/'
            || substring(split_part(product_code, '/', 2), 2)
        WHERE name = 11066
        AND product_code ilike '%/%'
        AND split_part(product_code, '/', 2) ilike '0%';
    """

    for _i in range(5):
        cr.execute(request)
