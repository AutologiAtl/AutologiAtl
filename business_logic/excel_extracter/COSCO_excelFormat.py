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
class COSCOExcelWriter:

    def calling_to_excel(self,processed_data, downloded_excel_path, uploaded_excel_path):
        try:
            consignee_from_pdf = processed_data.get('consignee', '')
            Notify_party_from_pdf = processed_data.get('notify', '')
            self.bl_issue_from_pdf = processed_data.get('B/LPlaceOfIssue', '')

            excel_processor = ExcelProcessor()
            self.df = excel_processor.process_all_excel_files(downloded_excel_path)
            excel_processor.copy_and_format_data(uploaded_excel_path)
            final_values = excel_processor.find_and_print_values('CONSIGNEE :','NOTIFY PARTY :','Shipper : ','Consignee : ', 'Notify : ','FREIGHT :','Vessel : ','B/L ISSUE BY :')
            excel_processor.extract_table_from_excel(uploaded_excel_path)

            try:
                if len(final_values) >= 3:
                    if len(final_values) >=3:
                        shiper_from_excel = final_values[0] if len(final_values) > 0 else None
                        consignee_from_excel = final_values[1] if len(final_values) > 0 else None
                        notify_party_from_excel = final_values[2] if len(final_values) > 0 else None
                        freight_from_excel = final_values[3] if len(final_values) > 0 else None
                        vessalNUMber_from_excel = final_values[4] if len(final_values) > 0 else None
                        bl_issue_from_excel = final_values[5] if len(final_values) > 0 else None
                    else:
                        # shiper_from_excel = final_values[0] if len(final_values) > 0 else None
                        consignee_from_excel = final_values[0] if len(final_values) > 0 else None
                        notify_party_from_excel = final_values[1] if len(final_values) > 0 else None
                        bl_issue_from_excel = final_values[2] if len(final_values) > 0 else None
                
                else:
                    print("Not enough values in final_values to create DataFrame.")
            except:
                pass
            
            
            if 'ACTUAL NAMEADDRESS' in consignee_from_pdf and 'SAME AS CONSIGNEE' in Notify_party_from_pdf:
                print(f"This condition is applied when the PDF document lacks shipper details and requires extraction from the Excel invoice sheet.-- {consignee_from_pdf} -- {Notify_party_from_pdf}")
                consignee = consignee_from_excel
                Notify_party = notify_party_from_excel
                bl_issue = bl_issue_from_excel
                return consignee, Notify_party, bl_issue
            
            else:
                if len(final_values) >=3:
                    return shiper_from_excel, consignee, Notify_party, bl_issue, freight_from_excel, vessalNUMber_from_excel
                
                else:
                    return consignee, Notify_party, bl_issue,

                # print(f"This condition applied when the docre pdf haveing the shiper details- \n\n{consignee_from_pdf} -- {Notify_party_from_pdf} -- {self.bl_issue_from_pdf}\n\n")  
                # shiper_from_excel = shiper_from_excel
                # consignee = consignee_from_excel
                # Notify_party = notify_party_from_excel
                # bl_issue = bl_issue_from_excel
                # freight = freight_from_excel
                # vessalNUMber_from_excel = vessalNUMber_from_excel

                # return consignee, Notify_party, bl_issue, freight, vessalNUMber_from_excel, shiper_from_excel

        except Exception as e:
            print(f"Error Exception in MSC excelfile: {e}")
            logging.basicConfig(filename='MSC.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.error(f'Here is the Error \n{traceback.print_exc()} \n\n Exception \n{e}')
            print("Created logfile...")
            return None, None, None
		
    def write_to_excel(self, template_path, output_folder, processed_data,downloded_excel_path,uploaded_excel_path):
        
        try:
            if template_path:
                template_path = template_path[0]
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@",template_path)
            try:
                consignee, Notify_party, bl_issue = self.calling_to_excel(processed_data, downloded_excel_path,uploaded_excel_path)
            except:
                consignee, Notify_party, bl_issue, freight, vessalNUMber_from_excel, shiper_from_excel = self.calling_to_excel(processed_data, downloded_excel_path,uploaded_excel_path)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("shiper_from_excel",shiper_from_excel)
                print("freight",freight)
                print("vessalNUMber",vessalNUMber_from_excel)


            print("consignee_from_excel",consignee)
            print("notify_party_from_excel",Notify_party)
            print("bl_issue_from_excel",bl_issue)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            # Extract relevant information from the processed data
            shipping_comp_name = processed_data.get('Shipping_Comp_Name', '')
            booking_number = processed_data.get('Booking_Number', 'UnknownBookingNo')
            vessel_and_voyage_no = processed_data.get('Vessel_No', 'Unknown')

            # Generate a timestamp
            timestamp = datetime.now().strftime("%Y%m%d")           
            print('temp---------->>',template_path)
            template_name = os.path.basename(template_path)
            booking_number = booking_number or 'UnknownBookingNo'
            new_file_name = f"DR-{shipping_comp_name}-{timestamp}-{vessel_and_voyage_no}-{booking_number}{os.path.splitext(template_name)[1]}"
            new_file_path = os.path.join(output_folder, new_file_name)

            # Copy template to the output folder with the new name
            shutil.copy(template_path, new_file_path)
            app = xw.App(visible=False)
            workbook = app.books.open(new_file_path)


            if actual_shipper_text is not None:	
                actual_shipper_text = processed_data['Actual_Shipper']
                workbook.sheets[0].range('A5').value = actual_shipper_text
            else:
                actual_shipper_text = processed_data['Actual_Shipper']
                workbook.sheets[0].range('A5').value = shiper_from_excel

            if consignee is not None:
                workbook.sheets[0].range('A13').value = consignee
                workbook.sheets[0].range('A13').api.WrapText = True
            else:
                workbook.sheets[0].range('A13').value = consignee
                workbook.sheets[0].range('A13').api.WrapText = True


            if Notify_party is not None:
                workbook.sheets[0].range('A20').value = Notify_party
                workbook.sheets[0].range('A20').api.WrapText = True
            else:
                workbook.sheets[0].range('A20').value = Notify_party
                workbook.sheets[0].range('A20').api.WrapText = True


            workbook.sheets[0].range('E65').value = bl_issue

            # Write Booking Number to cell K10
            workbook.sheets[0].range('F3').value = processed_data['Booking_Number']
            workbook.sheets[0].range('F5').value = processed_data['B/L_Original']
            workbook.sheets[0].range('A28').value = processed_data['Vessel_No'] +' '+ processed_data['Voyage_No']
            workbook.sheets[0].range('C28').value = processed_data['Port_of_Loading']
            workbook.sheets[0].range('C26').value = processed_data['Place_of_Receipt']
            workbook.sheets[0].range('A30').value = processed_data['Port_of_Discharge']
            workbook.sheets[0].range('C30').value = processed_data['Place_of_Delivery']
            workbook.sheets[0].range('D56').value = "Freight: "+ processed_data['Freight_']
            # workbook.sheets[0].range('P67').value = processed_data['B/L_Payble_At']
            print(f"Invoice df: {self.df}")
            self.write_sheet_2(workbook)
            workbook.save()

            print(f"File created: {new_file_path}")
            
            return new_file_name 

        except Exception as e:
            print(f"Error Exception in msc excelfile: {e}")
            traceback.print_exc()
            return None
        finally:
            workbook.close()
            app.quit()

    def write_sheet_2(self, workbook):

        #################### default df write into the excel sheet 1 ##################################################
        columns = list(self.df.columns) if not self.df.empty else []

        # Write column names in the first row
        for j, col in enumerate(columns):
            workbook.sheets[1].range(10, j+1).value = col

        # Write values horizontally for each row
        for i, row in self.df.iterrows():
            for j, col in enumerate(columns):
                workbook.sheets[1].range(i+12, j+1).value = row[col]

        last_row = workbook.sheets[1].range("A" + str(workbook.sheets[1].cells.last_cell.row)).end('up').row + 1  # Assuming the data starts from row 11

        last_row = last_row + 2
        print("last row >>>>>",last_row)


        # Merge cells A to E and write text
        workbook.sheets[1].range(f'A{last_row}:E{last_row}').merge()
        workbook.sheets[1].range(f'A{last_row}').value = "TOTAL WEIGHT AND M3"

        
        sum_formula = f'=SUM(G11:G{last_row - 1})'
        print('sum_formula',sum_formula)
        workbook.sheets[1].range(f'G{last_row}').formula = sum_formula
        workbook.sheets[1].range(f'G{last_row + 1}').value = "KG"
            

        # Sum values in column F
        sum_formula = f'=SUM(J11:J{last_row - 1})'
        workbook.sheets[1].range(f'J{last_row}').formula = sum_formula
        workbook.sheets[1].range(f'J{last_row +1}').value = "M3"

            