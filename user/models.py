from django.db import models

# Create your models here.

class RegisterModel(models.Model):
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    userid=models.CharField(max_length=200)
    password=models.IntegerField()
    mobilenumber=models.BigIntegerField()
    email=models.EmailField()
    gender=models.CharField(max_length=200)


class UploadModel(models.Model):
    usid = models.ForeignKey(RegisterModel, on_delete=models.CASCADE)
    usname=models.CharField(max_length=200)
    topic=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    upload_file=models.FileField()
    add_count=models.IntegerField(default='0')
    location=models.CharField(max_length=200)
    original_filename=models.CharField(max_length=300, default='')


class AttackLog(models.Model):
    """Stores every attack that was blocked by the ML Ensemble."""
    username  = models.CharField(max_length=200, default='Unknown')
    filename  = models.CharField(max_length=300, default='')
    cnn_score  = models.FloatField(default=0)
    lstm_score = models.FloatField(default=0)
    mrn_score  = models.FloatField(default=0)
    ensemble_score = models.FloatField(default=0)
    timestamp  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Attack by {self.username} on {self.timestamp:%Y-%m-%d %H:%M}"