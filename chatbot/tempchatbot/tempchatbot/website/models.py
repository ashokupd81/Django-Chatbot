from django.db import models


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"name: {self.username} password : {self.password}"


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"Date: {self.created} user: {self.user} message: {self.message}"
