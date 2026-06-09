import sqlite3
import csv

# 1. Connect to the database
con = sqlite3.connect("sensor_data.db")
cursor = con.cursor()

# 2. Get the data and the column names
cursor.execute("SELECT * FROM sensor_data")
rows = cursor.fetchall()
column_names = [description[0] for description in cursor.description]

# ---------------------------------------------------------
# OPTION A: Save as a CSV file (Great for GitHub and Excel)
# ---------------------------------------------------------
csv_filename = "sensor_data_output.csv"
with open(csv_filename, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(column_names) # Write headers
    writer.writerows(rows)        # Write data
print(f"✅ Successfully saved data to {csv_filename}")

# ---------------------------------------------------------
# OPTION B: Save as a Markdown Table (Great for README.md)
# ---------------------------------------------------------
md_filename = "sensor_data_table.md"
with open(md_filename, 'w') as md_file:
    # Write Headers
    md_file.write("| " + " | ".join(column_names) + " |\n")
    # Write Separator
    md_file.write("|" + "|".join(["---"] * len(column_names)) + "|\n")
    # Write Rows
    for row in rows:
        # Convert None/Null values to empty strings to look cleaner
        clean_row = [str(item) if item is not None else "" for item in row]
        md_file.write("| " + " | ".join(clean_row) + " |\n")
print(f"✅ Successfully saved data to {md_filename}")

con.close()