from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse, HttpResponseBadRequest, StreamingHttpResponse
from django.views import View
from .forms import FileUploadForm
from .models import UploadedFile
from business_logic.source_code.main import Main_Class
from business_logic.source_code.PDFExtractor import PDFExtractor
import pandas as pd
import os
import json
import openpyxl

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from business_logic.excel_extracter.json_file_read import MainClass


path = os.getcwd()

class FileUploadView(View):
    template_name = 'fileupload/home.html'
    fileupload = []
    dataframe = []

    def get(self, request):
        form = FileUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = FileUploadForm(request.POST, request.FILES)
        
            if form.is_valid():
                icm   = request.POST.get('form-select')
                icm1  = request.POST.get('form-select-sm')
                file1 = request.FILES.get('file1')
                file2 = request.FILES.get('file2')
                files = [form.cleaned_data[f] for f in form.files]
            
                for uploaded_file in files:
                    # Save the file to the server
                    instance = UploadedFile()
                    instance.file = uploaded_file

                # Save the file to the server
                    instance = UploadedFile(file=uploaded_file)

                excel_data = self.read_excel_file(instance.file.path)
                print("excel data -----@@@@@@",excel_data)
            # if form:
            #     icm   = request.POST.get('form-select')
            #     icm1  = request.POST.get('form-select-sm')
            #     file1 = request.FILES.get('file1')
            #     file2 = request.FILES.get('file2')

            #     self.fileupload.append((icm, icm1, file1, file2))

                main = Main_Class(icm, icm1, [file1,file2])
                main.main_function()
                df1=main.df
                df3=main.df_1

                self.dataframe.append([df1,df3])

                return redirect('view_files')
        else:
            form = FileUploadForm()
            return render(request, 'upload_files.html', {'form': form})
            
    def read_excel_file(file_path):
        # Use openpyxl to read the Excel file
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        # Process the data as needed
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(row)

        return data
       
class FileListView(View):
    template_name = 'fileupload/file_list.html'

    def get(self, request):
        files = UploadedFile.objects.all()
        return render(request, self.template_name, {'files': files})

class ViewFilesView(View):
    template_name = 'fileupload/outputedit.html'

    def get(self, request):
        print("####################################################")
        objclass1 = FileUploadView()
        objclass1.fileupload
        objclass1.dataframe

        obj = objclass1.fileupload
        for i in obj:
            icm = i[0]
            icm1 = i[1]
            file1 = i[2]
            file2 = i[3]

            print("_______",icm)
            print("_______",icm1)
            print("_______",file1)
            print("_______",file2)

        Data_frame = objclass1.dataframe
        for df_ in Data_frame:
            df1 = df_[0]
            df3 = df_[1]

        obj = PDFExtractor(icm, icm1)
        obj.extract_pdf_coordinates()
        df2 = obj.df

        df1 = df1.to_dict(orient='records')
        df2 = df2.to_dict(orient='records')
        df3 = df3.to_dict(orient='records')

        return render(request, self.template_name, {'df1_html': df1, 'df2_html': df2, 'df3_html': df3})
    

@method_decorator(csrf_exempt, name='dispatch')
class AjaxSaveView(View):
    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                # Assuming the data is sent as JSON
                data = json.loads(request.body)

                print('Received data:', data)
                request.session['data'] = data
                # print('Session data set:', request.session['data'])
                
                response_data = {'status': 'success', 'message': 'Data saved successfully'}
                return JsonResponse(response_data)
            except json.JSONDecodeError as e:
                response_data = {'status': 'error', 'message': 'Invalid JSON data'}
                return JsonResponse(response_data, status=400)
        else:
            response_data = {'status': 'error', 'message': 'Invalid request'}
            return JsonResponse(response_data, status=400)
     
class MscExcelView(View):
    template_name = 'fileupload/excel_file.html'

    def get(self, request, *args, **kwargs):
        
        json_dict = request.session.get('data')
        print("######################################")
        print(json_dict)
        if json_dict is not None:
            payload_dict = json_dict.get('payload', {})
        else:
            print("json_dict is None. Unable to retrieve payload.")

        json_data = json.dumps(payload_dict)
        json_data_dict = json.loads(json_data)
        template_excel_path = path + "\\business_logic\excel_extracter\MSC DURBAN TEMPLATE.xlsx"
        output_folder_path = path +"\\business_logic\excel_extracter\Excel_output_files"

        # print(json_file_path)
        print(template_excel_path)
        print(output_folder_path)

        # Access the 'payload' key
        instance_var = MainClass()
        processed_data = instance_var.processJson(json_data_dict)

        # Ensure the output folder exists
        os.makedirs(output_folder_path, exist_ok=True)

        # Call the copy_template_and_populate method and capture the returned new_file_name
        new_file_name = instance_var.copy_template_and_populate(template_excel_path, output_folder_path, processed_data)
        request.session['new_file_name'] = new_file_name

        return render(request, self.template_name, {'message': 'Data processed successfully','new_file_name':new_file_name})
    
class ExcelDownloadView(View):
    template_name = 'fileupload/excel_file.html'

    def get(self, request, *args, **kwargs):

        new_file_name = request.session.get('new_file_name')

        excel_file_path = path +'\\business_logic\excel_extracter\Excel_output_files'
        excel_file_path = f"{excel_file_path}\\{new_file_name}"
        print("excel_file_path",excel_file_path)

        if os.path.exists(excel_file_path):
            excel_file_name = os.path.basename(excel_file_path)
            response = StreamingHttpResponse(self.file_iterator(excel_file_path))
            response['Content-Disposition'] = f'attachment; filename="{excel_file_name}"'
            return response
        else:
            return render(request, self.template_name, {'file_not_found': True})

    def file_iterator(self, file_path, chunk_size=8192):
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk