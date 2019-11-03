# courseinfo

## Init DB

```bash
# delete DB migration files
rm -rf classroom/migrations/0*.py

# generate DB migration files
python manage.py makemigrations

# build DB tables
rm -rf db.sqlite3
python manage.py migrate

# clean DB
python manage.py flush --noinput

# init DB
python initdb.py

```