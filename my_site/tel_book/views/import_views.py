import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..models import Contact
import openpyxl
import pandas as pd


def upload_csv(file, request):
    try:
        file_data = file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(file_data)

        for row in csv_reader:
            try:
                Contact.objects.create(
                    name=row['name'],
                    surname=row['surname'],
                    father_name=row['father_name'],
                    type_contact=row['type_contact'],
                    phone=row['phone'],
                    email=row['email'],
                    user=request.user
                )
                print(f"Контакт {row['name']} додано успішно.")
            except KeyError as e:
                print(f'Пропущений стовпець: {e}')
                return HttpResponse(f'Пропущений стовпець: {e}', status=400)

        return redirect('phone_book')
    except Exception as e:
        print(f'Помилка при обробці файлу: {e}')
        return HttpResponse(f'Помилка при обробці файлу: {e}', status=500)
    

def upload_xlsx(file, request):
    try:
        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            Contact.objects.create(
                name=row[0],         
                surname=row[1],      
                father_name=row[2],  
                type_contact=row[3], 
                phone=row[4],        
                email=row[5],        
                user=request.user    
            )
        return redirect('phone_book')
    except Exception as e:
        print(f'Помилка при обробці файлу: {e}')
        return HttpResponse(f'Помилка при обробці файлу: {e}', status=500)
    

def upload_xls(file, request):
    try:
        data = pd.read_excel(file, engine='xlrd')

        for _, row in data.iterrows():
            Contact.objects.create(
                name=row['name'],
                surname=row['surname'],
                father_name=row['father_name'],
                type_contact=row['type_contact'],
                phone=row['phone'],
                email=row['email'],
                user=request.user
            )
        
        return redirect('phone_book') 
    except Exception as e:
        print(f'Неочікувана помилка: {e}')
        return HttpResponse(f'Помилка при обробці файлу: {e}', status=500)


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_type = uploaded_file.name.split('.')[-1].lower()  
        if file_type == 'csv':
            upload_csv(uploaded_file, request) 
        elif file_type in ['xlsx']:
            upload_xlsx(uploaded_file, request)  
        elif file_type in ['xls']:
            upload_xls(uploaded_file, request)
        else:
            return HttpResponse('Невірний формат файлу. Будь ласка, завантажте CSV або XLS(X) файл.', status=400)
        
        return redirect('phone_book')

    return render(request, 'upload.html')  



def parse_html(request):
    if request.method == "POST":
        contacts = Contact.objects.all().order_by('date_create')

        contact_list = []
        for c in contacts:
            if int(c.date_create.strftime('%Y')) >= 2023:  
                                contact_list.append({
                                                    "ID": c.id,
                                                    "Прізвище": c.surname, 
                                                    "Ім'я": c.name,    
                                                    "По-батькові": c.father_name,  
                                                    "Тип контакту": c.type_contact,  
                                                    "Телефон": c.phone,     
                                                    "Email": c.email,    
                                                    "Дата створення": c.date_create.strftime('%Y-%m-%d')
                                                })
        df = pd.DataFrame(contact_list)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="contacts.xlsx"'

        df.to_excel(response, index=False)

        return response


    return HttpResponse("Помилка: не отримано HTML", status=400)