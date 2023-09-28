# Environment variables
Create .env.dev file in .env folder using .env.example

# Init DB
docker-compose up -d --build  
docker-compose exec web python manage.py migrate --noinput  
docker-compose exec web python manage.py createsuperuser  

# Get permissions to run tests
docker-compose exec db psql postgresql://pguser:pgpass@db:5432/pgdb  
ALTER USER pguser CREATEDB;

# Run tests
docker-compose exec web python manage.py test

# Swagger documentation
http://127.0.0.1:8000/api/doc/