# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os

import invoice2data
from cryptography.fernet import Fernet

from odoo import tools
from odoo.tests.common import TransactionCase
from odoo.tools.float_utils import float_compare


class TestAbstract(TransactionCase):
    def setUp(self):
        super().setUp()

        self.invoice2data_key = tools.config.get("invoice2data_key", "")
        if not self.invoice2data_key:
            self.invoice2data_key = os.environ.get("INVOICE2DATA_KEY", "")
        if not self.invoice2data_key:
            raise Exception(
                "No invoice2data_key defined in odoo.cfg or environ variables"
            )
        self.invoice2data_key = self.invoice2data_key and self.invoice2data_key.encode(
            "utf-8"
        )
        self.env.user.company_id = self.env.ref(
            "account_invoice_invoice2data.invoice2data_company"
        )

    def _get_invoice_path(self, invoice_file_name):
        invoice_path = self.pdf_folder_path / invoice_file_name
        invoice_path_encrypted = self.pdf_folder_path / (
            invoice_file_name + ".encrypted"
        )
        if invoice_path.exists() and invoice_path_encrypted.exists():
            return invoice_path

        elif not invoice_path.exists() and not invoice_path_encrypted.exists():
            raise Exception("%s file doesn't exist" % invoice_path)

        fernet = Fernet(self.invoice2data_key)
        if invoice_path.exists() and not invoice_path_encrypted.exists():
            # we encrypt the pdf to put it on the CI
            with open(invoice_path, "rb") as file:
                file_data = file.read()
                encrypted_data = fernet.encrypt(file_data)
            with open(invoice_path_encrypted, "wb") as file:
                file.write(encrypted_data)

        elif not invoice_path.exists() and invoice_path_encrypted.exists():
            # we decrypt the pdf to extract the data
            with open(invoice_path_encrypted, "rb") as file:
                file_data = file.read()
                decrypted_data = fernet.decrypt(file_data)
            with open(invoice_path, "wb") as file:
                file.write(decrypted_data)

        return invoice_path

    def _test_supplier_template(
        self,
        invoice_file_name,
        line_qty,
        expected_values,
        expected_lines,
    ):
        invoice_path = self._get_invoice_path(invoice_file_name)
        result = invoice2data.main.extract_data(
            str(invoice_path), templates=self.templates
        )

        # check for the main values
        for key, expected_value in expected_values.items():
            self.assertEqual(
                result.get(key, False),
                expected_value,
                "The value of %s is %s. expected %s"
                % (key, result.get(key, False), expected_value),
            )

        # Check that all the lines has been found
        self.assertEqual(
            len(result["lines"]),
            line_qty,
            "Expected Lines : %d ; Lines Found : %d" % (line_qty, len(result["lines"])),
        )

        # check that total amount untaxed is correct
        if not result.get("fuzzy_total_amount_untaxed", False):
            lines_total = sum([x["price_subtotal"] for x in result["lines"]])
            extra_amounts_total = sum(
                {x: y for x, y in result.items() if "amount_extra_" in x}.values()
            )

            self.assertEqual(
                float_compare(
                    lines_total + extra_amounts_total,
                    result["amount_untaxed"],
                    precision_digits=2,
                ),
                0,
                "The total untaxed of the invoice %s is "
                "different than the sum of lines total (%s) and extra amount %s "
                % (result["amount_untaxed"], lines_total, extra_amounts_total),
            )

            # check detailed vat untaxed amount, if specified
            vat_code_000 = result.get("vat_code_000")
            vat_code_055 = result.get("vat_code_055")
            vat_code_200 = result.get("vat_code_200")
            lines_total_000 = extra_amounts_total_000 = 0.0
            lines_total_055 = extra_amounts_total_055 = 0.0
            lines_total_200 = extra_amounts_total_200 = 0.0

            for line in result["lines"]:
                if line.get("vat_code") == vat_code_000:
                    lines_total_000 += line["price_subtotal"]
                elif line.get("vat_code") == vat_code_055:
                    lines_total_055 += line["price_subtotal"]
                elif line.get("vat_code") == vat_code_200:
                    lines_total_200 += line["price_subtotal"]
            for k, v in result.items():
                if "amount_extra_" not in k:
                    continue
                if k.endswith("_000"):
                    extra_amounts_total_000 += v
                if k.endswith("_055"):
                    extra_amounts_total_055 += v
                if k.endswith("_200"):
                    extra_amounts_total_200 += v

            if "amount_untaxed_000" in result:
                self.assertEqual(
                    float_compare(
                        lines_total_000 + extra_amounts_total_000,
                        result["amount_untaxed_000"],
                        precision_digits=2,
                    ),
                    0,
                    "The total untaxed (VAT 0.0) of the invoice %s is "
                    "different than %s (sum sum of lines total (%s) and extra amount %s "
                    % (
                        result["amount_untaxed_000"],
                        lines_total_000 + extra_amounts_total_000,
                        lines_total_000,
                        extra_amounts_total_000,
                    ),
                )
            if "amount_untaxed_055" in result:
                self.assertEqual(
                    float_compare(
                        lines_total_055 + extra_amounts_total_055,
                        result["amount_untaxed_055"],
                        precision_digits=2,
                    ),
                    0,
                    "The total untaxed (VAT 5.5) of the invoice %s is "
                    "different than %s (sum sum of lines total (%s) and extra amount %s "
                    % (
                        result["amount_untaxed_055"],
                        lines_total_055 + extra_amounts_total_055,
                        lines_total_055,
                        extra_amounts_total_055,
                    ),
                )
            if "amount_untaxed_200" in result:
                self.assertEqual(
                    float_compare(
                        lines_total_200 + extra_amounts_total_200,
                        result["amount_untaxed_200"],
                        precision_digits=2,
                    ),
                    0,
                    "The total untaxed (VAT 20.0) of the invoice %s is "
                    "different than %s (sum of lines total (%s) and extra amount %s)"
                    % (
                        result["amount_untaxed_200"],
                        lines_total_200 + extra_amounts_total_200,
                        lines_total_200,
                        extra_amounts_total_200,
                    ),
                )

        # check for expected detailled lines
        for expected_line in expected_lines:
            line_found = False
            for real_line in result["lines"]:
                line_found = line_found or all(
                    [
                        real_line.get(key, False) == expected_line[key]
                        for key in expected_line.keys()
                    ]
                )

            self.assertTrue(
                line_found,
                "The following data has not been found %s\n"
                "===========\n"
                "%s"
                "===========\n" % (str(expected_line), str(result)),
            )
