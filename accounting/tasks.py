from http.client import HTTPResponse

from django.shortcuts import redirect
from .models import *

def import_data_from_saft(mysaft, itemProfitRate):
   
   # Add and Update Items (products)
    for item in mysaft["products"]:
        try:
            existingItem = Item.objects.get(code=item['ProductCode'])
            existingItem.code = item['ProductCode']
            existingItem.description = item['ProductDescription']
            existingItem.pvp = item['UnitPrice']
            existingItem.tax = item['TaxPercentage']
            existingItem.cost = round(
                (
                    float(item['UnitPrice'])
                    *  # Item Profit Rate is a percentage Ex: 30% so we have to divide it by 100
                    (1 - float(itemProfitRate) / 100)),
                2)
            existingItem.save()
        except Item.DoesNotExist:
            existingItem = Item()
            existingItem.code = item['ProductCode']
            existingItem.description = item['ProductDescription']
            existingItem.pvp = item['UnitPrice']
            existingItem.tax = item['TaxPercentage']
            existingItem.cost = round(
                (
                    float(item['UnitPrice'])
                    *  # Item Profit Rate is a percentage Ex: 30% so we have to divide it by 100
                    (1 - float(itemProfitRate) / 100)),
                2)
            existingItem.save()

    # Add and Update Clients
    for client in mysaft["clients"]:
        try:
            existingCustomer = Customer.objects.get(
                customerID=client["CustomerID"])
            existingCustomer.name = client["CompanyName"]
            existingCustomer.address = client["BillingAddress"][
                "AddressDetail"]
            existingCustomer.city = client["BillingAddress"]["City"]
            existingCustomer.zipCode = client["BillingAddress"]["PostalCode"]
            existingCustomer.country = client["BillingAddress"]["Country"]
            existingCustomer.taxNumber = client["CustomerTaxID"]
            existingCustomer.save()
        except Customer.DoesNotExist:
            existingCustomer = Customer(customerID=client["CustomerID"])
            existingCustomer.name = client['CompanyName']
            existingCustomer.address = client["BillingAddress"][
                "AddressDetail"]
            existingCustomer.city = client["BillingAddress"]["City"]
            existingCustomer.zipCode = client["BillingAddress"]["PostalCode"]
            existingCustomer.country = client["BillingAddress"]["Country"]
            existingCustomer.taxNumber = client["CustomerTaxID"]
            existingCustomer.save()


# Add and Update Invoices
    for invoice in mysaft["invoices"]:
        if invoice['InvoiceType'] != "FS":
            continue
        try:
            existingInvoice = Invoice.objects.get(
                docNumber=invoice["InvoiceNo"])
            existingInvoice.customer = Customer.objects.get(
                customerID=invoice["CustomerID"])
            existingInvoice.date = invoice["InvoiceDate"]
            existingInvoice.tax = invoice["DocumentTotals"]["TaxPayable"]
            existingInvoice.netTotal = invoice["DocumentTotals"]["NetTotal"]
            existingInvoice.grossTotal = invoice["DocumentTotals"][
                "GrossTotal"]

            for item in invoice["items"]:
                newItemOutput = ItemOutput()
                newItemOutput.date = invoice["InvoiceDate"]
                newItemOutput.item = Item.objects.get(code=item["ProductCode"])
                newItemOutput.tax = item["Tax"]["TaxPercentage"]
                newItemOutput.cost = item["UnitPrice"]
                newItemOutput.quantity = item["Quantity"]
                #newItemOutput.input =
                #newItemOutput.warehouse =
                newInvoiceItem = InvoiceItem()
                newInvoiceItem.invoice = existingInvoice
                newInvoiceItem.output = newItemOutput
                existingInvoice.save()
                newItemOutput.save()
                newInvoiceItem.save()
        except Invoice.DoesNotExist:
            existingInvoice = Invoice(docNumber=invoice["InvoiceNo"])
            existingInvoice.customer = Customer.objects.get(
                customerID=invoice["CustomerID"])
            existingInvoice.date = invoice["InvoiceDate"]
            existingInvoice.tax = invoice["DocumentTotals"]["TaxPayable"]
            existingInvoice.netTotal = invoice["DocumentTotals"]["NetTotal"]
            existingInvoice.grossTotal = invoice["DocumentTotals"][
                "GrossTotal"]

            for item in invoice["items"]:
                newItemOutput = ItemOutput()
                newItemOutput.date = invoice["InvoiceDate"]
                newItemOutput.item = Item.objects.get(code=item["ProductCode"])
                newItemOutput.tax = item["Tax"]["TaxPercentage"]
                newItemOutput.cost = item["UnitPrice"]
                newItemOutput.quantity = item["Quantity"]
                #newItemOutput.input =
                #newItemOutput.warehouse =
                newInvoiceItem = InvoiceItem()
                newInvoiceItem.invoice = existingInvoice
                newInvoiceItem.output = newItemOutput
                existingInvoice.save()
                newItemOutput.save()
                newInvoiceItem.save()

