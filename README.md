Instructions: 0. Navigate to project dir

1. Run Postgre database docker-compose up -d
2. Create database structure `python manage.py makemigrations` and then `python manage.py migrate`
3. Migration command: "python -m mgr_django.utils.migration"
4. launch the application `python manage.py runserver`
5. Open http://localhost:8000

# Implemented: Reset password and settings sequrity on Django project

In this project it is required to implement Django application to manage quotes by different users.

## Task description:

- Implement mechanizm of reset password for registered user
- All environment variables should be stored in a file .env and should be utilized in the settings.py file.

# Project technical task

Task description
Create a site. The site should be created similar to http://quotes.toscrape.com .
It is needed to implement this using Django.

1. Implement possibility to register on the site and login to the site.
2. Possibility to add new quote to site with the author's name (only for registerd users)
3. Do database migration from existing MongoDB to Postgres for your site. It can be implemented using custom script. (If desired you can leave quotes and authors on MongoDB and fork with users in Postgres)
4. All quotes are viewable without user authentication and you can see author's page without authentication as well.

Additional part

1. Implement search for quotes by tag. When you click on a tag, a list of quotes with this tag is displayed.
2. Incorporate "Top Ten tags" block and display the most popular tags.
3. Implement pagination. These are the nex and previous buttons.
4. Add the possibility of scraping data directly from your site by pressing a certain button on the form and filling the site database instead of transerring data from the MongoDB database.
