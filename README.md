![diversitechlogo](/Documents/Diversitech-Logo.jpg)

## Author
Diversitech was created by Marisha Schumacher-Hodge during her time as a Software Engineering Student at Hackbright Academy in Winter 2016. You can learn more about Marisha on her[LinkedIn profile](https://www.linkedin.com/in/marishaschumacherhodge>) and contact her directly at <marisha.schumacher.hodge@gmail.com>.

## Overview
Diversitech is considered to be "The Glassdoor for Diversity in Tech Companies". Created for job-seekers who are researching companies to work for and advocates of diversity and inclusion, this app analyzes tech companies' publically-reported gender and ethnicity diversity data, allows current and former employees to write anonymous reviews on companies, and provides the most recent news on diversity efforts within that company. Users can search for a particular company to get a visualization of all of the diversity details and overall ratings for that company. Diversitech is unique in that it compares the diversity data for all of the tech companies in order to rank the top companies for gender and ethnic diversity.

Future features for this app will include:
- Ability for users to log-in and write private messages to current and/or former employees who have written reviews.
- Ability for companies to sign-in and submit their diversity data to be able to compare their numbers to other companies.

## Tech Stack

**Server**: Python, Flask, Jinja2, Pandas

**Database**: SQL, Postgres, SQLAlchemy

**Algorithms**: Custom Algorithms for Ranking of Companies

**Frontend**: Javascript, JQuery, AJAX/JSON, Bootstrap, d3, ChartsJS, HTML5

**Testing**: Doctests and Unittest

**APIs Used**: Google News, Glassdoor


## Screenshots

### Homepage

#### Search for a company

![navhome](/Documents/Home-page.png)

#### See the Top Companies for Gender and Ethnicity

![rankings](/Documents/Top10.png)

### Diversity Data

#### Interact with the diversity charts to see the data for different roles within the company (i.e. Overall, Tech, Management)

![gender](/Documents/Gender-charts.png)

![ethnicity](/Documents/Ethnicity-data.png)

### Reviews

#### See the reviews and overall review ratings for a company, and access a featured review from Glassdoor.com

![reviews](/Documents/Reviews.png)

### News

See the most recent news stories for a company related to their diversity efforts

![navhome](/Documents/News.png)

## Run this app locally 

Create a virtualenv locally

```sh
$ virtualenv env
```
Install the requirements.txt
```sh
$ pip install -r requirements.txt
```
Create a psql database called diversity
```sh
$ createdb diversity
```
Seed the database
```sh
$ python seed.py
```

Run the server
```sh
$ python server.py
```

