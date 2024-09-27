from django.db import models
from django.contrib.auth.models import User

class Template(models.Model):
    name = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'templates'

class Domain(models.Model):
    id_template = models.ForeignKey(Template, on_delete=models.CASCADE, db_column='id_template')
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user')
    name = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'domains'