import math

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
CATEGORY_CHOICES = [
    ('other', 'Разное'),
    ('phone_repair', 'Ремонт мобильных телефонов'),
    ('plumbing', 'Сантехника'),
    ('tv_repair', 'Ремонт телевизоров'),
    ('buy_sell', 'Купи-продай')
]
#
# DEFAULT = 'product_pics/default.png'

RATES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
]


class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name='Название')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0],
                                verbose_name='Категории')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(null=True, blank=True, upload_to='product_pics', verbose_name='Картинка')

    def __str__(self):
        return f'{self.name}'

    def avg_rating(self):
        ratings = Review.objects.filter(product=self.pk)
        count = 0
        for r in ratings:
            count += r.rating
        try:
            avg = count / len(ratings)
        except ZeroDivisionError:
            avg = 'Not rated yet'
        return math.ceil(avg)

    class Meta:
        verbose_name = 'Товар-Услуга'
        verbose_name_plural = 'Товары-Услуги'


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1,
                               related_name='reviews', verbose_name='Автор')
    product = models.ForeignKey('webapp.Product', related_name='reviews', on_delete=models.CASCADE,
                                verbose_name='Товар-Услуга')
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Текст')
    rating = models.IntegerField(choices=RATES, null=False, blank=False, verbose_name='Оценка')

    def __str__(self):
        return f'{self.author} - {self.rating}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
