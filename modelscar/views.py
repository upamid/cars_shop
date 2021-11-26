from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

import environ

from .forms import ContactForm
from .models import Cars, Color, ImageCar, Equipment


env = environ.Env()
environ.Env.read_env()


def shop_view(request):
    cars = Cars.objects.all()
    return render(request, 'blog.html', {'posts': cars})


def detail_view(request, id):
    car = get_object_or_404(Cars, id=id)
    photos = ImageCar.objects.filter(car=car)
    equipment = Equipment.objects.filter(car=car)
    color = Color.objects.filter(car=car)
    return render(request, 'detail.html', {
        'post': car,
        'photos': photos,
        'equipment': equipment,
        'color': color,
    })


def contact(request, id):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Покупка авто"
            car = get_object_or_404(Cars, id=id)
            equipment = Equipment.objects.filter(car=car)
            colors = Color.objects.filter(car=car)
            eq = []
            c = []
            for q in equipment:
                eq.append(q.name)
            for color in colors:
                c.append(color.name)
            body = {
                'last_name': form.cleaned_data['last_name'],
                'first_name': form.cleaned_data['first_name'],
                'middle_name': form.cleaned_data['middle_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
                'car': car.title,
                'price': str(car.price),
                'equipment': '; '.join(eq),
                'color': '; '.join(c)}
            message = f'''Фамилия: {body['last_name']}\n
                        Имя: {body['first_name']}\n
                        Отчество: {body['middle_name']}\n
                        Почта: {body['email']}\n
                        Сообщение: {body['message']}\n
                        Автомобиль {body['car']}\n
                        Цена {body['price']} руб.\n
                        Комплектации {body['equipment']}\n
                        Цвета {body['color']}\n
                        '''
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email_address']]
                    )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("blog")
    form = ContactForm()
    return render(request, "contact.html", {'form': form})
