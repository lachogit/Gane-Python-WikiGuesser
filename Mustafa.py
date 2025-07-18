import random
from colorama import init, Fore, Style
init(autoreset=True)

score = 0

def main():
    top_four_articles ={"Eins":100,"Zwei":80,"Drei":60,"Vier":40}
    mapped_answer = radomize_answers(top_four_articles)
    display_answers(mapped_answer)
    user_answer = get_user_input()
    new_score = check_user_answer(top_four_articles,mapped_answer, user_answer, score)
    print(new_score)



def radomize_answers(top_four_articles: dict) -> dict:
    """Takes sorted answers and returns radomized answerorder with letters A-D"""
    sortierte_liste = list(top_four_articles.keys())

    # 2. Liste aller Artikel (unsortiert)
    unsortierte_liste = sortierte_liste
    random.shuffle(unsortierte_liste)

    # Mapping
    mapped_answers = {}
    mapped_answers[unsortierte_liste[0]] = "A"
    mapped_answers[unsortierte_liste[1]] = "B"
    mapped_answers[unsortierte_liste[2]] = "C"
    mapped_answers[unsortierte_liste[3]] = "D"

    return mapped_answers

def display_answers(mapped_answers, term,top_four_articles ):
    """Displays answeroptions"""
    frequencies = list(top_four_articles.values())

    print()
    print(Fore.GREEN + Style.BRIGHT +  f"Arrange these for articles in descending order sorted by the frequency of the word {term}")
    print(f"The word appears {Fore.GREEN}{frequencies[0]}, {Fore.GREEN}{frequencies[1]}, {Fore.GREEN}{frequencies[2]}{Style.RESET_ALL} and {Fore.GREEN}{frequencies[3]}{Style.RESET_ALL} times")
    print()
    for article, letter in mapped_answers.items():
        print(f"{letter} : {article}")

def get_user_input():
    # 5. Nutzer-Eingabe als String (z. B. "BADC")


    user_input = input("Enter your ranking (ex. BADC): ").upper()

    return user_input

def check_user_answer(top_four_articles,mapped_answer, user_answer, double):
    last_answer_all_correct = double
    score_for_this_round = 0

    sortierte_liste = list(top_four_articles.keys())

    # 4. Extrahiere das korrekte Ranking (z. B. ['B', 'A', 'D', 'C'])
    korrektes_ranking = [mapped_answer[artikel] for artikel in sortierte_liste]
    # 6. Umwandeln in Liste: ['B', 'A', 'D', 'C']
    user_ranking = list(user_answer)

    # 7. Vergleich
    if user_ranking == korrektes_ranking:
        print(Fore.GREEN + Style.BRIGHT + "Every answer is correct! You will get double the points for the next round!")
        double = True
        score_for_this_round = 4 + 3 + 2 + 1
    else:
        print(Fore.RED + Style.BRIGHT + "Wrong answer!")
        print("\nYour Ranking:", user_ranking)
        print("\nCorrect Ranking:", korrektes_ranking)
        double = False
        for i in range(4):
            if user_ranking[i] == korrektes_ranking[i]:
                score_for_this_round += (4 - i)

    if last_answer_all_correct == True:
        score_for_this_round = score_for_this_round * 2
    else:
        pass

    print(f"Points this round: {score_for_this_round}")

    return score_for_this_round, double


if __name__ == "__main__":
    main()


