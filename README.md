# Logs Analysis Project

This project sets up a mock PostgreSQL database for a fictional news website, assuming the frontend user-facing side and backend has been built,
and it is up and running. The provided Python script uses the psycopg2 library to query the database and produce a report that answers the following three questions:
* Most popular three articles of all time
* The most popular article authors of all time
* The days that more than 1% of requests lead to errors

## Requirement
* PostgreSQL database server
* Install [python](http://www.python.org)
* Install psycopg2 python library

## Setting up database
* connect to postgres database server `$ psql`
* create news database `create database news`
* [download data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) you will need to unzip this after downloading
* import newsdata.sql file to create schemas and seed `-d news -f newsdata.sql`
* create 2 views :

```sql
CREATE VIEW log_view AS 
SELECT (time::date) as date, COUNT(*) AS log_count 
FROM log 
GROUP BY date;

CREATE VIEW error_log_view AS 
SELECT (time::date) AS error_date, COUNT(*) as error_log_count 
FROM log 
WHERE status = '404 NOT FOUND' 
GROUP BY error_date;
```

## Running Application

* Navigate to project root `cd root-directory-path`
* Run the news_report.py class via terminal
```bash
python3 news_report.py

```
## Author
Ositadinma Tochukwu Godson