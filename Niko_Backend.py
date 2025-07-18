import wikipedia
from textblob import TextBlob
from collections import Counter
import math
import random
import pygame
import time
import requests
import textwrap
from bs4 import BeautifulSoup
import re
import json
import threading
from colorama import init, Fore, Style
init(autoreset=True)

NUMBER_OF_ARTICLES = 10

def search_articles(term: str) -> list:
    """Search Wikipedia and return article titles."""
    titles = wikipedia.search(term, results=NUMBER_OF_ARTICLES)
    return titles


def get_page_content(title: str) -> str:
    """Fetch the content of a Wikipedia article by title."""
    page = wikipedia.page(title)
    return page.content


def get_page_url(title: str) -> str:
    """Get the URL of a Wikipedia article by title."""
    return wikipedia.page(title).url


def calculate_term_frequency(content: str, term: str) -> int:
    """Calculate how often a term appears in the content."""
    blob = TextBlob(content.lower())
    counter = blob.word_counts[term.lower()] if term.lower() in blob.word_counts else 0
    return counter


def analyze_articles(titles: list, term: str) -> tuple:
    """
    Return two dictionaries:
    - full noun counts per page
    - frequency of the search term (if noun) per page
    """
    dict_of_pages = {}
    dict_of_freq = {}

    term = term.lower()

    for title in titles:
        try:
            content = get_page_content(title)
            url = get_page_url(title)

            blob = TextBlob(content.lower())

            # Extract only nouns
            nouns = [word for word, tag in blob.tags if tag.startswith('NN')]
            noun_freq = dict(Counter(nouns))

            dict_of_pages[url] = noun_freq
            dict_of_freq[url] = noun_freq.get(term, 0)

        except Exception as e:
            print(f"Skipping article '{title}' due to error: {e}")

    return dict_of_pages, dict_of_freq



def use_quartiles(dict_of_freq: dict) -> dict:
    """
    Returns 4 articles at the 25th, 50th, 75th, and 100th percentile ranks.
    Based on frequency sorting, not distance to arbitrary normalized values.
    """
    if not dict_of_freq:
        return {}

    sorted_items = sorted(dict_of_freq.items(), key=lambda x: x[1])
    n = len(sorted_items)

    if n == 0:
        return {}

    # Calculate index positions (rounded down)
    q25_idx = max(0, math.floor(0.25 * (n - 1)))
    q50_idx = max(0, math.floor(0.50 * (n - 1)))
    q75_idx = max(0, math.floor(0.75 * (n - 1)))
    q100_idx = n - 1

    # Get the actual entries
    selected = {
        0.25: sorted_items[q25_idx][0],
        0.50: sorted_items[q50_idx][0],
        0.75: sorted_items[q75_idx][0],
        1.00: sorted_items[q100_idx][0],
    }

    return selected

# Function to play music
def play_music(filename="sounds/black-box-league-of-legends-130392.mp3"):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # -1 = loop forever


def handle_music_controls():
    """Runs in background thread: allows volume change or stopping music with user input."""
    while pygame.mixer.music.get_busy():
        try:
            user_input = input("Type 'q' to stop music or 'v0.1'–'v1.0' to change volume: ").strip()
            if user_input.lower() == 'q':
                pygame.mixer.music.stop()
                print("Music stopped.")
                break
            elif user_input.lower().startswith('v'):
                try:
                    volume = float(user_input[1:])
                    if 0.0 <= volume <= 1.0:
                        pygame.mixer.music.set_volume(volume)
                        print(f"Volume set to {volume:.1f}")
                    else:
                        print("Volume must be between 0.0 and 1.0")
                except ValueError:
                    print("Invalid volume format. Use e.g., v0.5")
        except EOFError:
            break  # For environments that auto-close input


def fade_in_music(file_path, start_time=20.0, fade_duration=5.0, steps=30):
    volume = 0.25
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(start=start_time)
    pygame.mixer.music.set_volume(0.15)

    for i in range(steps + 1):
        volume_adj = volume * (i / steps)  # e.g., 0.0 → 1.0
        pygame.mixer.music.set_volume(volume_adj)
        time.sleep(fade_duration / steps)



def print_quote_block(quote_string):
    """Prints the quote in block format with soft styling."""
    print(Fore.CYAN + Style.DIM)
    wrapped_lines = textwrap.wrap(quote_string, width=100)

    print("\n" + "—" * 100)
    for line in wrapped_lines:
        print(line)
    print("—" * 100 + Style.RESET_ALL + "\n")


def get_quote():
    url = "https://thequoteshub.com/api/"
    try:
        # Send a GET request to the API
        response = requests.get(url)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        full_text = soup.get_text(strip=True)

        # Use regex to extract JSON-like quote from inside the text
        match = re.search(r'{.*}', full_text)
        if not match:
            return "No quote found in response."

        quote_data = json.loads(match.group(0))

        quote = quote_data.get("text", "No quote text found.")
        author = quote_data.get("author", "Unknown")

        return f'"{quote}" — {author}'

    except requests.exceptions.RequestException as e:
        return f"Error fetching quote: {e}"
    except json.JSONDecodeError:
        return "Error parsing quote data."



def main():
    user_input = input("Please enter a search term: ")
    article_titles = search_articles(user_input)

    if not article_titles:
        print("No articles found.")
        return

    print(f"\nFound {len(article_titles)} articles. Analyzing...")

    # Analyze articles: get full noun word counts and term frequencies
    full_texts, freq_dict = analyze_articles(article_titles, user_input)

    # Print Frequncy Dictionary
    print("Frequency Dictionary:")
    print(freq_dict)

    # Filter to 4 representative articles based on quartiles
    quartile_selection = use_quartiles(freq_dict)

    # Build filtered versions of the dictionaries
    filtered_full_texts = {
        url: full_texts[url]
        for url in quartile_selection.values()
    }

    filtered_freq_dict = {
        url: freq_dict[url]
        for url in quartile_selection.values()
    }

    print(f"\nTop {NUMBER_OF_ARTICLES} nouns from each selected article (based on quartile proximity):")
    for url, word_dict in filtered_full_texts.items():
        print(f"\n{url}")
        top_10 = dict(sorted(word_dict.items(), key=lambda x: x[1], reverse=True)[:10])
        print(top_10)

    print("\nSelected articles by quartile:")
    for q, url in quartile_selection.items():
        freq = filtered_freq_dict[url]
        print(f"Quartile {q:.2f} → {url} (frequency: {freq})")

    print(filtered_freq_dict)


if __name__ == "__main__":
    main()
