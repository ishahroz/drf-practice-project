from django.db import models

class Room(models.Model):
    # host = 
    # topic = 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants = 
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
