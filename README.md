# Logs Analysis Project

This project is an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like

## Setting up database
**NB**: This application uses postgres Database, so make sure you have postgres installed
* connect to postgres database server `$ psql`
* create news database `create database news`
* [download data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) you will need to unzip this after downloading
* import newsdata.sql file to create schemas and seed `-d news -f newsdata.sql`
* create 2 views :
```
create view log_view as select (time::date) as date, count(*) as log_count from log group by date;

create view error_log_view as select (time::date) as error_date, count(*) as error_log_count from log where status = '404 NOT FOUND' group by error_date;
```

## Running Application

* Install [python](http://www.python.org)
* Navigate to project root `cd root-directory-path`
* Run the news_report.py class via terminal
```
python news_report.py
```
## Author
Ositadinma Tochukwu Godson