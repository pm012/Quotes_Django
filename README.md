# HW10Django
Task description
It should be created similar site to http://quotes.toscrape.com . 
You need to implement this using Django.

1. Implement possibility to register on site and login to site.
2. Possibility to add new quote to site with the author's name (only for registerd users)
3. Do database migration from existing MongoDB to Postgres for your site. It can be implemented using custom script. (If desired you can leave quotes nad authors on MongoDB and fork with users in Postgres)
4. All quotes are viewable without user authentication and you can see author's page without authentication as well.

Additional part
1. Implement search for quotes by tag. When you click on a tag, a list of quotes with this tag is displayed. 
2. Incorporate "Top Ten tags" block and display the most popular tags.
3. Implement pagination. These are the nex and previous buttons.
4. Add the possibility of scraping data directly from your site by pressing a certain button on the form and filling the site database instead of transerring data from the MongoDB database.