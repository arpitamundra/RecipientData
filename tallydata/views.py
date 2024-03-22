from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import pandas as pd
import xml.etree.ElementTree as ET

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['file']
            transactions = parse_xml(xml_file)
            output_file = 'receipt.xlsx'
            create_spreadsheet(transactions, output_file)
            return redirect('success')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    transactions = []

    def find_element(parent, tag):
        element = parent.find(f".//{tag}")
        return element.text if element is not None else ''

    for voucher in root.findall('.//VOUCHER'):
        try:
            voucher_type = find_element(voucher, 'VOUCHERTYPENAME')
            if voucher_type == 'Receipt':
                mix_date = find_element(voucher, 'DATE')
                date = datetime.strptime(mix_date, "%Y%m%d").date()
                transaction_type = find_element(voucher, 'BANKALLOCATIONS.LIST/TRANSFERMODE')
                vch_no = find_element(voucher, 'VOUCHERNUMBER')
                ref_no = find_element(voucher, 'BANKALLOCATIONS.LIST/UNIQUEREFERENCENUMBER')
                ref_type = find_element(voucher, 'BILLALLOCATIONS.LIST/BILLTYPE')
                re_date = find_element(voucher, 'BANKALLOCATIONS.LIST/DATE')
                ref_date = datetime.strptime(re_date, "%Y%m%d").date()
                debtor = find_element(voucher, 'PARTYLEDGERNAME')
                ref_amount = find_element(voucher, 'BILLALLOCATIONS.LIST/AMOUNT')
                amount = find_element(voucher, 'ALLLEDGERENTRIES.LIST/AMOUNT')
                particulars = find_element(voucher, 'ALLLEDGERENTRIES.LIST/LEDGERNAME')
                vch_type = voucher_type
                amount_verified = find_element(voucher, 'ALLLEDGERENTRIES.LIST/AMOUNT')

                transactions.append(
                    {'Date': date, 'transaction_type': transaction_type, "Vch No.": vch_no, "Ref No.": ref_no,
                     "Ref Type": ref_type, "Ref Date": ref_date, "Debtor": debtor, "Ref Amount": ref_amount,
                     'Amount': amount, "Particulars": particulars, "Vch Type": vch_type,
                     "Amount Verified": amount_verified})
        except Exception as e:
            print(f"Error processing voucher: {e}")

    return transactions

def create_spreadsheet(transactions, output_file):
    df = pd.DataFrame(transactions)
    df.to_excel(output_file, index=False)
    return HttpResponseRedirect(f"Spreadsheet created successfully at: {output_file}")

def success_view(request):
    return render(request, 'success.html')



