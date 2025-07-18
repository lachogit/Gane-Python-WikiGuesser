from Denny import main_menu, home_screen, end_screen, get_quote, print_quote_block
from Andrey import mark_the_used_terms, sum_all_terms, delete_used_terms, remove_special_char, return_three_top_terms, secondary_user_choice
from Fabi import search_articles, calculate_frequency, rank_frequencies, select_four_articles
from Mustafa import radomize_answers, display_answers, get_user_input,check_user_answer
from Niko_Backend import use_quartiles, fade_in_music
import pygame

def main():
    player_name = home_screen()
    first_expression = main_menu()

    # user_input = ""
    used_terms = []
    user_choice_new_round = None
    user_score = 0
    double = False

    while True:
        # Usage
        fade_in_music("sounds/black-box-league-of-legends-130392.mp3", start_time=20.0, fade_duration=3.0)

        if user_choice_new_round is None:
            term = first_expression.lower()
        else:
            term = user_choice_new_round
        articles = search_articles(term)

        print()

        quote = get_quote()

        print("... while you are waiting - Did you know: ")
        print_quote_block(quote)
        print()

        frequency_dictionary = {}
        for i, article in enumerate(articles, start=1):         #Create dictionary of wordfrequency for each article
            frequency_dictionary[article] = calculate_frequency(article)
            bar = "[" + "#" * i * 3 + "-" * (len(articles) - i) * 3 + "]"
            print(f"\rLoading: {bar} {i * (100/len(articles)):.0f}%", end="")
        print()

        rank_list = rank_frequencies(frequency_dictionary, term)
        top_four_articles = select_four_articles(rank_list) # four articles with the highest frequency
        #top_four_articles = use_quartiles(rank_list)
        mapped_answer = radomize_answers(top_four_articles)
        display_answers(mapped_answer,term, top_four_articles)

        user_answer = get_user_input()
        score_this_round,double = check_user_answer(top_four_articles, mapped_answer, user_answer, double)

        pygame.mixer.init()
        pygame.mixer.music.load("sounds/collect-points-190037.mp3")
        pygame.mixer.music.play()

        user_score += score_this_round


        if score_this_round == 0:
            end_screen(player_name, user_score)
            break

        print()
        print(f"Your current score is: {user_score}")
        print()

        play_again = input("\nDo you want to play another round? (y/n): ").strip().lower()
        if play_again != 'y':
            end_screen(player_name, user_score)
            break

        input_data = frequency_dictionary
        used_terms = mark_the_used_terms(used_terms, term)
        assembled_data = sum_all_terms(input_data)
        assembled_data = delete_used_terms(used_terms, assembled_data)
        cleaned_data_without_spec_char = remove_special_char(assembled_data)
        top_three_terms = return_three_top_terms(cleaned_data_without_spec_char)
        user_choice_new_round = secondary_user_choice(top_three_terms)




if __name__ == "__main__":
    main()

