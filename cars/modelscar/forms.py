from django import forms

# Create your forms here.

class ContactForm(forms.Form):
    last_name = forms.CharField(max_length = 50,
    label='Фамилия')
    first_name = forms.CharField(max_length = 50,
    label='Имя')
    middle_name = forms.CharField(max_length = 50,
    label='Отчество')
    email_address = forms.EmailField(max_length = 150,
    label='Адресс электронной почты')
    message = forms.CharField(widget = forms.Textarea, max_length = 2000,
    label='Сообщение для вопросов')