from django.db import models

# Create your models here.
class Metadata(models.Model):
    download_date = models.DateTimeField()
    filename = models.CharField(max_length=255)

    def __str__(self):
        return_text = str(self.download_date) + " " + self.filename
        return return_text
