from django.db import models

class Youtube(models.Model):
    name = models.CharField(max_length=255)
    title = models.TextField(blank=True, null=True)
    rank = models.DecimalField(default=0,
                                    max_digits=14, decimal_places=7)

    def __str__(self):
        return self.name

class GeoAnalytics(models.Model):
    
    class Meta:
        unique_together = (('youtube', 'country_code', ),)

    youtube = models.ForeignKey(Youtube, related_name='geo')
    country_code = models.CharField(max_length=5)
    viewer_percentage = models.DecimalField(default=0,
                                            max_digits=5, decimal_places=2)

    def __str__(self):
        return self.country_code

class DemographicsAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube', 'age_group', 'gender', ),)

    youtube = models.ForeignKey(Youtube, related_name='demographics')
    age_group = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    viewer_percentage = models.DecimalField(default=0,
                                            max_digits=5, decimal_places=2)

    def __str__(self):
        return ', '.join((self.gender, self.age_group))

class DeviceAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube', 'device_type', ),)

    youtube = models.ForeignKey(Youtube, related_name='device_views')
    device_type = models.CharField(max_length=50)
    viewer_percentage = models.DecimalField(default=0,
                                            max_digits=5, decimal_places=2)

    def __str__(self):
        return self.device_type

class OSAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube', 'os', ),)

    youtube = models.ForeignKey(Youtube, related_name='os_views')
    os = models.CharField(max_length=50)
    viewer_percentage = models.DecimalField(default=0,
                                            max_digits=5, decimal_places=2)

    def __str__(self):
        return self.os
