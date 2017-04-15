from django.contrib import admin

from .models import (Youtube, GeoAnalytics,
                     DemographicsAnalytics, DeviceAnalytics,
                     OSAnalytics)

admin.site.register(Youtube)
admin.site.register(GeoAnalytics)
admin.site.register(DemographicsAnalytics)
admin.site.register(DeviceAnalytics)
admin.site.register(OSAnalytics)
