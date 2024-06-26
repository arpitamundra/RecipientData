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
    for voucher in root.findall('.//VOUCHER'):
        voucher_type = voucher.find('.//VOUCHERTYPENAME').text
        if voucher_type == 'Receipt':
            mix_date = voucher.find('DATE').text
            # mix_date = find_element(voucher, 'DATE')
            date = datetime.strptime(mix_date, "%Y%m%d").date()
            vch_type = voucher.find('VOUCHERTYPENAME').text
            vch_no = voucher.find('VOUCHERNUMBER').text
            debtor = voucher.find('PARTYLEDGERNAME').text
            transactions.append({'Date': date, 'transaction_type': "Parent", "Vch No.": vch_no, "Ref No.": "NA",
                                 "Ref Type": "NA", "Ref Date": "NA", "Debtor": debtor, "Ref Amount": "NA",
                                 'Amount': voucher.find('ALLLEDGERENTRIES.LIST/AMOUNT').text, "Particulars": debtor,
                                 "Vch Type": vch_type,
                                 "Amount Verified": "Yes"})

            for ledger_entry in voucher.findall('.//ALLLEDGERENTRIES.LIST'):
                ledger_name = ledger_entry.find('LEDGERNAME').text
                amount = ledger_entry.find('AMOUNT').text
                if ledger_name == debtor:
                    for allocation in ledger_entry.findall('BILLALLOCATIONS.LIST'):
                        transactions.append({'Date': date, 'transaction_type': "Child", "Vch No.": vch_no,
                                             "Ref No.": allocation.find('NAME').text,
                                             "Ref Type": allocation.find('BILLTYPE').text,
                                             "Ref Date": " ", "Debtor": ledger_name,
                                             "Ref Amount": allocation.find('AMOUNT').text,
                                             'Amount': "NA", "Particulars": ledger_name, "Vch Type": vch_type,
                                             "Amount Verified": "NA"})
            for ledger_entry in voucher.findall('.//ALLLEDGERENTRIES.LIST'):
                ledger_name = ledger_entry.find('LEDGERNAME').text
                amount = ledger_entry.find('AMOUNT').text
                if ledger_name != debtor:
                    transactions.append({'Date': date, 'transaction_type': "Other", "Vch No.": vch_no,
                                         "Ref No.": "NA",
                                         "Ref Type": "NA",
                                         "Ref Date": "NA", "Debtor": ledger_name, "Ref Amount": "NA",
                                         'Amount': amount, "Particulars": ledger_name, "Vch Type": vch_type,
                                         "Amount Verified": "NA"})

    return transactions

def create_spreadsheet(transactions, output_file):
    df = pd.DataFrame(transactions)
    df.to_excel(output_file, index=False)
    return HttpResponseRedirect(f"Spreadsheet created successfully at: {output_file}")

def success_view(request):
    return render(request, 'success.html')



