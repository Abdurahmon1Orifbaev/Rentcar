from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)  # Optional: timestamp

    def __str__(self):
        return f"{self.user.username} - {self.rating}"
