from django.shortcuts import redirect, render, get_object_or_404
from ..models import Contact
from ..forms import ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



def home_page(request):
    return render(request, 'contacts/home_page.html')


@login_required
def show_phone_book(request):
    phones = Contact.objects.all()
    return render(request, 'contacts/phone_book.html', {'phones': phones})


def show_phone_book(request):
    phone_list = Contact.objects.all() 

    per_page = request.GET.get('per_page', 5)
    per_page = int(per_page)

    paginator = Paginator(phone_list, per_page)  

    page_number = request.GET.get('page')  
    phones = paginator.get_page(page_number)  

    return render(request, 'contacts/phone_book.html', {
        'phones': phones,
        'per_page': per_page,  
    })                   


@login_required
def edit_contact(request, id):
    try:
        if request.user.is_superuser:
            contact = get_object_or_404(Contact, id=id)
        else:
            contact = get_object_or_404(Contact, id=id, user=request.user)
    except:
        messages.error(request, "Ви не можете редагувати цей контакт, оскільки він вам не належить.")
        return redirect(show_phone_book)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Контакт успішно оновлено.")
            return redirect(show_phone_book) 
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contact_actions/edit_contact.html', {'form': form})


@login_required
def delete_contact(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Контакти може видаляти лише адміністратор")
        return redirect(show_phone_book)
    contact = get_object_or_404(Contact, id=id)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "Контакт успішно видалено.")
        return redirect(show_phone_book)
    messages.success(request, "Контакт успішно видалено.")
    return redirect(show_phone_book)


@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            UserProfile = form.save(commit=False)
            UserProfile.user = request.user 
            UserProfile.save()
            messages.success(request, "Контакт успішно додано.")
            return redirect(show_phone_book)
    else:
        form = ContactForm()
    return render(request, 'contact_actions/add_contact.html', {'form': form})
