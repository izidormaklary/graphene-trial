from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=360)
    status = models.BooleanField()
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title
