from src.song_manager import load_songs_from_config, get_song_choice, sing_a_song

if __name__ == "__main__":
    song_paths = load_songs_from_config()
    while True:
        chosen_song_path = get_song_choice(song_paths)
        if chosen_song_path:
            sing_a_song(chosen_song_path)
        else:
            break # Exit if no songs are found

        another_song = input("Sing another song? (y/n): ").lower()
        if another_song != 'y':
            break