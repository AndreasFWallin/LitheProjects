def sing_a_song(song_path):
    """Prints song lyrics, handling errors robustly."""
    try:
        with open(song_path, "r", encoding="utf-8") as f:
            lyrics = f.read().strip() #Strip whitespace for cleaner output
            print(f"\nSinging {os.path.basename(song_path).replace('.txt', '')}:\n{lyrics}\n")
    except FileNotFoundError:
        print(f"Error: Song file '{song_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred while singing the song: {e}")

def get_song_choice(song_paths):
    """Gets song choice from user, handling invalid input and random selection."""
    if not song_paths:
        print("No songs found in the configuration file.")
        return None

    print("\nAvailable songs:")
    for i, song_path in enumerate(song_paths):
        song_name = os.path.basename(song_path).replace('.txt', '')
        print(f"{i + 1}. {song_name}")
    print(f"{len(song_paths) + 1}. Random song")

    while True:
        try:
            choice = input("Enter your choice (number or 'r' for random): ").lower()
            if choice == 'r':
                return random.choice(song_paths)
            choice = int(choice)
            if 1 <= choice <= len(song_paths):
                return song_paths[choice - 1]
            else:
                print("Invalid choice. Please enter a number from the list or 'r'.")
        except ValueError:
            print("Invalid input. Please enter a number or 'r'.")
def load_songs_from_config(config_file="config.ini"):
    """Loads song paths from a configuration file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        return list(config["songs"].values())
    except KeyError:
        return []

