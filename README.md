# EMFACT 2.0

Team PowerBasic+ created EMFACT-2.0 as part of the [2015 MIT Clean Earth Hackathon][3]. The [original EMFACT software][4] was developed by NEWMOA.

## Summary

EMFACT 2.0 is built as a tool to help small and medium companies track pollutant and material flows in order to reduce waste and energy usage.

## Technical (Software) Overview

This software is built with Python/[Flask][1] and can be run locally using either NGINX or Apache. A great Flask tutorial can be found [here][2]

## Installation (Local)

### Download the source code

    >>> git clone https://github.com/dhhagan/emfact-2
    
### Install flask (within a virtual environment)

    >>> sudo virtualenv flask
    
### Install Dependancies

    >>> (venv) sudo pip install -r requirements.txt
    
### Initialize the database (set up using SQLite)

    >>> (venv) sudo python manage.py db init
    >>> (venv) sudo python manage.py db migrate
    >>> (venv) sudo python manage.py db upgrade
    
### Run the server

    >>> (venv) sudo python manage.py runserver


[1]: http://flask.pocoo.org/docs/0.10/tutorial/
[2]: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
[3]: http://cleanearthhack.mit.edu/
[4]: http://www.newmoa.org/prevention/emfact/
