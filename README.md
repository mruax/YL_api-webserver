# YL_api-webserver
This is third Yandex Lyceum project webserver-api!
What is this project? This is a multi-page site specializing not in beautiful design or semantic integrity, but in the practical part. The project is just a demonstration of a wide range of functions, modules and other things.

Features:
- User authentication / authorization system.
- Massive database with multiple relationships between tables.

Further I am too lazy to write, but you can make your own to explore the program and to find more features and capabilities.

Not bugs - features (honestly):
1) Items can have same name and all other characteristics.
2) Mail send works only on local server because of heroku add-on system. 
3) After deleting items from database id autoincrement does not roll back or change previous items id.

Planned in the future:
1) Finalize unittests for api functions GET/POST/PUT/DELETE interacting with database.
2) Fill the site with content.
3) Solve heroku mail add-on problem.  