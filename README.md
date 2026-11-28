# PinoyRSS : Your Philippine RSS website for reliable, up-to-date information

PinoyRSS is a mobile news aggregator that delivers pre-curated and ad-free articles from verified Philippine news outlets. It is designed to eliminate the barrier from traditional RSS readers by providing a built-in library of trusted feeds that users can browse, search, filter and bookmark and read within the app.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                  # then fill in SECRET_KEY and DATABASE_URL; copy instead of cp in Windows
python manage.py migrate
python manage.py createsuperuser                      # then set Role = Admin in /admin/ for the admin dashboard
python manage.py seed_library                         # default categories + starter Philippine outlets
python manage.py fetch_rss                            # pull and auto-categorise articles (re-run any time)
python manage.py runserver
```


## Pages

| URL | What it does |
| --- | --- |
| `/` | Dashboard: search, today's stories, topics, recent bookmarks |
| `/articles/` | News list with keyword search, outlet / category / date filters, pagination (10 per page) |
| `/articles/<id>/` | In-app reader with the full text and the source link at the bottom |
| `/categories/` | Browse by category |
| `/bookmarks/` | Your bookmarks: search, filter by category, edit note or category, remove |
| `/accounts/profile/` | Profile and password change |
| `/admin-panel/` | Admin overview (admins only) |
