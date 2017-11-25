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

        conn = psycopg2.connect(self.connection_string)
        cur = conn.cursor()
        query = ("select articles.title, count(log.path) as views from log"
                 " join"
                 " articles on log.path = concat('/article/',articles.slug)"
                 " group by articles.title order by views limit 3")
        cur.execute(query)
        articles = cur.fetchall()
        print("{:^60}".format("Most popular articles of all time"))
        for article in articles:
            print("{:<30} - {:>15} views".format(article[0], article[1]))
        print("")
        cur.close()
        conn.close()

    def get_popular_author_by_article(self):
        """
            this method prints the most popular article authors of all time
        """

        conn = psycopg2.connect(self.connection_string)
        cur = conn.cursor()
        query = ("select authors.name, count(articles.title) as views"
                 " from authors"
                 " join articles on authors.id = articles.author "
                 " left join log"
                 " on log.path = concat('/article/',articles.slug)"
                 " group by authors.name order by views desc")
        cur.execute(query)
        authors = cur.fetchall()
        print("{:^65}".format("Most popular authors by articles of all time"))
        for author in authors:
            print("{:<30} - {:>20} views".format(author[0], author[1]))
        print("")
        cur.close()
        conn.close()

    def get_logged_failed_request(self):
        """
            this function prints the days that more than 1%
            of requests lead to errors
        """

        conn = psycopg2.connect(self.connection_string)
        cur = conn.cursor()
        query = ("select error_date, error_log_count, "
                 "((cast(error_log_count as FLOAT)"
                 " / cast(log_count as FLOAT)) * 100) as errors "
                 "from error_log_view join"
                 " log_view on error_date = date and "
                 "((cast(error_log_count as FLOAT) / "
                 "  cast(log_count as FLOAT)) * 100) > 1")
        cur.execute(query)
        logs = cur.fetchall()
        print("{:^40}".format("Request errors log by date"))
        for log in logs:
            print("{:<20} - {:>9}% errors".format(log[0].strftime("%B %d, %Y"),
                  round(log[2], 1)))
        cur.close()
        conn.close()

if __name__ == "__main__":

    news_report = NewsReport()

    news_report.get_popular_articles()
    news_report.get_popular_author_by_article()
    news_report.get_logged_failed_request()
