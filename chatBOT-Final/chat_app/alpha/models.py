from django.db import models

# Create your models here.


class Memory(models.Model):
    key = models.TextField()
    value = models.TextField()

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        #return f"name: {self.username} password : {self.password}"
        print("name: {self.username} password : {self.password}")


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"Date: {self.created} user: {self.user} message: {self.message}"


'''
class Conversation(models.Model):
    query = models.TextField()
    response = models.TextField()

    def __unicode__(self):
        return self.query
'''