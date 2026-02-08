import duckdb

# Open your exact database file
con = duckdb.connect(r"E:\llama_duckdb_project\my_project.duckdb")

# List all tables (DuckDB native way)
tables = con.execute("SHOW TABLES").fetchdf()
print("Tables in database:")
print(tables)

# Alternative: more detailed
print("\nAll relations:")
print(con.execute("SELECT * FROM duckdb_tables()").fetchdf())

# Try to describe the table if it exists
try:
    print("\nSchema of 'assessments' (or closest match):")
    print(con.execute("DESCRIBE assessments").fetchdf())
except Exception as e:
    print("Error describing 'assessments':", e)

# Case variants to check
for name in ["assessments", "Assessments", "ASSESSMENTS"]:
    try:
        count = con.execute(f"SELECT COUNT(*) FROM \"{name}\"").fetchone()[0]
        print(f"Table '{name}' exists with {count} rows!")
    except:
        pass

con.close()