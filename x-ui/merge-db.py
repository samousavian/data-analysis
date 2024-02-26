import sqlite3

# Database file paths
az_db_path = 'src.db'  # Update this with the actual path
core_db_path = 'dst.db'  # Update this with the actual path

# Connect to the databases
az_conn = sqlite3.connect(az_db_path)
core_conn = sqlite3.connect(core_db_path)

try:
    # Clear client_traffics table in both databases
    # az_conn.execute("DELETE FROM client_traffics")
    # core_conn.execute("DELETE FROM client_traffics")

    # Clear inbounds table in core.db
    # core_conn.execute("DELETE FROM inbounds")

    # Retrieve and copy inbounds data from az.db to core.db
    inbounds_rows = az_conn.execute("SELECT * FROM inbounds").fetchall()
    core_conn.executemany("INSERT INTO inbounds VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", inbounds_rows)

    # Commit changes and close connections
    az_conn.commit()
    core_conn.commit()
    print("All tasks completed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    az_conn.close()
    core_conn.close()
