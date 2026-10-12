import datetime 
from collections import defaultdict
import io
import csv

csv_data = """date,rep_name,region,product,units,unit_price
2024-01-05,Alice,North,Widget A,10,15.00
2024-01-12,Bob,South,Widget B,5,25.00
2024-01-18,Charlie,East,Widget A,8,15.00
2024-01-22,Alice,North,Widget C,12,50.00
2024-01-25,INVALID_DATE,West,Widget A,15,15.00
2024-01-28,David,West,Widget B,20,25.00
2024-02-02,Alice,North,Widget B,-5,25.00
2024-02-05,Bob,South,Widget A,14,15.00
2024-02-10,Charlie,East,Widget C,6,50.00
2024-02-14,David,West,Widget A,10,15.00
2024-02-18,Eve,North,Widget B,18,25.00
2024-02-22,Alice,North,,22,15.00
2024-02-25,Bob,South,Widget C,9,50.00
2024-03-01,Charlie,East,Widget B,11,25.00
2024-03-04,David,West,Widget C,7,50.00
2024-03-08,Eve,North,Widget A,30,15.00
2024-03-12,Alice,North,Widget B,15,25.00
2024-03-15,Bob,South,Widget A,10,15.00
2024-03-19,Charlie,East,Widget A,5,abc
2024-03-22,David,West,Widget B,13,25.00
2024-03-26,Eve,North,Widget C,8,50.00
2024-04-02,Alice,North,Widget A,25,15.00
2024-04-05,Bob,South,Widget B,16,25.00
2024-04-10,Charlie,East,Widget C,12,50.00
2024-04-14,David,West,Widget A,19,15.00
2024-04-18,Eve,North,Widget B,10,25.00
2024-04-21,Frank,,East,Widget A,5,15.00
2024-04-25,Alice,North,Widget C,7,50.00
2024-04-28,Bob,South,Widget A,21,15.00
2024-04-30,Charlie,East,Widget B,14,25.00"""
#now to handle the task
valid_rows = {}
errors = []

f = io.StringIO(csv_data)
r= csv.DictReader(f)

for ridx, row in enumerate(r,start=2):
    