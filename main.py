import helpers as h
import database_manager as db
from config import DATABASE_PATH

def main():
    """Main application function"""
    try:
        # Initialize database
        db.open_connection(DATABASE_PATH)
        db.setup_database()
        
        current_user = None
        
        # Main application loop
        while True:
            h.clear_screen()
            h.display_main_menu()
            choice = h.get_num("Your choice: ")

            # Search for a movie (guest mode)
            if choice == 1:
                movie_name = h.get_string()
                movie = h.search_movie(movie_name)

                if movie:
                    h.display_movie_info(movie)
                    input("\nPress Enter to continue...")
                else:
                    input("\nPress Enter to continue...")

            # Login
            elif choice == 2:
                username, password = h.get_existing_user_info()

                if db.valid_credentials(username, password):
                    current_user = username
                    print("="*20 + " Logged in successfully " + "="*20)
                    input("Press Enter to continue...")
                else:
                    print("Incorrect username or password")
                    input("Press Enter to continue...")
            
            # Register
            elif choice == 3:
                username, password, confirm_password = h.get_new_user_info()

                if db.register_user(username, password, confirm_password):
                    print("="*20 + " Registered successfully " + "="*20)
                    input("Press Enter to continue...")
                else:
                    print("Registration failed. Username may already exist or passwords don't match.")
                    input("Press Enter to continue...")

            # Exit
            elif choice == 4:
                print("Thank you for using Movie Tracker!")
                break

            else:
                print("Invalid choice")
                input("Press Enter to continue...")

            # User session loop
            while current_user:
                h.clear_screen()
                print(f"Welcome, {current_user}!")
                h.display_account_menu()
                choice = h.get_num("Your choice: ")

                # Search for a movie (logged in mode)
                if choice == 1:
                    movie_name = h.get_string()
                    movie = h.search_movie(movie_name)

                    if movie:
                        h.display_movie_info(movie)
                        h.display_submenu()

                        submenu_choice = h.get_num("Your choice: ")

                        if submenu_choice == 1:  # Rate movie
                            rating = h.get_rating()
                            if db.add_rating(current_user, movie["Title"], rating):
                                print(f"Rating of {rating}/10.0 added for {movie['Title']}")
                            else:
                                print("Failed to add rating")
                            input("Press Enter to continue...")
                            
                        elif submenu_choice == 2:  # Add to favorites
                            if db.add_to_list(current_user, "favorites", movie["Title"]):
                                print(f"{movie['Title']} added to your favorites!")
                            else:
                                print(f"{movie['Title']} is already in your favorites or failed to add.")
                            input("Press Enter to continue...")
                            
                        elif submenu_choice == 3:  # Add to watchlist
                            if db.add_to_list(current_user, "to_watch", movie["Title"]):
                                print(f"{movie['Title']} added to your watchlist!")
                            else:
                                print(f"{movie['Title']} is already in your watchlist or failed to add.")
                            input("Press Enter to continue...")
                            
                        elif submenu_choice == 4:  # Go back
                            pass
                        else:
                            print("Invalid choice")
                            input("Press Enter to continue...")
                    else:
                        input("Press Enter to continue...")
                        
                # View my lists
                elif choice == 2:
                    h.clear_screen()
                    print("My Lists:")
                    print("1. View my ratings")
                    print("2. View my favorites")
                    print("3. View my watchlist")
                    print("4. Go back")
                    
                    list_choice = h.get_num("Your choice: ")
                    
                    if list_choice == 1:
                        h.display_user_ratings(current_user)
                        input("Press Enter to continue...")
                    elif list_choice == 2:
                        h.display_user_list(current_user, "favorites")
                        input("Press Enter to continue...")
                    elif list_choice == 3:
                        h.display_user_list(current_user, "to_watch")
                        input("Press Enter to continue...")
                    elif list_choice == 4:
                        pass
                    else:
                        print("Invalid choice")
                        input("Press Enter to continue...")
                        
                # Log out
                elif choice == 3:
                    current_user = None
                    print("Logged out successfully!")
                    input("Press Enter to continue...")
                    
                else:
                    print("Invalid choice")
                    input("Press Enter to continue...")
                    
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Clean up database connection
        db.close_connection()

if __name__ == "__main__":
    main()
