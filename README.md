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
    python manage.py runserver

After this, you should have a running development version up and running on
http://localhost:8000

There's some test data dumped in the [_dev](_dev/) directory. Go have a look
there to get some data to play around with.

Specification & Plans
---------------------

The specification and plans are found at [spec/README.md](spec/README.md).
If you want to help out, see what's missing over there.

Deployment
----------

If you are a club or national body and want to use the software, *please*
google how to properly deploy a Django application. There's a few more things
to consider (like using a proper SQL database instead of sqlite3, and using an
SSL/TLS certificate. The latter is utterly important, as there will be
person-related information transferred on this application that you may not
want everybody to see).

License
-------

We intend to keep this all in the open, and thus all the code in here is licensed
AGPL, unless stated otherwise. For the full terms, see [LICENSE](LICENSE).


<!-- vim:set syntax=markdown tw=76 spelllang=en: -->
