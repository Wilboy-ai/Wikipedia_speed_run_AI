from bs4 import BeautifulSoup as bs
import requests
import urllib
from urllib.request import Request, urlopen
import re
import numpy as np

import wikipedia


def get_text_from_link(url):

    words = []
    # Global feature vector
    feature_vector = []

    html = urlopen(url).read()
    soup = bs(html, "html.parser")

    for script in soup(["script", "style"]):
        script.decompose()
    strips = list(soup.stripped_strings)

    for s in strips:
        ss = list(s.split(' '))
        for word in ss:
            if word.isalnum():
                words.append(word)

    # Vocabulary
    vocab = list(set(words))

    # Create feature vector
    for word in vocab:
        c = words.count(word)
        feature_vector.append((word,c))

    feature_vector.sort(key=lambda x:x[1], reverse=True)

    return feature_vector, vocab


def get_BOW_target_feature(search_word):
    result = wikipedia.search(search_word)
    text = wikipedia.summary(result[0], sentences=5)
    text = text.split()

    vocabulary = list(set(text))

    feature_vector = []
    for word in vocabulary:
        count_word = text.count(word)
        feature_vector.append(count_word)
        # print(str(word) + ": " + str(count_word))

    return vocabulary, feature_vector


def get_BOW_feature(search_word, vocabulary):
    result = wikipedia.search(search_word)
    text = wikipedia.summary(result[0], sentences=5)
    text = text.split()

    feature_vector = []
    for word in vocabulary:
        count_word = text.count(word)
        feature_vector.append(count_word)

    return feature_vector


def bow_dist(feature_vector, target_vector):
    diff = 0

    for i in range(len(feature_vector)):
        diff += abs(feature_vector[i] - target_vector[i])

    return diff


def get_wiki_sites(site):
    res = requests.get(site)
    soup = bs(res.text, "html.parser")
    links = []

    filter = ['File', '.png', 'http://', 'https://', 'ISBN', '%', 'Talk:', 'Portal:', 'Special:', 'Help:', 'Category:',
              'Main_Page', 'Wikipedia:', '(identifier)', 'Terms_of_Use', 'Privacy_policy', 'Cookie_statement', '#', '(',
              'Template:']

    for link in soup.find_all("a"):
        url = link.get("href", "")
        if "/wiki/" in url:
            add_wiki = True
            for word in filter:
                if word in url:
                    add_wiki = False
            if add_wiki:
                links.append(url)

    return list(set(links))  # Remove duplicates


def wiki_speed_run_bot():
    # Start site
    start_site = 'https://en.wikipedia.org/wiki/Klára_Fehér'
    # Target site
    target_site = 'https://en.wikipedia.org/wiki/Odense'

    vocabulary, target_vector = get_BOW_target_feature('Klára_Fehér')

    # Start links
    links = get_wiki_sites(start_site)
    # Sites that have already been visited, avoid cycles
    Visited_sites = []
    # Sites to be visited
    queue_sites = links

    while queue_sites:
        site = queue_sites[0]
        print("Searching site: " + site)
        print("VS: " + str(len(Visited_sites)) + ", queue_sites: " + str(len(queue_sites)))

        Visited_sites.append(site)
        links = get_wiki_sites('https://en.wikipedia.org' + site)

        for link in links:
            if link not in Visited_sites:
                queue_sites.append(link)

        if 'https://en.wikipedia.org' + site == target_site:
            print("Found site: " + target_site)
            break

        queue_sites.pop(0)

    for link in Visited_sites:
        print(link)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # wiki_speed_run_bot()

    # vocabulary, target_vector = get_BOW_target_feature('Mario')
    get_text_from_link('https://en.wikipedia.org/wiki/Bundle_adjustment')

    # feature_vector = get_BOW_feature('Bowser', vocabulary)
    # dist = bow_dist(feature_vector, target_vector)
    # print(dist)
