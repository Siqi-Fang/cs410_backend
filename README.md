# Scraper Backend
## For developers
### Installation Guide
1. `git clone` this repository to a folder on your local machine
2.`cd` into your root folder where this repository is cloned to 
3. Download dependencies with `python3 -m pip install -r requirements.txt`
4. Create a database in the `data` folder named `database.db`. If you need to create a new table refer to db.py file.
### How to run the app
1. `cd` into `app` folder.
2. enter `flask run` on command line
3. open a browser and go to `http://localhost:5000/`

## User Manual 
### How Scraper works
You can select any combination of platforms & keywords to query from. For facebook and truth social, you will need to provide your login informations. The query for facebook and social will open a chrome window, you will see a loding sign on the tab of the application page when the scraper is running, please don't close any window when the process is not finished. After the process complete, the new data will be written to the database.

### How to Search Through the Database
Open the Search Database page and select any combinations of search terms. After you hit search, the program will search through the database to retrieve all matching results. The waiting time may vary depending on the number of result, but it should be completed under 10 seconds. 

Then a link will appear at the bottom of the page. A csv file(spreadsheet) named results will automatically be downloaded through your browser. 

### Note
For both search and scrape, it is required that you choose at least one platform and one keyword. You can leave the dates empty, if a date field is empty, we assume the start date to have the earliest possible date and end data to be today.
