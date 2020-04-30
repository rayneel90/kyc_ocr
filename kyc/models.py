from django.db import models


class Input(models.Model):
    type = models.CharField(
        verbose_name="KYC Type",
        choices=(("PAN", "PAN Card"), ("Aadhar", "Aadhar Card"),
                 ("Passport", "Passport")),
        max_length=8
    )
    image = models.ImageField(verbose_name="Image", upload_to='image/%Y/%b/%d')
    created = models.DateTimeField(auto_now_add=True)

class Output(models.Model):
    input = models.ForeignKey(Input, on_delete=models.CASCADE)
    number = models.CharField(max_length=30, null=True)
    status = models.BooleanField()
    error = models.CharField(max_length=1000, null=True)