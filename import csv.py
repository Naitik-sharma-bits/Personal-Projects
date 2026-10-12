import csv
import io
from datetime import datetime
from collections import defaultdict

# a. Setup: Hardcoded 30-row CSV string (25 valid, 5 dirty)
csv_data = """date,rep_name,region,product,units,unit_price
2023-01-02,Alice,North,Widget A,150,25.00
2023-01-05,Bob,South,Widget B,200,15.50
2023-01-08,Charlie,East,Widget A,100,25.00
2023-01-12,Diana,West,Widget C,50,45.00
2023-01-15,Alice,North,Widget B,120,15.50
2023-01-18,,South,Widget A,80,25.00
2023-01-20,Bob,South,Widget C,60,45.00
2023-01-22,Charlie,East,Widget A,110,25.00
2023-01-25,Diana,West,Widget B,90,15.50
2023-02-01,Alice,North,Widget A,160,25.00
2023-02-04,Bob,South,Widget C,75,45.00
2023-02-29,Charlie,East,Widget B,100,15.50
2023-02-10,Diana,West,Widget A,130,25.00
2023-02-14,Alice,North,Widget C,40,45.00
2023-02-18,Bob,South,Widget B,180,15.50
2023-02-20,Charlie,East,Widget A,115,25.00
2023-02-25,Diana,West,Widget C,55,45.00
2023-03-02,Alice,North,Widget B,140,15.50
2023-03-05,Bob,South,Widget A,105,25.00
2023-03-08,Charlie,East,Widget C,-20,45.00
2023-03-12,Diana,West,Widget A,125,25.00
2023-03-15,Alice,North,Widget B,150,15.50
2023-03-18,Bob,South,Widget C,85,45.00
2023-03-22,Charlie,East,Widget A,130,25.00
2023-03-25,Diana,West,Widget B,95,15.50
2023-04-01,Alice,North,Widget C,65,45.00
2023-04-05,Bob,,Widget A,110,25.00
2023-04-10,Charlie,East,Widget B,145,15.50
2023-04-15,Diana,West,Widget A,140,25.00
2023-04-20,Alice,North,Widget B,160,Free
2023-04-25,Bob,South,Widget C,90,45.00"""

# b. Task: Parse, clean, and reject invalid rows
valid_data = []
errors = []

reader = csv.DictReader(io.StringIO(csv_data))
for line_num, row in enumerate(reader, start=2):
    try:
        # 1. Check for missing fields
        if any(not str(val).strip() for val in row.values()):
            raise ValueError("Missing one or more fields")
        
        # 2. Validate date format and existence (catches Feb 29, 2023)
        date_val = datetime.strptime(row['date'], '%Y-%m-%d')
        
        # 3. Validate units
        units = int(row['units'])
        if units < 0:
            raise ValueError("Units cannot be negative")
            
        # 4. Validate unit price
        price = float(row['unit_price'])
        if price < 0:
            raise ValueError("Price cannot be negative")
            
        # If all checks pass, store valid row
        valid_data.append({
            'date': date_val,
            'rep_name': row['rep_name'],
            'region': row['region'],
            'product': row['product'],
            'units': units,
            'unit_price': price
        })
        
    except ValueError as e:
        errors.append({'line': line_num, 'data': list(row.values()), 'reason': str(e)})

# Compute Metrics
revenue_by_region = defaultdict(float)
units_by_rep = defaultdict(int)
units_by_month = defaultdict(int)

for row in valid_data:
    revenue = row['units'] * row['unit_price']
    revenue_by_region[row['region']] += revenue
    units_by_rep[row['rep_name']] += row['units']
    
    month_key = row['date'].strftime('%Y-%m')
    units_by_month[month_key] += row['units']

# Calculate Month-over-Month Growth
sorted_months = sorted(units_by_month.keys())
mom_growth = []
for i, month in enumerate(sorted_months):
    units = units_by_month[month]
    if i == 0:
        growth = "N/A"
    else:
        prev_units = units_by_month[sorted_months[i-1]]
        pct_change = ((units - prev_units) / prev_units) * 100
        growth = f"{pct_change:+.2f}%"
    mom_growth.append((month, units, growth))

# Output Formatting Functions
def print_separator(width=60):
    print("-" * width)

# Print Errors
print("\n[ ERROR LOG: REJECTED ROWS ]")
print_separator(75)
print(f"{'Line':<6} | {'Reason':<28} | {'Raw Data'}")
print_separator(75)
for err in errors:
    print(f"{err['line']:<6} | {err['reason']:<28} | {','.join(err['data'])}")

# Print Total Revenue by Region
print("\n\n[ TOTAL REVENUE BY REGION ]")
print_separator(35)
print(f"{'Region':<15} | {'Revenue ($)'}")
print_separator(35)
for region, rev in sorted(revenue_by_region.items(), key=lambda x: x[1], reverse=True):
    print(f"{region:<15} | ${rev:,.2f}")

# Print Top Rep by Units Sold
print("\n\n[ TOP REP BY UNITS SOLD ]")
print_separator(35)
print(f"{'Rep Name':<15} | {'Units Sold'}")
print_separator(35)
top_rep = None
for rep, units in sorted(units_by_rep.items(), key=lambda x: x[1], reverse=True):
    if not top_rep: 
        top_rep = rep
        print(f"{rep:<15} | {units}  <-- [TOP PERFORMER]")
    else:
        print(f"{rep:<15} | {units}")

# Print Month-over-Month Growth
print("\n\n[ MONTH-OVER-MONTH UNIT GROWTH ]")
print_separator(45)
print(f"{'Month':<10} | {'Total Units':<15} | {'Growth'}")
print_separator(45)
for month, units, growth in mom_growth:
    print(f"{month:<10} | {units:<15} | {growth}")
print("\n")