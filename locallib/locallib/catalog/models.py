from django.db import models
from decimal import Decimal
from django.utils import timezone
# Create your models here.
class Type(models.Model):
    type = models.CharField('Тип', max_length=3)
    def __str__(self):
        return self.type
    class Meta:
        app_label = 'catalog'


class State (models.Model):
    state = models.IntegerField('Стан')
    def __str__(self):
        return self.state
    class Meta:
        app_label = 'catalog'


class Size(models.Model):
    size = models.CharField('Розмір', max_length=5)

    def __str__(self):
            return self.size

    class Meta:
            app_label = 'catalog'


class Seasonality(models.Model):
    seasonality = models.IntegerField('Стан')

    def __str__(self):
        return self.seasonality

    class Meta:
        app_label = 'catalog'


class Item(models.Model):
    '''item_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    item_state = models.ForeignKey(State, on_delete=models.CASCADE)
    item_cost = models.DecimalField('Ціна', max_digits=5, decimal_places=2, default=Decimal('0.00'))
    item_date = models.DateTimeField()
    item_seasonality = models.ForeignKey(Seasonality, on_delete=models.CASCADE)


   '''
    item_type = models.CharField('Тип', max_length=30)
    item_color = models.CharField('Колір', max_length=30)
    item_brand = models.CharField('Бренд', max_length=30)
    item_cloth = models.CharField('Тканина', max_length=30)
    item_text = models.CharField('Опис', max_length=100)
   # item_size = models.ForeignKey(Size, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.item_color)

    class Meta:
        app_label = 'catalog'

