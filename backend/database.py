import sqlite3

DATABASE_NAME = "nuvexa.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Business Information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS business_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT,
            phone TEXT,
            email TEXT,
            location TEXT,
            courses TEXT,
            fees TEXT,
            timings TEXT,
            additional TEXT
        )
    """)

    # Leads
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            course TEXT,
            enquiry TEXT,
            status TEXT DEFAULT 'New'
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        ai_response TEXT
    )
""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        course TEXT,
        appointment_date TEXT,
        appointment_time TEXT,
        status TEXT DEFAULT 'Scheduled'
    )
""")

    connection.commit()
    connection.close()