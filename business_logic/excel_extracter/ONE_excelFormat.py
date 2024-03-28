import logging
import os
import shutil
import traceback
import xlwings as xw
from openpyxl import load_workbook
import os 
from datetime import datetime
import traceback
from .excel_extr_atl import ExcelProcessor

path = os.getcwd()
class ONEExcelWriter:
    def calling_to_excel(self,processed_data, downloded_excel_path, uploaded_excel_path):
        try:
            shipping_comp_name = processed_data.get('Shipping_Comp_Name', '')
            consignee_from_pdf = processed_data.get('consignee', '')
            Notify_party_from_pdf = processed_data.get('notify', '')
            bl_issue_from_pdf = processed_data.get('B/LPlaceOfIssue', '')
            print("!!!!!!!!!!!!!!@##@@@@@@@@@@@@@@@@@@!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print('consignee_from_pdf',consignee_from_pdf)
            print(Notify_party_from_pdf)
            print(bl_issue_from_pdf)
            print("!!!!!!!!!!!!!!!@@@@@@@@@@@@@@@@@@@@@@@!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            excel_processor = ExcelProcessor()
            self.df = excel_processor.process_all_excel_files(downloded_excel_path)
            excel_processor.copy_and_format_data(uploaded_excel_path,shipping_comp_name)
            BL_ISSUE_BY_values_h31, final_values = excel_processor.find_and_print_values('B/L ISSUE BY :', 'CONSIGNEE :', 'NOTIFY PARTY :')
            excel_processor.extract_table_from_excel(uploaded_excel_path)

            consignee_from_excel = final_values[0] if len(final_values) > 0 else None
            Notify_party_from_excel = final_values[1] if len(final_values) > 0 else None
            bl_issue_from_excel = BL_ISSUE_BY_values_h31[0] if len(BL_ISSUE_BY_values_h31) > 0 else None

            if 'ACTUAL NAMEADDRESS' in consignee_from_pdf and 'SAME AS CONSIGNEE' in Notify_party_from_pdf:
                print(f"This condition is applied when the PDF document lacks shipper details and requires extraction from the Excel invoice sheet.-- {consignee_from_pdf} -- {Notify_party_from_pdf}")
                consignee = consignee_from_excel
                Notify_party = Notify_party_from_excel
                bl_issue = bl_issue_from_excel
                return consignee, Notify_party, bl_issue
            else:
                print(f"This condition applied when the docre pdf haveing the shiper details- {consignee_from_pdf} -- {Notify_party_from_pdf} -- {bl_issue_from_pdf}")  
                consignee = consignee_from_pdf
                Notify_party = Notify_party_from_pdf
                bl_issue = bl_issue_from_pdf

                return consignee, Notify_party, bl_issue

        except Exception as e:
            print(f"Error Exception in ONE excelfile: {e}")
            logging.basicConfig(filename='ONE.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.error(f'Here is the ONE Error \n{traceback.print_exc()} \n\n Exception \n{e}')
            print("Created logfile...")
            return None, None, None

    def write_to_excel(self, template_path, output_folder, processed_data,downloded_excel_path,uploaded_excel_path):
        
        try:
            if template_path:
                template_path = template_path[0]
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@",template_path)
            consignee, Notify_party, bl_issue = self.calling_to_excel(processed_data, downloded_excel_path,uploaded_excel_path)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print('consignee',consignee)
            print(Notify_party)
            print(bl_issue)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            
            # Extract relevant information from the processed data
            shipping_comp_name = processed_data.get('Shipping_Comp_Name', '')
            booking_number = processed_data.get('Booking_Number', 'UnknownBookingNo')
            vessel_and_voyage_no = processed_data.get('Vessel_No', 'Unknown')

            # Generate a timestamp
            timestamp = datetime.now().strftime("%Y%m%d")
            # Create the new file name
            template_name = os.path.basename(template_path)
            booking_number = booking_number or 'UnknownBookingNo'
            new_file_name = f"DR-{shipping_comp_name}-{timestamp}-{vessel_and_voyage_no}-{booking_number}{os.path.splitext(template_name)[1]}"
            new_file_path = os.path.join(output_folder, new_file_name)

            # Copy template to the output folder with the new name
            shutil.copy(template_path, new_file_path)
            app = xw.App(visible=False)
            workbook = app.books.open(new_file_path)
            

            # Write Actual Shipper details with wrap text
            actual_shipper_text = processed_data['Actual_Shipper']
            workbook.sheets[1].range('A7').value = actual_shipper_text
            workbook.sheets[1].range('A7').api.WrapText = True

            # Write Consignee details with wrap text
            workbook.sheets[1].range('A19').value = consignee
            workbook.sheets[1].range('A19').api.WrapText = True

            # Write Notify Party details with wrap text
            workbook.sheets[1].range('A30').value = Notify_party
            workbook.sheets[1].range('A30').api.WrapText = True

            # Merge and center cells H31
            # workbook.sheets[0].range('J67:O67').merge()
            workbook.sheets[1].range('X87').value = bl_issue

            # Write Value to Respective cells
            workbook.sheets[1].range('Y7').value = processed_data['Booking_Number']
            workbook.sheets[1].range('AI87').value = processed_data['B/L_Original']
            workbook.sheets[1].range('A44').value = processed_data['Vessel_No']
            workbook.sheets[1].range('M44').value = processed_data['Port_of_Loading']
            workbook.sheets[1].range('M41').value = processed_data['Place_of_Receipt']
            workbook.sheets[1].range('A47').value = processed_data['Port_of_Discharge']
            workbook.sheets[1].range('M47').value = processed_data['Place_of_Delivery']
            workbook.sheets[1].range('N80').value = "Freight: "+ processed_data['Freight_']

            self.write_sheet_2(workbook)
            # Save and close the workbook
            workbook.save()

            print(f"File created: {new_file_path}")
            print(f"Invoice df: {self.df}")
            return new_file_name 

        except Exception as e:
            print(f"Error Exception in ONE excelfile: {e}")
            logging.basicConfig(filename='example1.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.error(f'Here is the ONE Error \n{traceback.print_exc()} \n\n{e}')
            print("Created logfile...")
            return None
        finally:
            workbook.close()
            app.quit()

    def write_sheet_2(self, workbook):
        
        # df = self.df.reset_index(drop=True)[['NO', 'YEAR', 'MAKER', 'NAME','CHASSIS NO', 'WEIGHT', 'LENGTH', 'WIDTH', 'HEIGHT', 'MEAS']]
        print("DATAFRAME in one_file ",self.df)

        # # Assuming the DataFrame has the same structure as the 'Invoice' list in json_
        # for i, row in df.iterrows():
        #     workbook.sheets[2].range(f'A{i+11}').value = row['NO']
        #     workbook.sheets[2].range(f'B{i+11}').value = row['YEAR']
        #     workbook.sheets[2].range(f'C{i+11}').value = row['MAKER']
        #     workbook.sheets[2].range(f'D{i+11}').value = row['NAME']
        #     workbook.sheets[2].range(f'E{i+11}').value = row['CHASSIS NO']
        #     workbook.sheets[2].range(f'F{i+11}').value = row['WEIGHT']
        #     workbook.sheets[2].range(f'G{i+11}').value = row['LENGTH']
        #     workbook.sheets[2].range(f'H{i+11}').value = row['WIDTH']
        #     workbook.sheets[2].range(f'I{i+11}').value = row['HEIGHT']
        #     workbook.sheets[2].range(f'J{i+11}').value = row['MEAS']

        columns = list(self.df.columns) if not self.df.empty else []

        # Write column names in the first row
        for j, col in enumerate(columns):
            workbook.sheets[2].range(10, j+1).value = col

        # Write values horizontally for each row
        for i, row in self.df.iterrows():
            for j, col in enumerate(columns):
                workbook.sheets[2].range(i+12, j+1).value = row[col]


        last_row = workbook.sheets[2].range("A" + str(workbook.sheets[2].cells.last_cell.row)).end('up').row + 1  # Assuming the data starts from row 11

        last_row = last_row + 2
        print("last row >>>>>",last_row)

        # Merge cells A to E and write text
        workbook.sheets[2].range(f'A{last_row}:E{last_row}').merge()
        workbook.sheets[2].range(f'A{last_row}').value = "TOTAL WEIGHT AND M3"

        # Sum values in column F
        sum_formula = f'=SUM(F11:F{last_row - 1})'
        workbook.sheets[2].range(f'F{last_row}').formula = sum_formula
        workbook.sheets[2].range(f'F{last_row + 1}').value = "KG"


        # Sum values in column F
        sum_formula = f'=SUM(J11:J{last_row - 1})'
        workbook.sheets[2].range(f'J{last_row}').formula = sum_formula
        workbook.sheets[2].range(f'J{last_row +1}').value = "M3"
            