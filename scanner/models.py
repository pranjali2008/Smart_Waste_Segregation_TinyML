from django.db import models

# Create your models here.
class WasteScan(models.Model):
    image = models.ImageField(upload_to='waste_images/')
    waste_type = models.CharField(max_length=50,blank=True)
    confidence = models.FloatField(null=True,blank=True)
    green_coins = models.IntegerField(default=0)
    carbon_credits = models.FloatField(default=0)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.waste_type} - {self.scanned_at}"