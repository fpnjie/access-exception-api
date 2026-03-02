# Access Exception API (Django + DRF)

A Django REST API for managing access exception requests with:
- Structured parameters
- Reviewer workflow
- Status lifecycle (Pending → Approved/Rejected → Expired)
- Audit logging
- JWT authentication
- Filtering & search
- Automatic expiration logic

## Quickstart

```bash
git clone <your-repo-url>.git
cd access-exception-api
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
