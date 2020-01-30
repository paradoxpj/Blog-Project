from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    '''Database model for a blog post'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500, blank=False)
    image = models.ImageField(upload_to='uploads/', blank=False)
    created_on = models.DateTimeField()

    def __str__(self):
        '''Return the model as a string'''
        return self.title + " - " + self.user.username
