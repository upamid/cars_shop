from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.expressions import Col

from PIL import Image


class Cars(models.Model):
    title = models.CharField(
        verbose_name='Наименование автомобиля',
        max_length=200,
        blank=False,
        help_text='Напишите наименование автомобиля'
    )
    link = models.URLField( 
        max_length=128, 
        db_index=True, 
        unique=True, 
        blank=True
    )
    price = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100000000),
            MinValueValidator(1)
        ]
    )
    image = models.FileField(upload_to='images/',
        blank = True,
        verbose_name='Картинка автомобиля',
        )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска автомобиля',
        blank=False,
        help_text='Укажите год выпуска автомобиля',
    )
    text = models.TextField(
        verbose_name='Описание автомобиля',
        blank=False,
        help_text='Добавьте сюда описание автомобиля'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if  img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name = 'Автомобиль',
        verbose_name_plural = 'Автомобили'
        ordering = ['id']


class Color(models.Model):
    car = models.ForeignKey(
        Cars,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name='Автомобиль',
    )    
    name = models.CharField(
        verbose_name='Название цвета автомобиля',
        blank=False,
        max_length=200,
        help_text='Укажите название цвета'
    )
    color = models.CharField(
        verbose_name=(u'Color'),
        max_length=7,
        help_text=(u'HEX color, as #RRGGBB'),
        )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug'
        )

    def __str__(self):
        return self.car.title


class ImageCar(models.Model):
    car = models.ForeignKey(
        Cars,
        on_delete=models.CASCADE,
        )
    image = models.ImageField(
        upload_to='images/',
        blank = True,
        verbose_name='Картинка автомобиля',
        )

    def __str__(self):
        return self.car.title


class Equipment(models.Model):
    name = models.CharField(
        verbose_name='Название комплектации',
        blank=False,
        max_length=200,
        help_text='Укажите название ингредиента'
    )
    text = models.TextField(
        verbose_name='Описание комплектации',
        blank=False,
        help_text='Добавьте сюда описание комплектации'
    )
    car = models.ForeignKey(
        Cars,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name='Автомобиль'
    )

    class Meta:
        verbose_name = 'Комплектация',
        verbose_name_plural = 'Комплектации'
        ordering = ['id']
