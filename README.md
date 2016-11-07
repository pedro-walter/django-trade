# django-trade

A simple item trading application, designed for gaming items. Is integrated with Steam Login and has user registration using django-allauth. Includes sample items from Rocket League, probably outdated.

## Demo

You can see it in action [here](https://rocketradeweb.herokuapp.com/).

## How to install locally

1. Clone this repository
1. Install the needed software. On a Debian based system (tested on Linux Mint): 
```sudo apt-get install npm nodejs nodejs-legacy python-virtualenv```
1. Install bower: 
```sudo npm install -g bower```
1. Create a virtual environment: 
```virtualenv venv```
1. Load the environment:
```source venv/bin/activate```
1. Install dependencies
```pip install -r requirements.txt```
1. Edit django-trade/settings.py file, setting the SECRET_KEY and STEAM_API_KEY (if you plan to use this feature). You can use [this site](http://passwordsgenerator.net/) for random key.
1. Create the database
```./manage.py migrate```
1. Install bower dependencies
```./manage.py bower_install```
1. Run the development server
```./manage.py runserver```

**Have fun!**