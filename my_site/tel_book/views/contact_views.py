from django.shortcuts import redirect, render, get_object_or_404
from ..models import Contact
from ..forms import ContactForm
from django.contrib import messages


def home_page(request):
    return render(request, 'contacts/home_page.html')


#list contacts
def show_phone_book(request):
    phones = Contact.objects.all()
    return render(request, 'contacts/phone_book.html', {'phones': phones})



#list contacts for edit
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
    return render(request, 'edit_contact.html', {'form': form})


# delete contact
def delete_contact(request, id):
    if not request.user.is_superuser:
        return redirect(show_phone_book)
    contact = get_object_or_404(Contact, id=id)
    if request.method == 'POST':
        contact.delete()
        return redirect(show_phone_book)
    return render(request, 'confirm_delete.html', {'contact': contact})


# add contact
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            UserProfile = form.save(commit=False)
            UserProfile.user = request.user 
            UserProfile.save()
            form.save()
            return redirect(show_phone_book)
    else:
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form})