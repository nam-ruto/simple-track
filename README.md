# Application Tracker

A Django web app for tracking job applications. Keep all your applications in one place with a kanban-style board and full CRUD.

## Features

- **Kanban board** — View applications by stage: Applied, Interviewed, Offer, Rejected
- **Per-user data** — Each user sees only their own applications (login required)
- **Full CRUD** — Create, view, edit, and delete applications
- **Rich fields** — Company, location, job title, job URL, status, priority, deadline, salary range, notes
- **Django admin** — Optional backend at `/admin/` for superusers

## Tech Stack

- **Django 6.x** — Backend and auth
- **SQLite** — Default database (no extra setup)
- **Bootstrap** — Styling (via form widgets and message tags)

## Requirements

- Python 3.10+
- Django 6.x

## Setup

1. **Clone and enter the project**
   ```bash
   cd application-tracking
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install Django**
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the dev server**
   ```bash
   python manage.py runserver
   ```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). You’ll be redirected to login; create a user with:

```bash
python manage.py createsuperuser
```

or register via Django admin after creating one superuser, then log in.

## Project Structure

```
application-tracking/
├── config/                 # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── applications/           # Main app
│   ├── models.py          # Application model (status, priority, etc.)
│   ├── views.py           # List, create, edit, delete, detail
│   ├── forms.py           # ApplicationForm
│   ├── urls.py            # App routes
│   └── templates/applications/
│       ├── base.html
│       ├── application_list.html   # Kanban board
│       ├── application_form.html   # Create/Edit
│       ├── application_detail.html
│       └── application_confirm_delete.html
├── manage.py
└── README.md
```

## URLs

| Path            | Description        |
|-----------------|--------------------|
| `/`             | Application list (kanban) |
| `/create/`      | Add new application      |
| `/<id>/`        | Application detail       |
| `/<id>/edit/`   | Edit application         |
| `/<id>/delete/` | Delete application       |
| `/login/`       | Log in                   |
| `/logout/`      | Log out                  |
| `/admin/`       | Django admin             |

## Application Model

- **Status:** Applied → Interviewed → Offer | Rejected  
- **Priority:** Low, Medium, High  
- **Fields:** company, location, job_title, job_url, status, priority, applied_at, deadline, salary_range, notes  

## License

Use and modify as you like.
