# eth_track

# Simple Github workflow
```
# Pull from master
$ git pull
# Create (-b) or switch (no -b) to another branch
$ git checkout -b <branch name>
# Make changes
$ git add .
$ git commit -m "<message>"
$ git push origin <branch name>
```



***
## Install required python libraries
```bash
$ pip install -r ./requirements.txt
```

## Setup
Before running any flask application, you need to export the flask app, to tell flask what the application is that you're running. To do this, everytime you open a new shell, enter the command:
```
$ export FLASK_APP=eth_app
```
Where eth_app is the folder of the application. 


## Database Initialization
See eth_app/schema.sql for the database schema and the script run to initialize the database (in a local instance of mysql stored in ./instances). 
```bash
$ flask init-db
```
This command will create eth_app.sql in instances folder which is your database. To start over, remove this file from instances and re run the above command. See home.py for an example of how to access the database in python


## Run the app
```bash
$ flask run
```
