# Seattle Councilmatic

A website for tracking Seattle City Council legislation, built on the [Councilmatic](https://www.councilmatic.org/) platform.

## 🎯 What It Does

Seattle Councilmatic makes it easy to:

- Find your Seattle City Council representative
- Track legislation (bills, resolutions, ordinances)
- See upcoming council meetings and agendas
- Follow votes on issues you care about

**Live site:** <http://localhost:8000> (development)

---

## 🏗️ Architecture

### Components

```
┌─────────────────┐
│  seattle.gov    │  Official city council website
│  legistar.com   │  Legislative management system
└────────┬────────┘
         │ Scrapers pull data
         ▼
┌─────────────────┐
│  Pupa Scrapers  │  Extract & Transform data
│  (seattle/)     │  
└────────┬────────┘
         │ Writes to OCD format
         ▼
┌─────────────────┐
│  PostgreSQL     │  Open Civic Data models
│  + PostGIS      │  (opencivicdata_*)
└────────┬────────┘
         │ Synced to
         ▼
┌─────────────────┐
│ Councilmatic    │  Django models
│   Models        │  (councilmatic_core_*)
└────────┬────────┘
         │ Indexed by
         ▼
┌─────────────────┐
│ Elasticsearch   │  Full-text search
└────────┬────────┘
         │ Powers
         ▼
┌─────────────────┐
│  Django Web UI  │  User-facing website
│  (seattle_app/) │
└─────────────────┘
```

### Directory Structure

```
seattle-councilmatic/
├── seattle/              # Pupa scrapers (data collection)
│   ├── __init__.py      # Jurisdiction definition
│   ├── people.py        # Council member scraper
│   ├── events.py        # Meeting scraper (TODO)
│   └── bills.py         # Legislation scraper (TODO)
├── seattle_app/         # Django application (presentation)
│   ├── management/      # Custom management commands
│   ├── templates/       # HTML templates
│   ├── static/          # CSS, JS, images
│   ├── models.py        # Custom model extensions
│   └── settings.py      # Django configuration
├── scripts/             # Helper scripts
│   └── update_seattle.sh # One-command data update
├── docker-compose.yml   # Container orchestration
├── Dockerfile           # Container definition
└── requirements.txt     # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker Desktop](https://docs.docker.com/desktop/)
- Git

### Initial Setup

1. **Clone the repository:**

```bash
   git clone [your-repo-url]
   cd seattle-councilmatic
```

2. **Configure environment:**

```bash
   cp .env.example .env
   # Edit .env and add your DJANGO_SECRET_KEY
   # Generate one with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

3. **Build containers:**

```bash
   docker compose build
```

4. **Initialize database:**

```bash
   # Run Django migrations
   docker compose run --rm app python manage.py migrate
   
   # Initialize Pupa tables
   docker compose run --rm app pupa dbinit us
   
   # Create admin user
   docker compose run --rm app python manage.py createsuperuser
```

5. **Load initial data:**

```bash
   docker compose run --rm app ./scripts/update_seattle.sh
```

6. **Start the application:**

```bash
   docker compose up
```

7. **Visit the site:**
   - Main site: <http://localhost:8000>
   - Admin: <http://localhost:8000/admin>

---

## 🔄 Daily Development Workflow

### Update Data

```bash
# Full update (all scrapers)
docker compose run --rm app ./scripts/update_seattle.sh

# Update specific scraper
docker compose run --rm app ./scripts/update_seattle.sh people
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f app
docker compose logs -f webpack
```

### Django Management Commands

```bash
# Run any Django command
docker compose run --rm app python manage.py [command]

# Examples:
docker compose run --rm app python manage.py shell
docker compose run --rm app python manage.py dbshell
docker compose run --rm app python manage.py sync_councilmatic
```

### Restart Services

```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart app
```

---

## 🛠️ Technical Details

### Data Flow

1. **Scraping** (`pupa update seattle`)
   - Scrapers in `seattle/` fetch data from source websites
   - Data is validated and cached locally
   - Written to OpenCivicData tables (`opencivicdata_*`)

2. **Syncing** (`python manage.py sync_councilmatic`)
   - Bridges OCD models → Councilmatic models
   - Handles multi-table inheritance pattern
   - Creates required fields (slugs, etc.)

3. **Indexing** (`python manage.py update_index`)
   - Populates Elasticsearch for full-text search
   - Powers the site's search functionality

### Why Two Sets of Models?

Django-councilmatic 5.x uses **multi-table inheritance** rather than proxy models:

- **OCD Models** (`opencivicdata_person`): Canonical data from scrapers
- **Councilmatic Models** (`councilmatic_core_person`): Extended with web-specific fields (slugs, headshots, etc.)

They're linked via foreign key, requiring the sync step.

### Important Settings

**In `seattle_app/settings.py`:**

```python
# Must match your Jurisdiction.name in seattle/__init__.py
OCD_CITY_COUNCIL_NAME = 'Seattle City Council'

# Both scraper and app must be in INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'opencivicdata.core.apps.BaseConfig',
    'councilmatic_core',
    'seattle_app',  # Django app
    'seattle',      # Pupa scrapers
]
```

---

## 🧪 Testing

### Run Tests

```bash
docker compose run --rm app python manage.py test
```

### Check Scraper Output

```bash
# Scrape without importing (for testing)
docker compose run --rm app pupa update seattle people --scrape

# Check what was scraped
docker compose run --rm app ls -la _data/
```

### Validate Data

```bash
docker compose run --rm app python manage.py shell
```

```python
from opencivicdata.core.models import Person, Organization
from councilmatic_core.models import Person as CouncilPerson

# Check data counts
print(f"OCD People: {Person.objects.count()}")
print(f"Councilmatic People: {CouncilPerson.objects.count()}")
print(f"Organizations: {Organization.objects.count()}")

# Verify memberships
council = Organization.objects.get(name='Seattle City Council')
print(f"Council members: {council.memberships.count()}")
```

---

## 🐛 Troubleshooting

### "No data showing on website"

1. Check if data exists in database:

```bash
   docker compose run --rm app python manage.py shell -c "from opencivicdata.core.models import Person; print(Person.objects.count())"
```

2. Run sync command:

```bash
   docker compose run --rm app python manage.py sync_councilmatic
```

3. Rebuild search index:

```bash
   docker compose run --rm app python manage.py rebuild_index --noinput
```

### "Containers won't start"

Check port conflicts:

```bash
# Check if ports are in use
lsof -i :8000  # Django
lsof -i :5432  # PostgreSQL
lsof -i :9200  # Elasticsearch
lsof -i :3000  # Webpack
```

### "Out of memory errors"

Increase Docker Desktop memory allocation:

- Settings → Resources → Memory → Set to at least 4GB

### "Database migrations fail"

Reset and re-initialize:

```bash
docker compose down -v  # WARNING: Deletes all data!
docker compose up -d postgres
docker compose run --rm app python manage.py migrate
docker compose run --rm app pupa dbinit us
```

---

## 📚 Key Documentation Links

- [Councilmatic Website](https://www.councilmatic.org/)
- [Open Civic Data & Pupa Documentation](https://open-civic-data.readthedocs.io/en/latest/)
- [Open Civic Data Github](https://github.com/opencivicdata)
- [Django Documentation](https://docs.djangoproject.com/)

---

## 🤝 Contributing

### Adding New Scrapers

1. **Create scraper file** in `seattle/` (e.g., `events.py`)

2. **Register in jurisdiction** (`seattle/__init__.py`):

```python
   from .events import SeattleEventScraper
   
   class Seattle(Jurisdiction):
       scrapers = {
           "people": SeattlePersonScraper,
           "events": SeattleEventScraper,  # Add here
       }
```

3. **Test the scraper:**

```bash
   docker compose run --rm app pupa update seattle events --scrape
```

4. **Run full import:**

```bash
   docker compose run --rm app ./scripts/update_seattle.sh events
```

### Code Style

- Follow PEP 8 for Python
- Use Django conventions
- Add docstrings to functions
- Comment complex logic

---

## 📝 License

[Your chosen license]

---

## 🙏 Acknowledgments

Built with:

- [Councilmatic](https://www.councilmatic.org/) by DataMade
- [Open Civic Data](https://opencivicdata.org/)
- [Pupa](https://github.com/opencivicdata/pupa) scraping framework

Data sources:

- [Seattle City Council](https://www.seattle.gov/council)
- [Seattle Legistar](https://seattle.legistar.com)
