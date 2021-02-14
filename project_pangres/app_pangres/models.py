from django.db import models


class UploadModelDemo(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    upload_id = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
