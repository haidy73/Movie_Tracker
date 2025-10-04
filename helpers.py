
from config import BASE_URL, API_KEY
import requests
import re

def display_main_menu():
    print("="*10 + " Welcome to Movie Tracker " + "="*10)
    print("1. Search for a movie")
    print("2. Login")
    print("3. Register")
    print("4. Exit")
    
def display_account_menu():
    print("1. Search for a movie")
    print("2. View my lists")
    print("3. Log out")

def display_submenu():
    print("1. Rate")
    print("2. Add to \"favorites\"")
    print("3. Add to \"to watch\"")
    print("4. Go back")

def get_num(input_statement):
    """Get a number input with validation"""
    while True:
        try:
            menu_choice = int(input(input_statement))
            return menu_choice
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit()
    
def get_string():
    """Get string input with validation"""
    while True:
        try:
            movie_name = input("Movie name: ").strip()
            if movie_name:
                return movie_name
            else:
                print("Please enter a valid movie name.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit()


def get_existing_user_info():
    """Get user login credentials with validation"""
    while True:
        try:
            username = input("Username: ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            password = input("Password: ")
            if not password:
                print("Password cannot be empty.")
                continue
            return username, password
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit()
    
def get_new_user_info():
    """Get new user registration info with validation"""
    while True:
        try:
            username = input("Username: ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            if len(username) < 3:
                print("Username must be at least 3 characters long.")
                continue
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                print("Username can only contain letters, numbers, and underscores.")
                continue
                
            password = input("Password: ")
            if not password:
                print("Password cannot be empty.")
                continue
            if len(password) < 6:
                print("Password must be at least 6 characters long.")
                continue
                
            confirm_password = input("Confirm Password: ")
            if password != confirm_password:
                print("Passwords do not match.")
                continue
                
            return username, password, confirm_password
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit()

def get_rating():
    """Get movie rating from user with validation"""
    while True:
        try:
            rating = float(input("Enter your rating (0.0 - 10.0): "))
            if 0.0 <= rating <= 10.0:
                return rating
            else:
                print("Rating must be between 0.0 and 10.0")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit()

def display_movie_info(movie):

    fields = [
            ("Title", "Title"),
            ("Year", "Year"),
            ("Rated", "Rated"),
            ("Released", "Released"),
            ("Runtime", "Runtime"),
            ("Genre", "Genre"),
            ("Director", "Director"),
            ("Writer", "Writer"),
            ("Actors", "Actors"),
            ("Plot", "Plot"),
            ("Language", "Language"),
            ("Country", "Country"),
            ("Awards", "Awards"),
            ("IMDb Rating", "imdbRating"),
            ("IMDb Votes", "imdbVotes")
        ]

    print("="*60)
    print(f"🎬 {movie["Title"]} ({movie["Year"]})")
    print("="*60)

    for label, key in fields:
        value = movie[key]
        print(f"{label:<12}: {value}")

    print("="*60)

def search_movie(movie_name):
    """Search for a movie using OMDB API with error handling"""
    try:
        # URL encode the movie name to handle special characters
        import urllib.parse
        encoded_name = urllib.parse.quote(movie_name)
        url = BASE_URL + f"t={encoded_name}" + API_KEY
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        movie = response.json()
        
        # Check if movie was found
        if movie.get('Response') == 'False':
            print(f"Movie '{movie_name}' not found. Please check the spelling and try again.")
            return None
            
        return movie
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to movie database: {e}")
        return None
    except requests.exceptions.Timeout:
        print("Request timed out. Please check your internet connection and try again.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def display_user_ratings(username):
    """Display user's movie ratings"""
    import database_manager as db
    ratings = db.get_user_ratings(username)
    
    if not ratings:
        print("You haven't rated any movies yet.")
        return
    
    print(f"\n{'='*50}")
    print(f"Your Movie Ratings")
    print(f"{'='*50}")
    for movie_name, rating in ratings:
        print(f"{movie_name:<30} : {rating}/10.0")
    print(f"{'='*50}")

def display_user_list(username, list_name):
    """Display user's movie list"""
    import database_manager as db
    movies = db.get_user_list(username, list_name)
    
    if not movies:
        print(f"Your {list_name} list is empty.")
        return
    
    print(f"\n{'='*50}")
    print(f"Your {list_name.title()} List")
    print(f"{'='*50}")
    for i, movie_name in enumerate(movies, 1):
        print(f"{i}. {movie_name}")
    print(f"{'='*50}")

def clear_screen():
    """Clear the console screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

