from django.contrib import admin
from . import models

admin.site.register(models.DataInfo)
admin.site.register(models.ModelInfo)
admin.site.register(models.AlgoList)
admin.site.register(models.ModelConfig)
admin.site.register(models.ReportInfo)
admin.site.register(models.UserInfo)