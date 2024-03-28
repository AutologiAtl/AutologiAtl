import io
import os
import sys
import json
import fitz
import pandas as pd
import pdfplumber
from PIL import Image 

from google.cloud import vision
from google.cloud.vision_v1 import types

import traceback
import os

path = os.getcwd()
sep = os.path.sep
class PDFExtractor:    

    def __init__(self, cl_name,booking_Customer_name,booking_conformation_pdf_path=None):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path +f"{sep}business_logic{sep}source_code{sep}json_files{sep}token{sep}VisionAPI_ServiceAccountToken.json"
        self.client = vision.ImageAnnotatorClient()
        self.cl_name = cl_name
        self.booking_Customer_name = booking_Customer_name
        self.booking_conformation_pdf = booking_conformation_pdf_path
        self.path = os.getcwd()

    
    # --------- FOR TABLE DATA EXTRACTION --------- WORKING !!!!!!
    def extract_pdf_coordinates(self):
        self.path = os.getcwd()
        if self.booking_conformation_pdf is not None:
            json_config_path = os.path.join(self.path,'business_logic', 'source_code', 'json_files', f'{self.booking_Customer_name}.json')
            json_config = json.load(open(json_config_path))
            booking_conformation_pdf = os.path.basename(self.booking_conformation_pdf)
            
            json_config['pdf_files'][0]['file_name'] = booking_conformation_pdf

            for pdf_info in json_config["pdf_files"]:
                print("MMMMMMMMMMMMpdf_infoMMMMMMMMMMMMM",pdf_info)
                pdf_file = pdf_info["file_name"]
                pdf_file_path = os.path.join(self.path, 'media','uploads', pdf_file)

                try:
                    labels = []
                    contents = []
                    try:
                        with pdfplumber.open(pdf_file_path) as pdf:
                            for area in pdf_info["coordinates"]:
                                label = area["label"]
                                x0, y0, x1, y1 = area["x0"], area["y0"], area["x1"], area["y1"]

                                if x0 < 0 or y0 < 0 or x1 > pdf.pages[0].width or y1 > pdf.pages[0].height:
                                    print(f"Error: Coordinates for '{label}' exceed page dimensions in {pdf_file}.")
                                    continue

                                content = pdf.pages[0].crop((x0, y0, x1, y1)).extract_text()
                                
                                labels.append(label)
                                contents.append(content)
                    except Exception as err:
                        print("No PDf Found in pdfextracter", err)
                        print("let's try it again")
                        with pdfplumber.open(pdf_file_path) as pdf:
                            for area in pdf_info["coordinates"]:
                                label = area["label"]
                                x0, y0, x1, y1 = area["x0"], area["y0"], area["x1"], area["y1"]

                                if x0 < 0 or y0 < 0 or x1 > pdf.pages[0].width or y1 > pdf.pages[0].height:
                                    print(f"Error: Coordinates for '{label}' exceed page dimensions in {pdf_file}.")
                                    continue

                                content = pdf.pages[0].crop((x0, y0, x1, y1)).extract_text()
                                
                                labels.append(label)
                                contents.append(content)

                    self.df = pd.DataFrame({"Label": labels, "Content": contents})
                    # self.df.to_csv('booking.csv', index=False)

                except FileNotFoundError as e:
                    print(f"Error: PDF file '{pdf_file}' not found, please check whether the file is in the same file directory.")
                    traceback.print_exc()

                except Exception as e:
                    print(f"Error processing PDF '{pdf_file}': {str(e)}")
                    traceback.print_exc()
        else:
            print(f"No PDF file processing : {str(e)}")
            traceback.print_exc()
            pass
    
    # --------- WORKING !!!!!!!!!!!
    #PDF PASS IMAGE RETURN


    def pdf_to_images(self):
        # Open the PDF file
        try:
            pdf_document = fitz.open(self.PDF_FILE_PATH)
        except Exception as e:
            print(f"Error:{e}")

        a =[]
        b = []
        # Iterate through each page
        for page_number in range(pdf_document.page_count):
            # Get the page
            page = pdf_document[page_number]

            # Get the pixel dimensions (DPI) of the page
            dpi = 600  # You can adjust this value based on your requirements

            # Get the image data
            image = page.get_pixmap(matrix=fitz.Matrix(dpi / 255, dpi / 255))
            # Convert the image data to a Pillow Image
            pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
            resized_image = pil_image.resize((1901, 1469))
            # Save the image to the specified folder
            image_file_name = path +f"{sep}static{sep}images"
            image_filename = f"{image_file_name}{sep}page_{page_number + 1}.png"
            # print("image_filename :- ",image_filename)
            pil_image.save(image_filename)
            # Open the image from the file path
            original_image = Image.open(image_filename)

            # Resize the image
            # resized_image = original_image.resize((1600,1200))
            a.append(resized_image)
            b.append(image_filename)
            # print(f"Page {page_number + 1} converted and saved as {image_filename}")

        # Close the PDF document
        pdf_document.close()

        return a,b

    def image_crop(self, file_name):
        filepath = file_name
        with io.open(filepath, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = self.client.text_detection(image=image, image_context={"language_hints": ["ja"]},)
        upper = response.text_annotations[0].bounding_poly.vertices[0].x
        left = response.text_annotations[0].bounding_poly.vertices[0].y
        im = Image.open(filepath)
        down = response.text_annotations[0].bounding_poly.vertices[2].y
        right = response.text_annotations[0].bounding_poly.vertices[2].x

        cropimg = (left, upper, right, down) 
        im_cropped = im.crop(cropimg)
        
        size = (1901, 1469)
        im_resized = im_cropped.resize(size)
        #im_resized.show()
        print("__________________________________++++++++++++++++++++=======>>>",im_resized.size)
        
        return im_resized

    @staticmethod
    def crop_image(left, top, right, bottom, image_path):

        # Open the image from the file path
        original_image = Image.open(image_path)        
        # Define the coordinates for cropping
        coordinates = (left, top, right, bottom)
        # Crop the image
        cropped_image = original_image.crop(coordinates)
        # cropped_image.save('cropped_image.png')
        return cropped_image

    def extract_text_from_image(image_path):
        # Instantiates a client
        client = vision.ImageAnnotatorClient()

        # Open the image from the file path
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        # Create a Vision API image object
        image = vision.Image(content=content)

        # Perform text detection
        response = client.text_detection(image=image, image_context={"language_hints": ["en","ja"]})

        # Extract text from all annotations
        texts = response.text_annotations


        # Check if there are text annotations
        if texts:
            # Extract the description (text) from the first annotation
            text = texts[0].description.replace('\n', ' ')
            print("Extracted Text:", text)
            return text
        else:
            print("No text detected.")

