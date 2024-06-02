from django.db import models


class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=30)
    user_email = models.EmailField(max_length=254)

    objects = models.Manager()
