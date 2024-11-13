import csv
from django.shortcuts import render
from ..forms import CSVUploadForm
from ..models import Contact

def import_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    Contact.objects.create(
                        name=row['name'],
                        surname=row['surname'],
                        father_name=row['father_name'],
                        type_contact=row['type_contact'],
                        phone=row['phone'],
                        email=row['email'],
                        user=request.user 
                    )
                return render(request, 'import/import_success.html')
            except Exception as e:
                print('Error while processing CSV:', e)  
        else:
            print('Form is not valid')
    else:
        print('Request method is not POST') 
        form = CSVUploadForm()
    return render(request, 'import/import_csv.html', {'form': form})
