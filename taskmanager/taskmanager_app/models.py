from django.db import models
from django import forms

class CardsCollections(models.Model):
    collection_name = models.CharField(max_length=100)  # Заголовок задачи

    def __str__(self):
        return self.title  # Отображение названия задачи в административной панели

class Cards(models.Model):
    text_russian = models.CharField(max_length=30)
    text_english = models.CharField(max_length=30)

    # Связь с коллекцией через ForeignKey
    collection = models.ForeignKey(CardsCollections, on_delete=models.CASCADE, related_name='cards',default='0')

    def __str__(self):
        return self.title  # Отображение названия задачи в административной панели