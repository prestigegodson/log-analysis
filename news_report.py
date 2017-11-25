#!/usr/bin/env python3

import psycopg2


class NewsReport(object):
    """
        This class handles internal reporting which uses
        information from the news database to generate:
        1 most popular three articles of all time
        2 the most popular article authors of all time
        3 the days that more than 1% of requests lead to errors
    """

    def __init__(self):
        self.connection_string = "dbname=news"

    def get_popular_articles(self):
        """
            this function prints the most popular three articles of all time
        """

        query = ("""SELECT articles.title, COUNT(log.path) AS views
                    FROM log
                    join articles
                    ON log.path = concat('/article/',articles.slug)
                    GROUP BY articles.title
                    ORDER BY views DESC LIMIT 3""")
        articles = self.execute_query(query)
        print("{:^60}".format("Most popular articles of all time"))
        for title, views in articles:
            print("{:<30} - {:>15} views".format(title, views))
        print("")

    def get_popular_author_by_article(self):
        """
            this method prints the most popular article authors of all time
        """

        query = ("""SELECT authors.name, COUNT(articles.title) AS views
                    FROM authors
                    JOIN articles ON authors.id = articles.author
                    LEFT JOIN log
                    ON log.path = concat('/article/',articles.slug)
                    GROUP BY authors.name ORDER BY views DESC""")
        authors = self.execute_query(query)
        print("{:^65}".format("Most popular authors by articles of all time"))
        for name, views in authors:
            print("{:<30} - {:>20} views".format(name, views))
        print("")

    def get_logged_failed_request(self):
        """
            this function prints the days that more than 1%
            of requests lead to errors
        """

        query = ("""SELECT error_date, error_log_count,
                    ((cast(error_log_count as FLOAT)
                    / cast(log_count as FLOAT)) * 100) AS errors
                    FROM error_log_view
                    JOIN log_view
                    ON error_date = date AND
                    ((cast(error_log_count as FLOAT) /
                    cast(log_count as FLOAT)) * 100) > 1""")
        logs = self.execute_query(query)
        print("{:^40}".format("Request errors log by date"))
        for log in logs:
            print("{:<20} - {:>9}% errors".format(log[0].strftime("%B %d, %Y"),
                  round(log[2], 1)))

    def execute_query(self, query):
        """execute_query takes an SQL query as a parameter,
            executes the query and returns the results as a list of tuples.
           args:
            query - (string) an SQL query statement to be executed.

           returns:
            A list of tuples containing the results of the query.
        """
        try:
            conn = psycopg2.connect(self.connection_string)
            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            conn.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

if __name__ == "__main__":

    news_report = NewsReport()

    news_report.get_popular_articles()
    news_report.get_popular_author_by_article()
    news_report.get_logged_failed_request()
