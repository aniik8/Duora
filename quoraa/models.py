from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from PIL import Image
from ckeditor.fields import RichTextField

class question_data(models.Model):
    questions = RichTextField(blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    datee =  models.DateTimeField('Date Posted', default=datetime.now())

    def __str__(self):
        return self.questions

class answer_data(models.Model):
    questions = models.ForeignKey(question_data,default=1, on_delete=models.SET_DEFAULT)
    answer = RichTextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    image = models.ImageField(upload_to='answer_image', blank=True)
    likes = models.ManyToManyField(User, related_name='likes_for_answer')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return self.answer

    def total_likes(self):
        return self.likes.count()


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='dp', default='default.png')
    bio = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, default='')
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 128 or img.width > 128:
            output_size = (128,128)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)