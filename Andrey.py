

def mark_the_used_terms(used_terms, user_input):
    """Safe and collect used terms in the separate list"""
    used_terms.append(user_input)
    return used_terms


def sum_all_terms(nested_dictionary):
    """Assemble all terms from nested dictionary data into simple dictionary data"""
    assemble_data = {}

    for url, terms in nested_dictionary.items():
        for term, frequency in terms.items():
            if term in assemble_data:
                assemble_data[term] += frequency
            else:
                assemble_data[term] = frequency

    return assemble_data


def delete_used_terms(used_terms, assemble_data):
    """Delete already used terms.
    Should return cleaned dictionary."""

    for term in used_terms:
        if term in assemble_data:
            del assemble_data[term]

    return assemble_data

def remove_special_char(assemble_data):
    """Remove special characters from dictionary.
    Should return cleaned dictionary"""

    special_characters = {"-", ":", "+", "*", "=", "/", "%", "@", "$", "!", "§", "(", ")", "?", "#", ";"}
    cleaned_data_without_spec_char = {}
    for key, value in assemble_data.items():
        cleaned_key = "".join(char for char in key if char not in special_characters)
        cleaned_data_without_spec_char[cleaned_key] = value

    return cleaned_data_without_spec_char

def return_three_top_terms(cleaned_data_without_spec_char):
    """return a list with top three terms/ keys with the highest frequencies from assemble dictionary """
    top_three_terms = sorted(cleaned_data_without_spec_char.keys(), key=lambda term: cleaned_data_without_spec_char[term], reverse=True)[:3]
    return top_three_terms

def secondary_user_choice(top_three_terms):
    choice_of_user_term = input(f"Please choose one of the related term: {top_three_terms[0]}, {top_three_terms[1]} or {top_three_terms[2]} or a new word:")
    print(f"You have entered: {choice_of_user_term}")
    return choice_of_user_term


def main():
    user_input = ""
    used_terms = []

    used_terms = mark_the_used_terms(used_terms, user_input)
    assembled_data = sum_all_terms(input_data)
    assembled_data = delete_used_terms(used_terms, assembled_data)
    cleaned_data_without_spec_char = remove_special_char(assembled_data)
    top_three_terms = return_three_top_terms(cleaned_data_without_spec_char)
    secondary_user_choice(top_three_terms)



if __name__ == "__main__":
    main()