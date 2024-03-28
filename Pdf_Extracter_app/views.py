import os
import json
import re
import shutil
import psutil
import time
import traceback
import pandas as pd
from django.views import View
from urllib.parse import quote
from .models import *
from django.contrib import messages
from .forms import FileUploadForm,LoginForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from business_logic.source_code.main import Main_Class
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView as BaseLogoutView
from business_logic.source_code.PDFExtractor import PDFExtractor
from business_logic.excel_extracter.json_file_read import MainClass
from business_logic.excel_extracter.excel_extr_atl import ExcelProcessor
from django.http import FileResponse, HttpResponse, JsonResponse, HttpResponseBadRequest, StreamingHttpResponse
from django.conf import settings
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from django.core.paginator import Paginator



# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['docre']
collection = db['Pdf_Extracter_app_uploaduserdata']
submit_col = db['Pdf_Extracter_app_submituserinfo']
from datetime import datetime
created_date_utc = datetime.utcnow()
sep = os.path.sep
path = os.getcwd()

class LoginView(View):
    template_name = f'registration{sep}login.html'  # Your login template

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('file_upload')  # Redirect to a success page if the user is already authenticated
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form, 'error_message': None})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request,f'WELLCOME, {username}')
                return redirect('file_upload')  # Redirect to a success page
            else:
                # Authentication failed
                messages.error(request,'Invalid username or password! \nPlease try Again.')
                return render(request, self.template_name, {'form': form})
        else:
            # Form is not valid
            return render(request, self.template_name, {'form': form, 'error_message': 'Invalid form data'})

def logout_view(request):
    logout(request)
    messages.success(request,"Logout successfully")
    return redirect('login') # Redirect to the login page after logout

@method_decorator(login_required(login_url='login'), name='dispatch')
class FileUploadView(LoginRequiredMixin, View):
    template_name = f'fileupload{sep}home.html'

    def close_open_excel_files(self, directory):
        for proc in psutil.process_iter():
            try:
                files = proc.open_files()
                for f in files:
                    if directory in f.path:
                        proc.kill()
            except Exception:
                pass
    
    def get(self, request):
        form = FileUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        print("check data")
        form = FileUploadForm(request.POST, request.FILES)
        if form:
            icm = request.POST.get('form-select')
            icm1 = request.POST.get('form-select-sm')
            file1 = request.FILES.get('file1')
            file2 = request.FILES.get('file2')
            file3 = request.FILES.get('file3')

            data1 = {
                "id": ObjectId(),
                "user": str(request.user),
                "client": str(icm),
                "agent":str(icm1),
                "customFile": str(file1),
                "drFile": str(file2),
                "excelFile":str(file3)
            }
            collection.insert_one(data1)

            pdfs_All_files_paths = []
            pdfs_download_path = os.path.join(path, f'media','uploads')
            os.makedirs(pdfs_download_path, exist_ok=True)
            
            for file in request.FILES.getlist('file1'):
                pdf_file_path = os.path.join(pdfs_download_path, file.name)
                pdfs_All_files_paths.append(pdf_file_path)
                with open(pdf_file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

            excel_All_files_paths = []
            folder_format = "uploaded_{}"
            counter = 0

            while True:
                folder_name = folder_format.format(counter)
                excel_download_path = os.path.join(path, 'media', 'uploads', folder_name)
                if not os.path.exists(excel_download_path):
                    break
                counter += 1

            uploads_path = os.path.join(path, 'media', 'uploads')
            for folder in os.listdir(uploads_path):
                if folder.startswith('upload'):
                    folder_path = os.path.join(uploads_path, folder)
                    self.close_open_excel_files(folder_path)
                    # Remove the directory
                    shutil.rmtree(folder_path)

            # Create the directory again
            os.makedirs(excel_download_path, exist_ok=True)
            
            for file in request.FILES.getlist('file3'):
                excelfile_path = os.path.join(excel_download_path, file.name)
                excel_All_files_paths.append(excelfile_path)
                with open(excelfile_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                        
            print("multipe files",'\n',excel_All_files_paths)
            main = Main_Class(icm, icm1, pdf_file_path,file2)
            main.main_function()
            df1=main.df

            df1_dict = df1.to_dict(orient='records')
            df1_json = json.dumps(df1_dict)
            # Store the JSON strings in the session
            request.session['df1'] = df1_json
            request.session['excel_download_path'] = excel_download_path
            request.session['excelfile_path'] = excelfile_path
            
            pdf_file_path = str(pdf_file_path)
            file2 = str(file2.name)
            return redirect('view_files', icm=icm, icm1=icm1, excel_download_path=excel_download_path, file2=file2,df1_json=df1_json,excelfile_path=excelfile_path)
        else:
            return HttpResponseBadRequest("Form data is not valid.")



def view_files_view(request,icm,icm1,excel_download_path,file2,df1_json,excelfile_path):
    template_name = f'fileupload{sep}outputedit.html'

    booking_conformation_pdf_path = os.path.join(excel_download_path, file2)
    df1_json = df1_json
    df1_dict = json.loads(df1_json)
    df1 = pd.DataFrame(df1_dict)

    obj = PDFExtractor(icm, icm1, booking_conformation_pdf_path)
    obj.extract_pdf_coordinates()
    df2_ = obj.df

    try:
        instance_var1 = ExcelProcessor()
        df3 = instance_var1.process_all_excel_files(excel_download_path)
        instance_var1.copy_and_format_data(excelfile_path)
        final_values = instance_var1.find_and_print_values('CONSIGNEE :','NOTIFY PARTY :','Shipper : ','Consignee : ', 'Notify : ','FREIGHT :　','Vessel : ','B/L ISSUE BY :')
        instance_var1.extract_table_from_excel(excelfile_path)

        shiper_from_excel = final_values[0] if len(final_values) > 0 else None
        consignee_from_excel = final_values[1] if len(final_values) > 1 else None
        notify_party_from_excel = final_values[2] if len(final_values) > 2 else None

        if len(final_values) > 4:
            print("ABCDEFGHIJK<<<<<<<<<<<<<<<<<<<<<<<<<")
            labels = [
                'Actual Shipper', 'CONSIGNEE', 'NOTIFY', 'FREIGHT', 'Vessel Number', 'B/L PLACE OF ISSUE'
            ]
        elif len(final_values) <=4:
            print("ABCDEFGHIJKL>>>>>")
            labels = [
                'CONSIGNEE', 'NOTIFY', 'FREIGHT', 'B/L PLACE OF ISSUE'
            ]
        else:
            print("DONT HAVE ENOUGH DATA.........")

        print("Labels", labels)
        df_final_values = pd.DataFrame({"Label": labels[:len(final_values)], "Content": final_values})
        print(f"df_final_values \n{df_final_values}")

        df_2 = pd.DataFrame(df2_)
        df_concatenated = pd.concat([df_final_values, df_2])
        df_unique = df_concatenated.drop_duplicates(subset='Label', keep='first')
        print(f"combined_df \n{df_unique}")
        df2 = df_unique.to_dict(orient='records')
    except:
        df2 = df2_.to_dict(orient='records')
        pass

    image_paths = [            
        os.path.join(path + f"{sep}static{sep}images{sep}page_3.png"),            
        os.path.join(path + f"{sep}static{sep}images{sep}page_4.png"),            
        os.path.join(path + f"{sep}static{sep}images{sep}page_5.png"),
        os.path.join(path + f"{sep}static{sep}images{sep}page_6.png"),
        os.path.join(path + f"{sep}static{sep}images{sep}page_7.png"),
    ]

    df1 = df1.to_dict(orient='records')
    df3 = df3.to_dict(orient='records')
    columns = list(df3[0].keys()) if df3 else []

    new_list = []
    for index, item in enumerate(df1, start=1):
        new_dict = {'masho' + str(index): {
            'Registration no': item['Registration_no'],
            'Registration date': item['Registration_date'],
            'First registration date': item['First_registration_date'],
            'makers_serial_no': item['Makers_serial_no'],
            'trade_maker_vehicle': item['Trade_maker_vehicle'],
            'engine_model': item['Engine_model'],
            'name_address': item['Name_address'],
            'use': item['use'],
            'purpose': item['purpose'],
            'type_of_body': item['type_of_body'],
            'fixed_no': item['fixed_no'],
            'maxim_carry': item['maxim_carry'],
            'weight': item['weight'],
            'gweight': item['gweight'],
            'engine_capacity': item['engine_capacity'],
            'fuel': item['fuel'],
            'length': item['length'],
            'width': item['width'],
            'height': item['height'],
            'export_schedule_day': item['export_schedule_day'],
            'mileage': item['mileage'],
        }}
        new_list.append(new_dict)

    filtered_data = [entry for entry in new_list if all(value is not None for value in entry.values())]
    df1_html = json.dumps(filtered_data)

    result = os.path.basename(booking_conformation_pdf_path)
    context = {
        'media_file_path': result,
    }

    print("columns check",columns)
    print("context check",context)
    print("df3 check",df3)
    print("df2 check",df2)
    print("df1_html check",df1_html)

    return render(request, template_name, {'image_paths': image_paths, 'df1_html': df1_html,
                                            'df2_html': df2, 'df3_html': df3, 'columns':columns,
                                            'icm':icm, 'icm1':icm1, 'context':context
                                            })
                                                
@method_decorator(csrf_exempt, name='dispatch')
class AjaxSaveView(View):
    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                # Assuming the data is sent as JSON
                self.data = json.loads(request.body)

                print('Received data:', self.data)
                data = self.data.get('payload', {})
                request.session['data'] = data                
                j1 = json.dumps(data)
                parsed_data = json.loads(j1)
                try:
                    booking_comp_name = parsed_data['requestObject']['booking_comp_name']
                except Exception as e:
                    booking_comp_name = "missin data"

                try:
                    booking_number = parsed_data['requestObject']['booking_conformation']['BookingNumber']
                except Exception as e:
                    booking_number  = "missin data"  

                try:
                    shipping_comp_name = parsed_data['requestObject']['booking_conformation']['Shipping_comp_name']
                except Exception as e:
                    shipping_comp_name =  "missin data"    

                data2 = {
                        "id": ObjectId(),
                        "user": request.user.id,
                        "bookingCompany": str(booking_comp_name),
                        "shippingCompany":str(shipping_comp_name),
                        "bookingNo": booking_number,
                        "createdDate": created_date_utc
                }

                

                insert_result = submit_col.insert_one(data2)
                inserted_id = insert_result.inserted_id
                print("Inserted document ID:", inserted_id)

                request.session['data11'] = str(inserted_id) 

                response_data = {'status': 'success', 'message': 'Data saved successfully'}
                return JsonResponse(response_data)
            except json.JSONDecodeError as e:
                response_data = {'status': 'error', 'message': 'Invalid JSON data'}
                return JsonResponse(response_data, status=400)
        else:
            response_data = {'status': 'error', 'message': 'Invalid request'}
            return JsonResponse(response_data, status=400)
        
    def returnJsonData(self):
        data = self.data
        print("DATA_________ DATA ___________",data)
        return data


@method_decorator(login_required(login_url='login'), name='dispatch')
class MscExcelView(View):
    template_name = f'fileupload{sep}excel_file.html'

    def get(self, request, *args, **kwargs):
        try:
            time.sleep(3)
            json_dict = request.session.get('data')
            print(f'###################################### \n{json_dict}')

            print("######################################")
            if json_dict is not None:
                payload_dict = json_dict.get('requestObject', {})
            else:
                print("json_dict is None. Unable to retrieve payload.")
                payload_dict = {}

            json_data = json.dumps(payload_dict)
            json_data_dict = json.loads(json_data)
        except json.JSONDecodeError:
            return redirect('view_files')
        
        downloded_excel_path = request.session.get('excel_download_path')
        print("downloded_excel_path",downloded_excel_path)
        uploaded_excel_path = request.session.get('excelfile_path')

        template_folder = path + f"{sep}business_logic{sep}excel_extracter{sep}Templates"   

        # Access the 'payload' key
        instance_var = MainClass()
        processed_data = instance_var.processJson(json_data_dict)
        shipping_comp_name = processed_data.get('Shipping_Comp_Name', '')
        print(shipping_comp_name)
        excel_file_keyword = shipping_comp_name.replace(" ",'')
        template_files = os.listdir(template_folder)
        matching_file_paths = []
        template_excel_path_ = []

        for file in template_files:            
            target_prefix = excel_file_keyword.lower()[:3]
            if target_prefix in file.lower() and file.lower().endswith(".xlsx"):
                matching_file_path = os.path.join(template_folder, file)
                matching_file_paths.append(matching_file_path)
            
        if matching_file_paths:
            print(f"Matching Excel files found:")
            for temp_pass in matching_file_paths:
                template_excel_path_.append(temp_pass)
                print('temp_pass00000000000005555666443321111111111111',temp_pass)
        else:
            print(f"No Excel files found in '{template_folder}' with '{excel_file_keyword}' in their names.")

        template_excel_path = template_excel_path_
        output_folder_path = path + f"{sep}business_logic{sep}excel_extracter{sep}Excel_output_files"


        print("check path",output_folder_path)

        os.makedirs(output_folder_path, exist_ok=True)
        new_file_name = instance_var.copy_template_and_populate(template_excel_path, output_folder_path, processed_data,downloded_excel_path,uploaded_excel_path)
        print("new file",new_file_name)
        request.session['new_file_name'] = new_file_name


        # filter = {"_id": ObjectId(request.session['data11'])}
        # update = {"$set": {"fileName": str(output_folder_path) +  "\"  + new_file_name}}
        # update_result = submit_col.update_one(filter, update)

        filter = {"_id": ObjectId(request.session['data11'])}
        file_path = os.path.join(output_folder_path, new_file_name)
        update = {"$set": {"filepath": str(file_path),"filename":new_file_name[17:],"fullname":new_file_name}}
        update_result = submit_col.update_one(filter, update)

        return render(request, self.template_name, {'message': 'Data processed successfully','new_file_name':new_file_name})

@method_decorator(login_required(login_url='login'), name='dispatch')
class ExcelDownloadView(View):
    template_name = f'fileupload{sep}excel_file.html'

    def get(self, request, *args, **kwargs):
        mediador = request.session.get('icm1')
        new_file_name = request.session.get('new_file_name')
        excel_file_path = os.path.join(path, 'business_logic', 'excel_extracter', 'Excel_output_files', new_file_name)
        try:
            if os.path.exists(excel_file_path):
                with open(excel_file_path, 'rb') as excel_file:
                    excel_file_name = os.path.basename(excel_file_path)
                    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    response['Content-Disposition'] = f'attachment; filename="{quote(excel_file_name)}"'
                    return response
            else:
                return render(request, self.template_name, {'excel_file_name': excel_file_name})
        except Exception as err:
            if os.path.exists(excel_file_path):
                with open(excel_file_path, 'rb') as excel_file:
                    excel_file_name = os.path.basename(excel_file_path)
                    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    response['Content-Disposition'] = f'attachment; filename="{quote(excel_file_name)}"'
                    return response
            else:
                return render(request, self.template_name, {'excel_file_name': excel_file_name})

        finally:
            self.move_files(new_file_name, mediador)
            print("Move Files Successfully:")

    def file_iterator(self, file_path, chunk_size=8192):
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def move_files(self,filename,mediador):
        
        try:
            pattern = r'-(\w+)\.xlsx$'
            # Use re.search to find the match in the filename
            match = re.search(pattern, filename)
            if match:
                booking_number = match.group(1)
                print("Booking Number:move ", booking_number)
            else:
                print("Booking number not found in the filename.")

            booking_number = booking_number
            old_name = 'uploads'
            mediator = mediador
            source_folder = path + f'{sep}media{sep}uploads'
            destination_folder = path + f'{sep}business_logic{sep}UPLOAD_Files'
            destination_folder = f'{destination_folder}{sep}{mediator}{sep}{booking_number}'
            os.makedirs(destination_folder, exist_ok=True)

            for filename in os.listdir(source_folder):
                source_file = os.path.join(source_folder, filename)
                destination_file = os.path.join(destination_folder, filename)
                shutil.move(source_file, destination_file)

            print(f"All files from '{source_folder}' moved to '{destination_folder}' successfully!")
        except Exception as e:
            print(f"Error moving files: {e}")

def download_file(request):
    # Path to the file you want to download
    excel_file_path = os.path.join(path, 'business_logic', 'excel_extracter', 'Excel_output_files', 'DR-MSC(JAPAN)K.K.-20240208-VESSEL MSC MONTEREYVOY HI407A-EBKG07870938.xlsx')
    print("!@!!!!!!!!!!!!!!@@@@@@@@@@@@@@!9999999999999",excel_file_path)

    # Open the file
    with open(excel_file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="excel_file.xlsx"'
        return response


def my_view(request):
    return render(request, 'my_template.html')


@method_decorator(login_required(login_url='login'), name='dispatch') 
class FileListView(View):
    template_name = f'fileupload{sep}list_view.html'
    paginate_by = 10  # Number of records per page
    def get(self, request, *args, **kwargs):
        all_data_cursor = submit_col.find()
        all_data_list = list(all_data_cursor)
        query = request.GET.get('search')
        if query:
            all_data_list = [data for data in all_data_list if query.lower() in data.get('bookingNo', '').lower()]

        # Paginate the queryset
        paginator = Paginator(all_data_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'message': 'Hello, Coming Soon!',
            "page_obj": page_obj,
        }
        return render(request, self.template_name, context)




def myfun(request,filename):
    try:
        directory_path = r"C:\Users\ATLAnish\Desktop\Abi_projects\docre_5\Altdocre\business_logic\excel_extracter\Excel_output_files"
        
        file_path = os.path.join(directory_path, filename)
        
        with open(file_path, 'rb') as f:
            file_contents = f.read()
        response = HttpResponse(file_contents, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="DR-MSC-20240327-“MSC VIGOUR III” (V. HG410A-4444444444555.xlsx"'
        return response

    except FileNotFoundError:
        return HttpResponse("File not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)
 

def search_files(request):
    query = request.GET.get('query')
    print("query check",query)

    if query:
        query_filter = {"bookingNo": {"$regex": query, "$options": "i"}}
        files = submit_col.find(query_filter)
    else:
        files = submit_col.find()

    # Convert MongoDB cursor to a list of dictionaries
    data = []
    for file in files:
        data.append({
            'bookingNo': file['bookingNo'],
            'bookingCompany': file['bookingCompany'],
            'shippingCompany': file['shippingCompany'],
            'createdDate': file['createdDate'],
            'fullname':file['fullname']

        })
    return JsonResponse(data, safe=False)
        