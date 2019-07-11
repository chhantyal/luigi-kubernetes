import csv
import time
import sqlite3
import contextlib

import luigi

from luigi.local_target import LocalTarget


@contextlib.contextmanager
def db_connect(db):
    conn = sqlite3.connect(db)
    try:
        yield conn
    finally:
        conn.close()


class DumpDatabaseTask(luigi.Task):
    date = luigi.DateParameter()

    def output(self):
        return LocalTarget(f"resources/csv/{self.date.isoformat()}.csv")

    def run(self):
        with db_connect("resources/sales.db") as conn, self.output().open("w") as f:
            cursor = conn.cursor()
            rows = cursor.execute(f"SELECT * FROM sales WHERE date_ordered='{self.date.isoformat()}'")
            writer = csv.writer(f)
            writer.writerow(["customer_id", "date_ordered", "order_value"])

            for row in rows:
                writer.writerow(row)


class LoadToAnalyticsDBTask(luigi.Task):
    date = luigi.DateParameter()

    def requires(self):
        return DumpDatabaseTask(date=self.date)

    def run(self):
        with self.input().open("r") as f, db_connect("resources/analytics.db") as conn:
            cursor = conn.cursor()
            reader = csv.DictReader(f)
            rows = [(i['customer_id'], i['date_ordered'], i["order_value"]) for i in reader]
            cursor.executemany(
                "INSERT INTO analytics (customer_id, date_ordered, order_value) VALUES (?, ?, ?);",
                rows)

            with self.output().open("w") as t_file:
                t_file.write("SUCCESS")
            conn.commit()

    def output(self):
        return LocalTarget(f"target_files/ingest_{self.date.isoformat()}.txt")


class AggregateTask(luigi.Task):
    date = luigi.DateParameter()

    def run(self):
        with db_connect("resources/analytics.db") as conn:
            cursor = conn.cursor()

            sql = f"""INSERT INTO sales_report (date, total_sales)
             SELECT date_ordered as date, sum(order_value) as total_sales FROM analytics 
             WHERE date_ordered='{self.date.isoformat()}' GROUP BY date_ordered
             """
            cursor.execute(sql)

            time.sleep(60)  # sleeping as task run is too fast ;)

            with self.output().open("w") as t_file:
                t_file.write("SUCCESS")

            conn.commit()

    def requires(self):
        return LoadToAnalyticsDBTask(date=self.date)

    def output(self):
        return LocalTarget(f"target_files/report_{self.date.isoformat()}.txt")


class SalesReport(luigi.task.MixinNaiveBulkComplete, luigi.WrapperTask):
    date = luigi.DateParameter()

    def requires(self):

        yield AggregateTask(date=self.date)
