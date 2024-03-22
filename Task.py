import xml.etree.ElementTree as ET
import pandas as pd
import os
from datetime import datetime
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    transactions = []

    for voucher in root.findall('.//VOUCHER'):
        try:
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
        except Exception as e:
            print(f"Error processing voucher: {e}")

    return transactions


def create_spreadsheet(transactions, output_file):
    df = pd.DataFrame(transactions)
    df.to_excel(output_file, index=False)
    print(f"Spreadsheet created successfully at: {output_file}")


def main():
    input_file = 'Input.xml'
    dir_path = '/Users/arpitamundra/Downloads'
    input_xml = os.path.join(dir_path, input_file)
    output_excel = 'output.xlsx'

    try:
        transactions = parse_xml(input_xml)
        create_spreadsheet(transactions, output_excel)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
