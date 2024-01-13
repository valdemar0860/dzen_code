from django.db import models
from django.contrib.auth import get_user_model


class Comment(models.Model):
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.text