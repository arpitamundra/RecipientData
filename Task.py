import xml.etree.ElementTree as ET
import pandas as pd
import os

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    transactions = []
    def find_element(parent, tag):
        return parent.find(f".//{tag}").text if parent.find(f".//{tag}") is not None else ''

    for voucher in root.findall('.//VOUCHER'):
        voucher_type = voucher.find('.//VOUCHERTYPENAME').text
        if voucher_type == 'Receipt':
            date = find_element(voucher, 'DATE')
            transaction_type = find_element(voucher, 'BANKALLOCATIONS.LIST/TRANSFERMODE')
            vch_no = find_element(voucher, 'VOUCHERNUMBER')
            ref_no = find_element(voucher, 'BANKALLOCATIONS.LIST/UNIQUEREFERENCENUMBER')
            ref_type = find_element(voucher, 'BILLALLOCATIONS.LIST/BILLTYPE')
            ref_date = find_element(voucher, 'BANKALLOCATIONS.LIST/DATE')
            debtor = find_element(voucher, 'PARTYLEDGERNAME')
            ref_amount = find_element(voucher, 'BILLALLOCATIONS.LIST/AMOUNT')
            amount = find_element(voucher, 'ALLLEDGERENTRIES.LIST/AMOUNT')
            particulars = find_element(voucher, 'ALLLEDGERENTRIES.LIST/LEDGERNAME')
            vch_type = find_element(voucher, 'VOUCHERTYPENAME')
            amount_verified = find_element(voucher, 'ALLLEDGERENTRIES.LIST/AMOUNT')

            print(f"Date: {date}")
            print(f"Transaction Type: {transaction_type}")
            print(f"Vch No.: {vch_no}")
            print(f"Ref No.: {ref_no}")
            print(f"Ref Type: {ref_type}")
            print(f"Ref Date: {ref_date}")
            print(f"Debtor: {debtor}")
            print(f"Ref Amount: {ref_amount}")
            print(f"Amount: {amount}")
            print(f"Particulars: {particulars}")
            print(f"Vch Type: {vch_type}")
            print(f"Amount Verified: {amount_verified}")
            print()
            transactions.append({'Date': date, 'transaction_type': transaction_type,"Vch No.":vch_no,"Ref No.":ref_no,"Ref Type":ref_type,"Ref Date":ref_date,"Debtor":debtor,"Ref Amount":ref_amount, 'Amount': amount,"Particulars":particulars,"Vch Type":vch_type,"Amount Verified":amount_verified})

    return transactions


def create_spreadsheet(transactions, output_file):
    df = pd.DataFrame(transactions)
    df.to_excel(output_file, index=False)


def main():
    input_file = 'Input.xml'
    dir_path = '/Users/arpitamundra/Downloads'
    input_xml = os.path.join(dir_path, input_file)
    output_excel = 'output.xlsx'


    transactions = parse_xml(input_xml)

    create_spreadsheet(transactions, output_excel)
    print("Spreadsheet created successfully.")


if __name__ == "__main__":
    main()


import xml.etree.ElementTree as ET
import pandas as pd
import os

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    transactions = []
    def find_element(parent, tag):
        return parent.find(f".//{tag}").text if parent.find(f".//{tag}") is not None else ''

    for voucher in root.findall('.//VOUCHER'):
        voucher_type = voucher.find('.//VOUCHERTYPENAME').text
        if voucher_type == 'Receipt':
            date = find_element(voucher, 'DATE')
            transaction_type = find_element(voucher, 'BANKALLOCATIONS.LIST/TRANSFERMODE')
            vch_no = find_element(voucher, 'VOUCHERNUMBER')
            ref_no = find_element(voucher, 'BANKALLOCATIONS.LIST/UNIQUEREFERENCENUMBER')
            ref_type = find_element(voucher, 'BILLALLOCATIONS.LIST/BILLTYPE')
            ref_date = find_element(voucher, 'BANKALLOCATIONS.LIST/DATE')
            debtor = find_element(voucher, 'PARTYLEDGERNAME')
            ref_amount = find_element(voucher, 'BILLALLOCATIONS.LIST/AMOUNT')
            amount = find_element(voucher, 'ALLLEDGERENTRIES.LIST/AMOUNT')
            particulars = find_element(voucher, 'ALLLEDGERENTRIES.LIST/LEDGERNAME')
            vch_type = find_element(voucher, 'VOUCHERTYPENAME')
            amount_verified = find_element(voucher, 'ALLLEDGERENTRIES.LIST/AMOUNT')

            print(f"Date: {date}")
            print(f"Transaction Type: {transaction_type}")
            print(f"Vch No.: {vch_no}")
            print(f"Ref No.: {ref_no}")
            print(f"Ref Type: {ref_type}")
            print(f"Ref Date: {ref_date}")
            print(f"Debtor: {debtor}")
            print(f"Ref Amount: {ref_amount}")
            print(f"Amount: {amount}")
            print(f"Particulars: {particulars}")
            print(f"Vch Type: {vch_type}")
            print(f"Amount Verified: {amount_verified}")
            print()
            transactions.append({'Date': date, 'transaction_type': transaction_type,"Vch No.":vch_no,"Ref No.":ref_no,"Ref Type":ref_type,"Ref Date":ref_date,"Debtor":debtor,"Ref Amount":ref_amount, 'Amount': amount,"Particulars":particulars,"Vch Type":vch_type,"Amount Verified":amount_verified})

    return transactions


def create_spreadsheet(transactions, output_file):
    df = pd.DataFrame(transactions)
    df.to_excel(output_file, index=False)


def main():
    input_file = 'Input.xml'
    dir_path = '/Users/arpitamundra/Downloads'
    input_xml = os.path.join(dir_path, input_file)
    output_excel = 'output.xlsx'


    transactions = parse_xml(input_xml)

    create_spreadsheet(transactions, output_excel)
    print("Spreadsheet created successfully.")


if __name__ == "__main__":
    main()
