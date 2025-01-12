from django.shortcuts import render

def user_data_view(request):
    user = request.user 
    return render(request, 'header.html', {'user': user})
