# Movie Tracker

A Python-based movie tracking application that allows users to search for movies, rate them, and maintain personal lists of favorites and watchlists.

## Features

- **Movie Search**: Search for movies using the OMDB API
- **User Authentication**: Secure user registration and login with password hashing
- **Movie Rating**: Rate movies on a scale of 0.0 to 10.0
- **Personal Lists**: 
  - Favorites list
  - To-watch list
- **User Dashboard**: View your ratings and lists
- **Guest Mode**: Search movies without logging in

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

### Main Menu Options:
1. **Search for a movie** - Search and view movie details (guest mode)
2. **Login** - Log in to your account
3. **Register** - Create a new account
4. **Exit** - Close the application

### Logged-in User Options:
1. **Search for a movie** - Search movies and add them to your lists or rate them
2. **View my lists** - View your ratings, favorites, and watchlist
3. **Log out** - Return to main menu

### Movie Actions (when logged in):
1. **Rate** - Rate the movie (0.0 - 10.0)
2. **Add to favorites** - Add movie to your favorites list
3. **Add to watchlist** - Add movie to your to-watch list
4. **Go back** - Return to previous menu

## File Structure

- `main.py` - Main application entry point
- `config.py` - Configuration settings
- `database_manager.py` - Database operations and user management
- `helpers.py` - Utility functions and UI helpers
- `users.db` - SQLite database file (created automatically)
- `requirements.txt` - Python dependencies

## Database Schema

### Users Table
- `id` - Primary key
- `name` - Username
- `password` - Hashed password

### Ratings Table
- `user_id` - Foreign key to users table
- `movie_name` - Movie title
- `rate` - User's rating (0.0 - 10.0)

### Lists Table
- `user_id` - Foreign key to users table
- `list_name` - Type of list (favorites, to_watch)
- `movie_name` - Movie title

## Security Features

- Password hashing using bcrypt
- Input validation and sanitization
- SQL injection prevention with parameterized queries
- Error handling for network requests

## API

This application uses the OMDB API for movie data. The API key is included in the configuration file.

## Requirements

- Python 3.6+
- Internet connection for movie searches
- Required packages listed in `requirements.txt`

## Error Handling

The application includes comprehensive error handling for:
- Network connectivity issues
- Invalid user input
- Database operations
- API failures
- Keyboard interrupts (Ctrl+C)

## Future Enhancements

Potential improvements could include:
- Movie recommendations
- Social features (sharing lists)
- Export/import functionality
- Advanced search filters
- Movie reviews and comments
- Integration with other movie databases

