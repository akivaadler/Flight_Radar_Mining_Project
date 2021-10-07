# Establish a connection
import pymysql.cursors
import pandas as pd
from IPython.display import display

def get_connection():
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='SGT2020!',
                             db='flight_radar',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)

    cur = connection.cursor()
    return cur


def execute_and_display(cur, query, number_of_rows=10):
  f"""
  Execute the query and display up to {number_of_rows} rows from the results
  as a table.
  """
  cur.execute(query)
  result = cur.fetchmany(size=number_of_rows)
  display(pd.DataFrame(result))

q1 = 'delete from airline where airline_id = 1 ;'
q2 = "select * from airline;"
cur = get_connection()
execute_and_display(cur, q1)
execute_and_display(cur, q2)


def get_query(choice, request):
    if choice ==
