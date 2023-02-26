The module analyse the PDF using ``invoice2data`` python library.
(https://github.com/invoice-x/invoice2data)


**To develop a template for a new supplier**

1. put the PDF in the folder ``./account_invoice_invoice2data_templates/tests/invoices``
   with the name ``supplier-name__date-invoice__invoice-number.pdf``

2. create a new test in ``./account_invoice_invoice2data_templates/tests/``
   named ``test_supplier_name.pdf``

3. create a new template in ``./account_invoice_invoice2data_templates/templates/``
   named ``supplier_name.yml``

To test your template :

``invoice2data --exclude-built-in-templates --template-folder=./account_invoice_invoice2data_templates/templates/ ./account_invoice_invoice2data_templates/tests/invoices/supplier-name__date-invoice__invoice-number.pdf``

Note :

Use ``--debug`` if you want to have the text extracted from the pdf.
You can then test your regular expression with https://regex101.com/.

**Regex Attention**

When you write the 'lines' regex, be careful that writing a multi lines regex in the
yaml file create implicite space for each return to the line :

.. code-block:: yaml

    line: ^(?P<product_code>\d+)
      (?P<product_name>.*)

is equivalent to

.. code-block:: yaml

    line: ^(?P<product_code>\d+)\s(?P<product_name>.*)

**Regex Common Pattern**

* Float quantity : ``\d+\.\d+`` ; exemple : ``47.53``
* Price with space delimiter : ``[\d\s?]+\.\d+`` ; exemple : ``1 422.99``
* Long date format : ``\d{2}/\d{2}/\d{4}`` ; exemple : ``22/04/1982``
* Short date format : ``\d{2}/\d{2}/\d{2}`` ; exemple : ``22/04/82``
