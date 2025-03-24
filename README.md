### ERD

CarItem
- id int
- brand string
- license_plate (unique) string
- frame_number (unique) string
- model string
- color (optional) string

## requirements???

- sqlite for testing
- postgresql for local, dev, prod
- model manager /  table manager / ORM /  migration


## HOW TO GET STARTED
- docker destop
- uv python

### how to run the DB

- docker-compose up -d

### how to migrate db
- uv run flask db migrate
- uv run flask db upgrade

### how to load the fixtures
- uv run python load_fixture.py