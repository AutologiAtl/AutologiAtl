from http import client
import os
import sys
from django.conf import settings
import pdfplumber
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from .PDFExtractor import PDFExtractor

import os

# Accessing the value of MY_SETTING
my_setting_value = settings.MY_SETTING

# Now you can use my_setting_value in your code
print(f"my_setting_value \n\n{my_setting_value} \n\n")


# file separator added instead of hard coding '/' or '\'
sep = os.path.sep



class Main_Class():

    def __init__(self, cl_name, booking_Customer_name ,files , file2):
        self.cl_name = cl_name
        self.booking_Customer_name = booking_Customer_name
        self.files = files
        self.file2 = file2
        self.path = os.getcwd()
        self.df = ''
        self.df1 = ''

    def main_function(self):
        masho_pdf = self.files
    
        # download_pdf_path = os.path.join(self.path, 'business_logic', 'media')
        download_pdf_path = os.path.join(self.path,'media','uploads')
        pdf_file_path = os.path.join(download_pdf_path, masho_pdf)

        Booking_conf_pdf = self.file2

        if Booking_conf_pdf is not None:
            print("booking_conformation_pdf=================>>", Booking_conf_pdf)
            second_pdf_file_path = os.path.join(download_pdf_path, Booking_conf_pdf.name)
            pdf_extractor = PDFExtractor(self.cl_name, self.booking_Customer_name, second_pdf_file_path)
            pdf_extractor.extract_pdf_coordinates()

            with open(second_pdf_file_path, 'wb') as destination:
                for chunk in Booking_conf_pdf.chunks():
                    destination.write(chunk)
        else:
            print("Booking_conf_pdf is None. Unable to create PDFExtractor instance.")

        print("pdfs--------->>>>",pdf_file_path)

        # Update the PDF_FILE_PATH in PDFExtractor with the new file path
        pdf_extractor.PDF_FILE_PATH = pdf_file_path
        images, filepath_test = pdf_extractor.pdf_to_images()
        print("filepath_test",filepath_test)
        # cropped_img = pdf_extractor.image_crop(filepath_test[2])

        # Create a DataFrame outside the loop to hold the extracted data
        columns = ['Registration_no', 'Registration_date', 'First_registration_date', 'Makers_serial_no', 'Trade_maker_vehicle',
                'Engine_model', 'Name_address', 'use', 'purpose', 'type_of_body', 'fixed_no', 'maxim_carry', 'weight',
                'gweight', 'engine_capacity', 'fuel', 'length', 'width', 'height', 'export_schedule_day', 'mileage']
        df_list = []

        image_folder = self.path + f"{sep}static{sep}images"
        for filename in os.listdir(image_folder):

            if my_setting_value == 'ON':

                if filename.startswith("page_") and filename.endswith(".png") and (filename!="page_1.png" and filename!="page_2.png"):
                    print(filename)
                    im =  os.path.join(image_folder, filename)

                    Registration_no = PDFExtractor.crop_image(12, 190, 400, 250, im)
                    Registration_no.save(image_folder + "/Crpd_Imgs/Registration_no.png")
                    ext_Registration_no = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/Registration_no.png")
                    
                    Registration_date = PDFExtractor.crop_image(444, 205, 762, 247, im)
                    Registration_date.save(image_folder + "/Crpd_Imgs/Registration_date.png")
                    ext_Registration_date = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/Registration_date.png")

                    First_registration_date = PDFExtractor.crop_image(760, 207, 1076, 242, im)
                    First_registration_date.save(image_folder + "/Crpd_Imgs/First_registration_date.png")
                    ext_First_registration_date = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/First_registration_date.png")

                    Makers_serial_no = PDFExtractor.crop_image(1078,190,1750,238, im)
                    Makers_serial_no.save(image_folder + "/Crpd_Imgs/Makers_serial_no.png")
                    ext_Makers_serial_no = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/Makers_serial_no.png")

                    Trade_maker_vehicle = PDFExtractor.crop_image(12, 279, 860, 334, im)
                    Trade_maker_vehicle.save(image_folder + "/Crpd_Imgs/Trade_maker_vehicle.png")
                    ext_Trade_maker_vehicle = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/Trade_maker_vehicle.png")

                    Engine_model = PDFExtractor.crop_image(1380, 266, 1750, 326, im)
                    Engine_model.save(image_folder + "/Crpd_Imgs/Engine_model.png")
                    ext_Engine_model = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/Engine_model.png")

                    Name_address = PDFExtractor.crop_image(234, 326, 1750, 445, im)
                    Name_address.save(image_folder + "/Crpd_Imgs/Name_address.png")
                    ext_Name_address = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/Name_address.png")

                    use = PDFExtractor.crop_image(230, 670, 320, 730, im)
                    use.save(image_folder + "/Crpd_Imgs/use.png")
                    ext_use = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/use.png")

                    purpose = PDFExtractor.crop_image(320, 670, 470, 729, im)
                    purpose.save(image_folder + "/Crpd_Imgs/purpose.png")
                    ext_purpose = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/purpose.png")

                    type_of_body = PDFExtractor.crop_image(470, 670, 860, 730, im)
                    type_of_body.save(image_folder + "/Crpd_Imgs/type_of_body.png")
                    ext_type_of_body = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/type_of_body.png")

                    fixed_no = PDFExtractor.crop_image(1050, 665, 1210, 725, im)
                    fixed_no.save(image_folder + "/Crpd_Imgs/fixed_no.png")
                    ext_fixed_no = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/fixed_no.png")

                    maxim_carry = PDFExtractor.crop_image(1314, 670, 1400, 720, im)
                    maxim_carry.save(image_folder + "/Crpd_Imgs/maxim_carry.png")
                    ext_maxim_carry = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/maxim_carry.png")
                    
                    weight = PDFExtractor.crop_image(1400, 670, 1528, 720, im)
                    weight.save(image_folder + "/Crpd_Imgs/weight.png")
                    ext_weight = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/weight.png")

                    gweight = PDFExtractor.crop_image(1525, 670, 1750, 720, im)
                    gweight.save(image_folder + "/Crpd_Imgs/gweight.png")
                    ext_gweight = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/gweight.png")

                    engine_capacity = PDFExtractor.crop_image(12, 785, 260, 840, im)
                    engine_capacity.save(image_folder + "/Crpd_Imgs/engine_capacity.png")
                    ext_engine_capacity = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/engine_capacity.png")

                    fuel = PDFExtractor.crop_image(260, 785, 550, 880, im)
                    fuel.save(image_folder + "/Crpd_Imgs/fuel.png")
                    ext_fuel = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/fuel.png")

                    length = PDFExtractor.crop_image(900, 800, 1110, 870, im)
                    length.save(image_folder + "/Crpd_Imgs/length.png")
                    ext_length = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/length.png")

                    width = PDFExtractor.crop_image(1203, 860, 1350, 930, im)
                    width.save(image_folder + "/Crpd_Imgs/width.png")
                    ext_width = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/width.png")

                    height = PDFExtractor.crop_image(1352, 860, 1490, 922, im)
                    height.save(image_folder + "/Crpd_Imgs/height.png")
                    ext_height = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/height.png")

                    export_schedule_day = PDFExtractor.crop_image(490, 920, 984, 995, im)
                    export_schedule_day.save(image_folder + "/Crpd_Imgs/export_schedule_day.png")
                    ext_export_schedule_day = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/export_schedule_day.png")

                    mileage = PDFExtractor.crop_image(1038, 995, 1340, 1042, im)
                    mileage.save(image_folder + "/Crpd_Imgs/mileage.png")
                    ext_mileage = PDFExtractor.extract_text_from_image(image_folder + "/Crpd_Imgs/mileage.png")

                    # Create a dictionary with the extracted data
                    data = {
                            "Registration_no": ext_Registration_no,
                            "Registration_date": ext_Registration_date,
                            "First_registration_date": ext_First_registration_date,
                            "Makers_serial_no": ext_Makers_serial_no,
                            "Trade_maker_vehicle": ext_Trade_maker_vehicle,
                            "Engine_model": ext_Engine_model,
                            "Name_address": ext_Name_address,
                            "use": ext_use,
                            "purpose": ext_purpose,
                            "type_of_body": ext_type_of_body ,
                            "fixed_no": ext_fixed_no,
                            "maxim_carry": ext_maxim_carry,
                            "weight": ext_weight,
                            "gweight": ext_gweight,
                            "engine_capacity": ext_engine_capacity,
                            "fuel": ext_fuel,
                            "length": ext_length,
                            "width": ext_width,
                            "height": ext_height,
                            "export_schedule_day": ext_export_schedule_day,
                            "mileage": ext_mileage,
                            }
                    
                    # Append the data to the list of dataframes
                    df_list.append(pd.DataFrame(data, index=[1]))

                    
            else:
                # Create a dictionary with the extracted data
                data = {
                        "Registration_no": None,
                        "Registration_date": None,
                        "First_registration_date": None,
                        "Makers_serial_no": None,
                        "Trade_maker_vehicle": None,
                        "Engine_model": None,
                        "Name_address": None,
                        "use": None,
                        "purpose": None,
                        "type_of_body": None ,
                        "fixed_no": None,
                        "maxim_carry": None,
                        "weight": None,
                        "gweight": None,
                        "engine_capacity": None,
                        "fuel": None,
                        "length": None,
                        "width": None,
                        "height": None,
                        "export_schedule_day": None,
                        "mileage": None,
                        }

                
                # Append the data to the list of dataframes
                df_list.append(pd.DataFrame(data, index=[1]))

        # Concatenate the list of dataframes into a single dataframe
        self.df = pd.concat(df_list, ignore_index=False)


        # Save the DataFrame to an Excel file
        # OUTPUT_DIRECTORY1 = path +"/fileupload/business_logic/OUTPUT_Files/Masho_Text_Extracted.xlsx"
        # self.df.to_excel(OUTPUT_DIRECTORY1, index=True)



        #----------- MULTI PAGE PDF EXTRACTION -----------
        # with pdfplumber.open(pdf_file_path) as pdf:
        # with pdfplumber.open(pdf_extractor.PDF_FILE_PATH) as pdf:
        #     text = ""
        #     for page in pdf.pages:
        #         text += page.extract_text()


        # #----------- Print or process the extracted text -----------
        # print(text)



        # #----------- SPLITTING TEXT BY SPACE " " -----------
        # a = text.split('\n')
        # a


        # #----------- EXTRACT DATA FROM 'FINAL DESTINATION' TILL TABLE END (TABLE DATA BASICALLY) -----------

        # # Your data
        # text_data = text
        # # Define a regular expression pattern
        # pattern = re.compile(r'DESTINATION :(.+?)SHIPPING FROM :', re.DOTALL)

        # # Use the pattern to find the match in the text data
        # match = pattern.search(text_data)

        # # Extract the matched content
        # if match:
        #     destination_data = match.group(1).split('\n')
        #     print("Destination Data:")
        #     print(destination_data)
        # else:
        #     print("Pattern not found in the text data.")

        # #----------- TO CHECK DATA IN DESTINATION_DATA -----------
        # destination_data

        # #----------- TO CHECK DATA IN MAIN_TABLE_DATA (AFTER 'DUBLIN' TILL 'TOTAL') -----------
        # main_table_data = destination_data[1:-1]


        # #----------- Split each element of each item with space -----------
        # split_data = [item.split() for item in main_table_data]

        # # Check and merge 4th and 5th index if the 5th index has alphabets
        # for i in range(1, len(split_data)):
        #     if any(c.isalpha() for c in split_data[i][4]):
        #         split_data[i][3] = f'{split_data[i][3]} {split_data[i][4]}'
        #         split_data[i].pop(4)

        # # Print the result
        # for row in split_data[1:-1]:
        #     print(row)

        # print(len(row))



        # #----------- CREATING LISTS TO SAVE DATA IN DATA FRAME -----------
        # sno = []
        # year = []
        # maker = []
        # name = []
        # rec_no_list = []
        # chassis_no_list = []
        # weight_list = []
        # length_list = []
        # width_list = []
        # height_list = []
        # meas_list = []
        # # disp_list = []
        # # fuel_list = []
        # # category_list = []
        # # seat_list = []
        # # cf_list = []
        # engine_power_list = []



        # #----------- REMOVE GAP B/W '1400' AND 'CC' MAKING IT 1 ENTRY ('1400 CC') + TRANSFERRING VALUES TO LISTS -----------
        # for s in split_data[1:-1]:
        #     s[-2] = ' '.join([s[-2], s[-1]])  # Join the last two elements with a space
        #     s.pop()  # Remove the last element
        #     print(s)
        #     sno.append(s[0])
        #     year.append(s[1])
        #     maker.append(s[2])
        #     name.append(s[3])
        #     rec_no_list.append(s[4])
        #     chassis_no_list.append(s[5])
        #     weight_list.append(s[6])
        #     length_list.append(s[7])
        #     width_list.append(s[8])
        #     height_list.append(s[9])
        #     meas_list.append(s[10])
        #     # disp_list.append(s[11])
        #     # fuel_list.append(s[12])
        #     # if len(s)>16:
        #     #     category_list.append(s[13])
        #     #     seat_list.append(s[14])
        #     #     cf_list.append(s[15])
        #     #     engine_power_list.append(s[16])
            
        #     # seat_list.append(s[13])
        #     # cf_list.append(s[14])
        #     engine_power_list.append(s[15])



        # # Creating a DataFrame and saving it to Excel
        # self.df_1 = pd.DataFrame({
        #     "S.No.": sno,
        #     "Year": year,
        #     "Maker": maker,
        #     "Name": name,
        #     "Recno.": rec_no_list,
        #     "Chassis No.": chassis_no_list,
        #     "Weight": weight_list,
        #     "Length": length_list,
        #     "Width": width_list,
        #     "Height": height_list,
        #     "MEAS": meas_list,
        #     # "DISP": disp_list,
        #     # "Fuel": fuel_list,
        #     # "Category": " ",
        #     # "Seat": seat_list,
        #     # "C/F": cf_list,
        #     "Engine Power": engine_power_list
        # })


        # excel_file_name = f"{self.cl_name}_MarineServ_Table.xlsx"
        # # excel_file_path = os.path.join(PDFExtractor.OUTPUT_DIRECTORY, excel_file_name)

        # # self.df_1.to_excel(excel_file_path, index=False)

        # print("\n")
        # print(f"Excel file '{excel_file_name}' created!")



# if __name__ == "__main__":
    
#     client_name = sys.argv[1]
#     main = Main_Class(client_name)
#     main.main_function()
#     print('---------')