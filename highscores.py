import json
from rich.console import Console
from rich.table import Table
from rich import box
import random

FILENAME = "highscores.json"

def load_data(filename = FILENAME):
    # Highscore-Daten (Beispiel)
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def show_leaderboard(data: dict, title="🏆 Leaderboard"):
    console = Console()
    table = Table(title=title, title_style="bold magenta", box=box.ROUNDED)

    table.add_column("Rank", style="bold cyan", justify="right")
    table.add_column("Name", style="bold green")
    table.add_column("Score", style="bold yellow", justify="right")

    # Sort the data by score (descending)
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    colors = ["cyan", "green", "yellow", "magenta", "blue", "red"]

    for i, (name, score) in enumerate(sorted_data, start=1):
        color = random.choice(colors)
        table.add_row(f"[{color}]{i}[/{color}]", f"[bold {color}]{name}[/bold {color}]", f"[{color}]{score}[/{color}]")

    console.print(table)


def save_data(highscore_dict, filename = FILENAME):
    """Writes the updated highscore data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as fileobj:
        json.dump(highscore_dict, fileobj,  ensure_ascii=False, indent = 4)

    print(f"The highscores were saved successfully in {filename}.")


def main():
    data = load_data()
    user = "Dima"
    score = 5
    if user not in data or score > data[user]:
        data[user] = score
    save_data(data)


if __name__ == "__main__":
    main()