from django.db import models
import uuid 

class Tour(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.title 

    class Meta:
        db_table = "tour"


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images',null=False)
    image = models.FileField(upload_to='tour')

    class Meta:
        db_table = "tour_image"

    def __str__(self) -> str:
        return f'{self.tour}'
