import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",        
    database="estoque", 
    user="ricardo",     
    password="ricardo"  
)

cursor = conn.cursor()

# Example of creating a table
#cursor.execute("""
#    CREATE TABLE IF NOT EXISTS users (
#        id SERIAL PRIMARY KEY,
#        name VARCHAR(100),
#        age INT
#    )
#""")

# Example of inserting data
cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Jane Doe", 25))
conn.commit()

# Example of querying data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
cursor.close()
conn.close()
