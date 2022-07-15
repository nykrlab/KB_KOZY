from django.db import models

class Bookmark(models.Model):
    content = models.TextField()
    user_id = models.TextField()