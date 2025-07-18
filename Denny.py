import time
import sys
from colorama import init, Fore, Style
init(autoreset=True)
import re
import pygame
from highscores import load_data, save_data, show_leaderboard
from Niko_Backend import handle_music_controls, play_music, fade_in_music, print_quote_block, get_quote


def home_screen():
    """Main screen where the user starts the game"""
    import time
    with open("wiki_guesser_ascii.txt", "r", encoding="utf-8") as file:
        ascii_text = file.read()
    print()
    for i in range(21):
        bar = "[" + "#" * i + "-" * (20 - i) + "]"
        print(f"\rLoading: {bar} {i * 5}%", end="")
        time.sleep(0.1)
    print()
    intro = "\n***** Welcome to *****"
    welcome_text(intro, delay= 0.2)
    print(ascii_text)

    pygame.mixer.init()
    pygame.mixer.music.load("sounds/mixkit-completion-of-a-level-2063.wav")
    pygame.mixer.music.play()

    # Wait until it's done
    while pygame.mixer.music.get_busy():
        continue



    print(Fore.GREEN + "  --- Made by Besserguesser ---")

    name_input = input("\nWhat is your name? ")
    print(f"\n          Hi, {Fore.GREEN + name_input + Style.RESET_ALL}! Thank you for playing Wikiguesser! :)")

    # Usage
    fade_in_music("sounds/black-box-league-of-legends-130392.mp3", start_time=20.0, fade_duration=3.0)

    welcome_text(text, 0.02)
    return name_input


def welcome_text(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

text ="""
    You think you can guess where a word shows up the most? Let’s find out.

    Here’s how it works:
    You’ll be given a word that appears in four different Wikipedia articles.
    Your job? Rank those articles from most to least based on
    how often you think the word appears in each one.

    Sounds easy, right? Well… here’s the twist:
    You only score points for every correct ranking.
    The first correct guess grants you 4 points,
    the second correct guess grants you 3 points etc.

    That means if you get all guesses correct you have 10 points
    and in the next round you score double the amount of points!
    But the moment you get zero correct guesses—
    GAME OVER.

    Your best score will be saved on the scoreboard, so aim high and go all in!
    Ready to play?
    """


def start_game():
    """Start of the actual game"""
    print(Fore.GREEN + Style.BRIGHT + "\n     So you want to play a game ?")
    first_expression = str(input(Style.RESET_ALL + "\nName an expression you want to start with: "))
    if first_expression:
        return first_expression

def update_highscore(user_name: str, score: int):

    data = load_data()

    users = data.keys()
    if user_name not in users:
        data[user_name] = 0

    current_score = data[user_name]
    if score > current_score:
        data[user_name] = score
        print("Congratulations! You achieved a NEW HIGHSCORE!")

    save_data(data)

    return current_score

def end_screen(user_name: str, score: int):
    """Ending of the game"""

    print(Fore.RED + Style.BRIGHT + "      *****GAME OVER*****")
    update_highscore(user_name, score)
    data = load_data()
    best_score = data[user_name]
    print(f"\n     Your best score is: {best_score} !")
    credits(credit_lines, delay=0.05)


def credits(credit_lines, delay=0.05):
    for color, text in credit_lines:
        for char in text:
            sys.stdout.write(color + char)
            sys.stdout.flush()
            time.sleep(delay)
        print()


credit_lines = [
    (Fore.WHITE, "\nThank you for playing Wikiguesser!\n"),
    (Fore.WHITE, "Your Wikiworkers were:\n"),
    (Fore.RED, "Fabi aka The Brain\n"),
    (Fore.BLUE, "Niko aka The Hacker\n"),
    (Fore.CYAN, "Andrey aka The Visionary\n"),
    (Fore.YELLOW, "Mustafa aka The Strategist\n"),
    (Fore.GREEN, "Denny aka Frontend in spe\n")
]


def main_menu():
    """Player actions to choose"""

    print(Fore.GREEN + "1." + Style.RESET_ALL + " Start Game")
    print(Fore.GREEN + "2." + Style.RESET_ALL + " View Scoreboard")
    print(Fore.GREEN + "3." + Style.RESET_ALL + " Exit")

    while True:
        try:
            choice = int(input(Fore.GREEN + "\nWhat would you like to do? "))
            if choice == 1:
                first_expression = start_game()
                print(f"\nYou started a round with: {first_expression}")

                return first_expression
            elif choice == 2:
                data = load_data()
                show_leaderboard(data)

            elif choice == 3:
                print(Fore.GREEN + "\n     Goodbye!")
                exit()
            else:
                print("Invalid choice. Please choose 1, 2, or 3.")
        except ValueError:
            print("\nThat's not a valid choice. Please try again.")


def main():
    home_screen()
    main_menu()
    quote = get_quote()
    print_quote_block(quote)


if __name__ == "__main__":
    main()
