from math import radians, sin, cos, sqrt, atan2
from django.utils import timezone
from .models import Issue

CLUSTER_RADIUS_M = 30
SEVERITY = {
    'pothole': 3,
    'drainage': 3,
    'streetlight': 2,
    'road': 2,
    'garbage': 1,
}

def distance_m(lat1, lon1, lat2, lon2):
    """Haversine: distance in meters between two GPS points."""
    R = 6371000
    p1, p2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlmb = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(p1) * cos(p2) * sin(dlmb / 2) ** 2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))

def calculate_priority(issue):
    days_open = (timezone.now() - issue.created_at).days
    severity = SEVERITY.get(issue.category.name.lower(), 1)
    return issue.report_count * 10 + severity * 5 + days_open * 2

def find_or_create_issue(category, lat, lon):
    """Returns (issue, joined_existing)."""
    nearby = Issue.objects.filter(category=category).exclude(status='closed')
    for issue in nearby:
        if distance_m(lat, lon, issue.latitude, issue.longitude) <= CLUSTER_RADIUS_M:
            issue.report_count += 1
            issue.priority_score = calculate_priority(issue)
            issue.save()
            return issue, True

    issue = Issue.objects.create(category=category, latitude=lat, longitude=lon)
    issue.priority_score = calculate_priority(issue)
    issue.save()
    return issue, False