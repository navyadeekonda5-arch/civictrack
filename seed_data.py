from django.contrib.auth.models import User
from reports.models import Department, Category, OfficerProfile

depts = {
    'Roads Department': ['road', 'pothole'],
    'Sanitation Department': ['garbage'],
    'Electricity Department': ['streetlight'],
    'Water & Drainage Department': ['drainage'],
}
for dept_name, cats in depts.items():
    d, _ = Department.objects.get_or_create(name=dept_name, defaults={'email': 'demo@civictrack.test'})
    for c in cats:
        Category.objects.get_or_create(name=c, defaults={'department': d})

if not User.objects.filter(username='roads_officer').exists():
    u = User.objects.create_user('roads_officer', password='Roads@2026')
    OfficerProfile.objects.create(user=u, department=Department.objects.get(name='Roads Department'))

print('Demo data ready')