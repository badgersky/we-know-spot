from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    date_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag_name


class Province(models.Model):
    province_name = models.CharField(max_length=100)
    main_city = models.CharField(max_length=100)
    date_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.province_name
