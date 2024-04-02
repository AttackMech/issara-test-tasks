from django.db import models

class Dealer(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    logo = models.URLField()
    email = models.EmailField()
    rating_score = models.FloatField()
    rating_count = models.IntegerField()
    comments_count = models.IntegerField()
    popularity = models.IntegerField()
    city = models.IntegerField()
