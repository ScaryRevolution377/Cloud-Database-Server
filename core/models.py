from django.db import models
from django.contrib.auth.models import User

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")

file_name = models.CharField(max_length=50)
file_url = models.URLField(max_length=500)
uploaded_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.user.username} - {self.file_name}"
