# CivicTrack

Civic issue reporting app. Citizens report potholes, road damage, garbage, streetlight and drainage problems with a photo and location. Reports of the same problem at the same place are merged into one issue and prioritised. Department officers update progress, and citizens can follow it.

## Try it in GitHub Codespaces
1. Click the green **Code** button, then **Codespaces**, then **Create codespace**.
2. In the terminal that opens, run:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py shell -c "exec(open('seed_data.py').read())"
python manage.py runserver
```
3. Click **Open in Browser** on the popup.

## Run it on your computer
Needs Python 3.12 or newer.
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py shell -c "exec(open('seed_data.py').read())"
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Logins
- Citizen: sign up on the login page
- Officer (demo): `roads_officer` / `Roads@2026`