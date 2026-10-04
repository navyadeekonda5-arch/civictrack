from django.contrib import admin
from .models import Department, Category, Issue, Report, OfficerProfile, IssueUpdate

admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Issue)
admin.site.register(Report)
admin.site.register(OfficerProfile)
admin.site.register(IssueUpdate)

# Register your models here.
