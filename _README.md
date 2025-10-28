# Seattle Councilmatic

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Configure Your Instance

```bash
cp .env.example .env
```

```bash
pip install -r requirements.txt
```

**`.env`** - Set your environment variables:

- Generate a secure `DJANGO_SECRET_KEY`
- Configure your database connection
- Set up search engine URLs

### 2. Initial Setup

```bash
docker compose build
```

### 3. Create a Superuser

```bash
docker compose run --rm app python manage.py createsuperuser
```

### 4. Start Development Server

```bash
docker compose up
```

Visit <http://localhost:8000> to see your site!

## Data Import

We recommend using `pupa` to scrape and import data into your database. Follow [its helpful documentation](https://open-civic-data.readthedocs.io/en/latest/scrape/new.html) to initialize and run your own scraper/s to populate your database.

N.b., your app comes with `pupa` pre-installed! You can use your containers to run the commands specified in the `pupa` docs like this:

```bash
# Initialize your scrapers
docker compose run --rm app pupa init seattle

# Run a scrape
docker compose run --rm app pupa update seattle
```

## Development Workflow

### Frontend Development

The template uses Webpack to build frontend assets:

- **SCSS files**: `seattle/static/scss/`
- **JavaScript files**: `seattle/static/js/`

Customize your city's branding by editing:

- `seattle/static/scss/main.scss` - Colors, fonts, and styles
- `seattle/static/js/main.js` - JavaScript functionality

## Customization

### Templates

Councilmatic gives you the infrastructure. You create the interface! Build your site by
adding templates to `seattle/templates/`.

### Models

Extend core models in `seattle/models.py`:

```python
class SeattleBill(Bill):
    # Add custom fields or methods
    custom_field = models.CharField(max_length=100, blank=True)
    
    class Meta:
        proxy = True
```

## Getting Help

- [Councilmatic documentation](https://www.councilmatic.org/)
- [Django Councilmatic GitHub](https://github.com/datamade/django-councilmatic)
- [Open Civic Data documentation](https://open-civic-data.readthedocs.io)

## License

Copyright (c) 2025 Participatory Politics Foundation and DataMade. Released under the [MIT License](LICENSE).
