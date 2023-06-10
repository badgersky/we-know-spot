from django.core.validators import MinValueValidator
from django.db import models
from config.settings import AUTH_USER_MODEL


class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    date_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        ordering = ('tag_name',)


class Province(models.Model):
    province_name = models.CharField(max_length=100)
    main_city = models.CharField(max_length=100)
    date_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.province_name

    class Meta:
        ordering = ('province_name',)


class Spot(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    province = models.ForeignKey('Province', on_delete=models.CASCADE)
    likes = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    photo = models.ImageField(upload_to='spot-photos')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_add', '-likes',)
        

class SpotLike(models.Model):
    spot = models.ForeignKey('Spot', on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
