# Scraper Backend
## For developers
### Installation Guide
1. `git clone` this repository to a folder on your local machine
2.`cd` into your root folder where this repository is cloned to 
3. Download dependencies with `python3 -m pip install -r requirements.txt`
4. Create a database in the `data` folder named `database.db`. If you need to create a new table refer to db.py file.
5. Username, Password, local database path and chrome driver path need to be provided with in an `.env` file.
### How to run the app
1. `cd` into root folder.
2. enter `flask run` 
3. open a browser and go to `http://localhost:5000/`

### Note & Common Errors
- We advise against running the fb scraper since it might result in your account being blocked.

- Note that we use [Blueprint](https://flask.palletsprojects.com/en/2.2.x/blueprints/), so you won't be able to run individual scripts without using some testing framwork.

- Make sure chromedriver path matches, and you are using the correct version for your browser.

- Website updates may result in errors in scraping. 
