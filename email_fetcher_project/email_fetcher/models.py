from django.db import models

class Email(models.Model):
    sender = models.EmailField()
    subject = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Subject: {self.subject} from {self.sender}"
