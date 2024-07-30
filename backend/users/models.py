from django.db import models


class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=30)
    user_email = models.EmailField(max_length=254)
    user_password = models.CharField(max_length=128, null=True, blank=True) 
    objects = models.Manager()


class Albums(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    s3_url = models.CharField(max_length=255)
    is_private = models.BooleanField(True)
    objects = models.Manager()


class Photos(models.Model):
    album = models.ForeignKey(Albums, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    s3_url = models.CharField(max_length=255)
    objects = models.Manager()


class Networks(models.Model):
    founder_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Albums, on_delete=models.CASCADE)
    objects = models.Manager()
