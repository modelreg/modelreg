Model Reg - the voluntary RC model registry
===========================================

We're some guys form Switzerland thinking about building some useful measure to
counter the "Drone hate" and over-reaching regulation fantasies that are
currently going on in some of our governments.

Here's a rough outline of what we're trying to build:

* A web application where people can register themselves (voluntarily, address
  verification via physical letter)
* Ability to print out a sheet with QR codes to stick to your model
  (potentially as-a-service for a small fee)
* The data will be fully encrypted. Part of the QR code URL would be a random
  key to decrypt part of your information (for example phone number and name)
* Access via QR code will also give you the ability to notify the owner if you
  found a model

This will be targeted towards recular RC clubs / plane owners, RC drone and
racing clubs etc, as they do have similar requirements/problems.

The goal is to show to the government bodies that there is already a system in
place that satisfies their *actual* requirements of criminal prosecution IF
something happens and give a reasonable alternative to the transponder idea
that DJI recently proposed (some of the guys in our civil aviation government
body are playing with that idea as well)

We're explicitly building this as free software, so clubs all over the world
could run this themselves if they want. For the same reason, we're not using
anything too new or fancy, so deployments should be simple and easy, with
only a few standard django commands.


Project status
--------------

If you see this, you're welcome to help. Not much working as of now.

Contributing
------------

Please talk to Marc Urben or David Vogt if you have an idea. Then the standard
rules apply: Fork, send a PR/MR, discuss, and we'll be happy to merge.

Development
-----------

We explicitly don't put up a complex deployment, so everyone with a bit of
Python knowledge can join in and help (or run the application for themselves).

To get started, install Python (3.5 or newer) and preferrably, create a
Virtualenv (not really necessary, if you're into development, we suggest you
look into it). Then, run the following commands to get started:

    git submodule update --init --recursive
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

After this, you should have a running development version up and running on
http://localhost:8000

There's some test data dumped in the [_dev](_dev/) directory. Go have a look
there to get some data to play around with.

Specification & Plans
---------------------

The specification and plans are found at [spec/README.md](spec/README.md).
If you want to help out, see what's missing over there.

Deployment - classic
--------------------

There are two ways of deployment: Either in a classic way, or using
Docker.

If you are a club or national body and want to use the software, *please*
google how to properly deploy a Django application.  There's a few more
things to consider (like using a proper SQL database instead of sqlite3, and
using an SSL/TLS certificate. The latter is utterly important, as there will
be person-related information transferred on this application that you may
not want everybody to see).

Deployment with Docker
----------------------

With Docker, you can just run the following commands to get started:

    docker build .
    docker run

Maybe in the future, we will also provide "official" modelreg docker images,
so you won't have to build it yourself.

The docker image provides a few points to configure the application, which
you can use if you want:

* *Volumes*:
  * You may mount the "static" directory, so you can serve it properly via a
    dedicated web server by adding the following parameters to `docker run`:
    `-v /path/to/your/modelreg_static:/usr/src/app/static`
  * If you're using SQLite (not recommended for production!), add
    `-v /path/to/your/modelreg_db:/usr/src/app/db.sqlite3`

* *Initialisation*:
  * To update the database structure (required on the first run, or after
    updates), add the following to `docker run`: `-e MIGRATE_DB=true`
  * To create an initial superuser, use the environment variables
    `SUPERUSER_NAME`, `SUPERUSER_EMAIL` and `SUPERUSER_PASSWORD`, as
    follows:
    `-e SUPERUSER_NAME=admin -e SUPERUSER_EMAIL=dave@example.org -e SUPERUSER_PASSWORD=verys3cr3t`
    If those variables are not set, we assume that you already have
    a superuser in your database.

* *Running*
  * *Database*: The Docker environment currently supports MySQL and PostgreSQL only.
    This may change in the future to support other databases as well. Pass
    the following env variables to tell the app about your DB server:
    `DB_USER`, `DB_PASSWORD`, DB_NAME`, `DB_HOST` and `DB_TYPE`.

    The `DB_TYPE` must be either the values `sqlite3` (the default), `mysql`
    or `postgresql`.

    Note: If you don't set those parameters, the default SQLite3 is used,
    which is not suitable for production use!
    `-e DB_TYPE=mysql -e DB_USER=username -e DB_PASSWORD=secretkey -e DB_NAME=modelreg -e DB_HOST=dbserver.local`

    Optionally, you can also pass the port as `DB_PORT`. IF not given, it
    will default to the database's default (5432 on PostgreSQL, 3306 for
    MySQL)

  * *Secret Key*: Django uses a secret key to encrypt cookies and
    authentication tokens. By default, it is randomly generated on startup.
    If you want to set it to a permanent value, pass it as `SECRET_KEY` env
    variable:
    `-e SECRET_KEY=ail4pulooMivu3LaiyaeB4phoDee8Ohnga6IeSheey2cohsu6i`

  * *Port*: Set the address and port to listen on by using the `ADDRPORT`
    variable: `-e ADDRPORT=localhost:8080`

  * *Debugging*: You can enable debugging by adding the following parameter:
    `-e DEBUG=true`

  * *Allowed Hosts*: Django can restrict access, so the application will
    only work on a given set of domains. This should be a comma-separated
    list of domain names:
    `-e ALLOWED_HOSTS=modelreg.example.org,www.modelreg.example.org`

ToDo
----

* Surround the QR-Code with the words "found?" and the translation to the user
  language, so the finder knows to scan the code
* Use DJango versioning for the fields address and qr-code
  * QR-Code so that all old QR-Codes can be matched to the user
  * Address, so that the admin can access the verified address and history
* QR-Code rate limiting (the user can only create one new QR-Code per day)
* QR-Code caching to not calculate it every time from scratch
* Validate postal address, during testing and development, send the validation
  code via email
* OAuth support
* Postal address add verified field
* Send a reminder (to finder and user) email (and finally close the case) if no
  messages where exchanged for some time.
* Obvious:
  * Translations
  * Make it pretty
  * Create unit tests

License
-------

We intend to keep this all in the open, and thus all the code in here is licensed
AGPL, unless stated otherwise. For the full terms, see [LICENSE](LICENSE).


<!-- vim:set syntax=markdown tw=76 spelllang=en: -->
