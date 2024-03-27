
# models.py
from django.db import models
import uuid


class Employee(models.Model):
    regid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phoneNo = models.CharField(max_length=15)
    addressDetails = models.JSONField()
    workExperience = models.JSONField()
    qualifications = models.JSONField()
    projects = models.JSONField()
    photo = models.TextField()

    def serialize(self):
        return {
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'gender': self.gender,
            'phoneNo': self.phoneNo,
            'addressDetails': self.addressDetails,
            'workExperience': self.workExperience,
            'qualifications': self.qualifications,
            'projects': self.projects,
            'photo': self.photo
        }
