# OpenSurvey


This project uses [Foreman](https://github.com/ddollar/foreman) for managing secrets like the database username and password and [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) for managing the Python packages.

When deploying to Ubuntu 14.04, run the following command to make sure the required packages are present:

    $ sudo apt-get install git python-pip postgresql postgresql-contrib python-psycopg2 python-dev libpq-dev ruby
    $ sudo pip install virtualenv
    $ gem install foreman

Now clone the repository and install the required Python packages:

    $ git clone https://github.com/vta/OpenSurvey.git
    $ cd OpenSurvey
    $ . venv/bin/activate
    $ pip install -r requirements.txt

Then create a `.env` file in the base directory containing the following:

```
DATABASE_URL=[database type]://[username]:[password]@[host]:[port]/[database name]
SECRET_KEY=[random key to be used as a secret]
DEBUG=True
```
The `SECRET_KEY` can be anything, but an easy way to make something nice and random is with the `openssl` command:

    $ openssl rand -base64 64
    
Create the database if you haven't already, then allow privileges to that user on that database.

Example:

```
$ createdb opensurvey
$ createuser -P opensurvey_admin
$ psql
# GRANT ALL PRIVILEGES ON DATABASE opensurvey TO opensurvey_admin;
```

migrate the database using foreman: `foreman run python manage.py migrate`
create a superuser using foreman: `foreman run python manage.py createsuperuser`
run the project: `foreman start`
go to http://localhost:5000/admin and login with the newly-created superuser


If wanting to backup from the Heroku database and restore the data locally, the following steps work

```
$ heroku pg:backups capture
$ curl -o latest.dump `heroku pg:backups public-url`
$ pg_restore --verbose --clean --no-acl --no-owner -h localhost -U opensurvey_admin -d opensurvey  ./latest.dump
```
For more info see:

* https://gist.github.com/wrburgess/5528649
* https://devcenter.heroku.com/articles/heroku-postgres-import-export

To put the database from local dev to Heroku, do:
```
pg_dump --no-acl --no-owner -h localhost -U opensurvey_admin opensurvey | heroku pg:psql
```


Social authentication is handled with the [django-allauth](http://django-allauth.readthedocs.org/en/latest/index.html) and [django-rest-auth](http://django-rest-auth.readthedocs.org/en/latest/index.html) packages. [Configuration](http://django-allauth.readthedocs.org/en/latest/providers.html) is done within the admin site.

http://localhost:8000/accounts/facebook/login/callback/
