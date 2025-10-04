import sqlite3
import bcrypt

database_connection = None
cur = None

def open_connection(db_path):
    global database_connection, cur
    database_connection = sqlite3.connect(db_path)
    cur = database_connection.cursor()

def setup_database():
    global cur
    if not cur:
        cur = database_connection.cursor()

    # Create database tables if it don't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        password TEXT
    )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            user_id INTEGER,
            movie_name INTEGER,
            rate REAL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lists (
            user_id INTEGER,
            list_name TEXT,
            movie_name TEXT, 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)
    
    # Commit creation changes 
    database_connection.commit()


def valid_credentials(username, password):
    global cur
    cur.execute(""" SELECT name, password FROM users where name = ? """, (username,))
    db_user_info = cur.fetchone()

    if db_user_info and bcrypt.checkpw(password.encode(), db_user_info[1]):
        return True
    
    return False

def register_user(username, password, confirm_password):
    global cur, database_connection
    
    # Check if user already exists
    cur.execute(""" SELECT name FROM users where name = ? """, (username,))
    db_user_info = cur.fetchone()

    if db_user_info or password != confirm_password:
        return False

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # Insert new user
    cur.execute(""" INSERT INTO users (name, password) VALUES (?, ?) """, (username, hashed_password))
    database_connection.commit()
    
    return True

def get_user_id(username):
    """Get user ID by username"""
    global cur
    cur.execute(""" SELECT id FROM users WHERE name = ? """, (username,))
    result = cur.fetchone()
    return result[0] if result else None

def add_rating(username, movie_name, rating):
    """Add or update a movie rating for a user"""
    global cur, database_connection
    user_id = get_user_id(username)
    
    if not user_id:
        return False
    
    # Check if rating already exists
    cur.execute(""" SELECT rate FROM ratings WHERE user_id = ? AND movie_name = ? """, (user_id, movie_name))
    existing_rating = cur.fetchone()
    
    if existing_rating:
        # Update existing rating
        cur.execute(""" UPDATE ratings SET rate = ? WHERE user_id = ? AND movie_name = ? """, (rating, user_id, movie_name))
    else:
        # Insert new rating
        cur.execute(""" INSERT INTO ratings (user_id, movie_name, rate) VALUES (?, ?, ?) """, (user_id, movie_name, rating))
    
    database_connection.commit()
    return True

def add_to_list(username, list_name, movie_name):
    """Add a movie to a user's list (favorites, to_watch, etc.)"""
    global cur, database_connection
    user_id = get_user_id(username)
    
    if not user_id:
        return False
    
    # Check if movie already exists in the list
    cur.execute(""" SELECT movie_name FROM lists WHERE user_id = ? AND list_name = ? AND movie_name = ? """, (user_id, list_name, movie_name))
    existing_movie = cur.fetchone()
    
    if not existing_movie:
        cur.execute(""" INSERT INTO lists (user_id, list_name, movie_name) VALUES (?, ?, ?) """, (user_id, list_name, movie_name))
        database_connection.commit()
        return True
    
    return False  # Movie already in list

def get_user_ratings(username):
    """Get all ratings for a user"""
    global cur
    user_id = get_user_id(username)
    
    if not user_id:
        return []
    
    cur.execute(""" SELECT movie_name, rate FROM ratings WHERE user_id = ? """, (user_id,))
    return cur.fetchall()

def get_user_list(username, list_name):
    """Get movies from a specific user list"""
    global cur
    user_id = get_user_id(username)
    
    if not user_id:
        return []
    
    cur.execute(""" SELECT movie_name FROM lists WHERE user_id = ? AND list_name = ? """, (user_id, list_name))
    return [row[0] for row in cur.fetchall()]

def close_connection():
    """Close database connection"""
    global database_connection
    if database_connection:
        database_connection.close()