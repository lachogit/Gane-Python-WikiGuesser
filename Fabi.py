import wikipedia
import spacy
from Niko_Backend import use_quartiles
import warnings

# spaCy-Modell nur einmal laden
nlp = spacy.load("en_core_web_sm")


def search_articles(term: str) -> list:
    """Take search-string as input and creates
        list of url to wikipedia-articles as output"""

    warnings.filterwarnings("ignore", message=".*features=\"lxml\".*")
    warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")

    full_article_list = wikipedia.search(term, results=10, suggestion=False)
    article_list = []
    for article in full_article_list:
        try:
            wikipedia.page(article, auto_suggest=False)
            article_list.append(article)
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError) as e:
            #print(f"{e} for {article}")
            pass

    return article_list


def calculate_frequency(article: str) -> dict:
    """
    Fetch Wikipedia article content, extract all nouns, and return a frequency dictionary.
    Only nouns (NN, NNS, NNP, NNPS) are counted.
    """
    frequency = {}
    content = wikipedia.page(article, auto_suggest=False).content
    doc = nlp(content.lower())

    # Nur Nomen extrahieren
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]

    for word in nouns:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency


def rank_frequencies(freq_list: dict, term: str) -> dict:
    """Takes dict of frequencies and returns a dict of raw frequencies
    for the search term, sorted in descending order."""


    term_dict = {}

    for article_name, freq_dict in freq_list.items():
        if term in freq_dict:
            term_dict[article_name] = freq_dict[term]
        else:
            term_dict[article_name] = 0

    term_dict = dict(sorted(term_dict.items(), key=lambda item: item[1],reverse= True))


    return term_dict


def select_four_articles(term_dict: dict) -> dict:
    """
    Selects 4 articles at different quartile ranks of frequency
    and returns a dict with 'title *** url' as keys and frequencies as values.
    """
    quartile_articles = use_quartiles(term_dict)
    result = {}

    for article in quartile_articles.values():
        try:
            url = wikipedia.page(article, auto_suggest=False).url
            key = f"{article} *** {url}"
            result[key] = term_dict[article]
        except Exception as e:
            print(f"Error retrieving page for '{article}': {e}")


    result = dict(sorted(result.items(), key=lambda item: item[1],reverse= True))
    return result

#def select_four_articles(term_dict: dict) -> dict:
#    """ Takes the dictionairy of all loaded articles
#    and selects 4 with a wide distribuition of values"""
#
#    dict_of_four = {}
#
#    counter = 0
#    for article, freq in term_dict.items():
#        if counter < 4:
#            url = wikipedia.page(article,auto_suggest=False).url
#            dict_of_four[article + " *** " + url] = freq
#            counter += 1
#
#    return dict_of_four


def main():
    warnings.filterwarnings("ignore", message=".*features=\"lxml\".*")

    term = "android"
    articles = search_articles(term)

    frequency_dictionary  = {}
    for article in articles:
        frequency_dictionary[article] = calculate_frequency(article)

    rank_list = rank_frequencies(frequency_dictionary, term)
    print(select_four_articles(rank_list))


if __name__ == "__main__":
    main()