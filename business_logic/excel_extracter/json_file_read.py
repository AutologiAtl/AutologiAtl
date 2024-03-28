# main_class_script.py

from .MSC_excelFormat import MSCExcelWriter
from .ONE_excelFormat import ONEExcelWriter
from .SITC_excelFormat import SITCExcelWriter
from .COSCO_excelFormat import COSCOExcelWriter
from .INTERASIA_excelFormat import INTERASIAExcelWriter

import os
import json
from datetime import datetime
import xlwings as xw

class MainClass:

    def processJson(self, data):
        processed_data = {
            'Actual_Shipper': data.get('booking_conformation', {}).get('ActualShipper', '').replace('\n', ' '),
            'Booking_Number': data.get('booking_conformation', {}).get('BookingNumber', ''),
            'Vessel_No': data.get('booking_conformation', {}).get('Vessel_no', '').replace('\n', ' '),
            'Voyage_No': data.get('booking_conformation', {}).get('Voyage_no', '').replace('\n', ' '),
            'Shipping_Comp_Name': data.get('booking_conformation', {}).get('Shipping_comp_name', '').replace('\n', ' '),
            'Place_of_Receipt': data.get('booking_conformation', {}).get('PortOfReceipt', '').replace(',', ', '),
            'Port_of_Discharge': data.get('booking_conformation', {}).get('PortOfDischarge', '').replace(',', ', '),
            'Port_of_Loading': data.get('booking_conformation', {}).get('PortOfLoading', '').replace(',', ', '),
            'Place_of_Delivery': data.get('booking_conformation', {}).get('PlaceOfDelivery', '').replace(',', ', '),
            'B/L_Original': data.get('booking_conformation', {}).get('B/LOriginal', ''),
            'Freight_': data.get('booking_conformation', {}).get('Freight',''),
            'B/LPlaceOfIssue': data.get('booking_conformation', {}).get('B/LPlaceOfIssue',''),
            'shipper': data.get('booking_conformation', {}).get('shipper', ''),
            'consignee': data.get('booking_conformation', {}).get('consignee', ''),
            'notify': data.get('booking_conformation', {}).get('notify', ''),
        }
        return processed_data

    def copy_template_and_populate(self, template_path, output_folder, processed_data,downloded_excel_path,uploaded_excel_path):
        vassNAdbaou  = processed_data.get('Vessel_No', '')
        shipping_comp_name = processed_data.get('Shipping_Comp_Name', '')
        print("vassNAdbaou---------->>",vassNAdbaou)
        print("shipping_comp_name---------->>",shipping_comp_name)
        
        if 'Shipping_Comp_Name' in processed_data and 'MSC' in processed_data['Shipping_Comp_Name']:
            instance_variable = MSCExcelWriter()
            print("Run MSC File")
            try:
                new_file_name = instance_variable.write_to_excel(template_path, output_folder, processed_data,downloded_excel_path,uploaded_excel_path)
                print('Data written to Excel successfully.')
                return new_file_name
            except FileNotFoundError as e:
                print(f"Error FileNotFoundError : {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif processed_data.get('Shipping_Comp_Name', '') == 'ONE':
            instance_variable = ONEExcelWriter()
            print("Run ONE File")
            try:
                new_file_name = instance_variable.write_to_excel(template_path, output_folder, processed_data,downloded_excel_path,uploaded_excel_path)
                print('Data written to Excel successfully.')
                return new_file_name
            except FileNotFoundError as e:
                print(f"Error FileNotFoundError : {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif 'Shipping_Comp_Name' in processed_data and 'SITC' in processed_data['Shipping_Comp_Name']:
        # elif processed_data.get('Shipping_Comp_Name', '') == 'SITC CONTAINER LINES CO.,':
            instance_variable = SITCExcelWriter()
            print("Run SITC File")
            try:
                new_file_name = instance_variable.write_to_excel(template_path, output_folder, processed_data,downloded_excel_path,uploaded_excel_path)
                print('Data written to Excel successfully.')
                return new_file_name
            except FileNotFoundError as e:
                print(f"Error FileNotFoundError : {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif 'Shipping_Comp_Name' in processed_data and 'COSCO' in processed_data['Shipping_Comp_Name']:
        # elif processed_data.get('Shipping_Comp_Name', '') == 'SITC CONTAINER LINES CO.,':
            instance_variable = COSCOExcelWriter()
            print("Run COSCO File")
            try:
                new_file_name = instance_variable.write_to_excel(template_path, output_folder, processed_data,downloded_excel_path,uploaded_excel_path)
                print('Data written to Excel successfully.')
                return new_file_name
            except FileNotFoundError as e:
                print(f"Error FileNotFoundError : {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")


        elif 'Shipping_Comp_Name' in processed_data and 'IAL' in processed_data['Shipping_Comp_Name']:
        # elif processed_data.get('Shipping_Comp_Name', '') == 'SITC CONTAINER LINES CO.,':
            instance_variable = INTERASIAExcelWriter()
            print("Run COSCO File")
            try:
                new_file_name = instance_variable.write_to_excel(template_path, output_folder, processed_data,downloded_excel_path,uploaded_excel_path)
                print('Data written to Excel successfully.')
                return new_file_name
            except FileNotFoundError as e:
                print(f"Error FileNotFoundError : {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        else:
            print("FileNotFound error!!")