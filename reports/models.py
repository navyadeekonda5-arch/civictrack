from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} → {self.department.name}"

class Issue(models.Model):
    STATUS = [
        ('open', 'Open'), ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved (awaiting verification)'),
        ('closed', 'Closed'), ('reopened', 'Reopened'),
    ]
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='open')
    report_count = models.PositiveIntegerField(default=1)
    priority_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.id} {self.category.name} ({self.report_count} reports)"

class Report(models.Model):
    issue = models.ForeignKey(Issue, related_name='reports', on_delete=models.CASCADE)
    citizen = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='reports/')
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class OfficerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.department.name})"

class IssueUpdate(models.Model):
    issue = models.ForeignKey(Issue, related_name='updates', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    proof_photo = models.ImageField(upload_to='proof/', blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)