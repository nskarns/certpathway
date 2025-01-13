import re
import requests
import string
import nltk
import json
import time
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


def clean_html(html):
    """
    html: the HTML string to be cleaned
    returns: clean version of page text
    https://stackoverflow.com/questions/26002076/python-nltk-clean-html-not-implemented
    """

    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'option']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def soup_parsing(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup.findAll(text=True)
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)



def get_keywords(text):
    """
    text: cleaned text to be tokenized and cleaned 
    returns: list of tokenized text with stopwords removed (the keyword list)
    """
    text = text.lower()
    # manually entered stopwords to prevent need for nltk.corpus download
    filters = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 
               'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 
               'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 
               'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 
               'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
               'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
               'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 
               'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 
               'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', 
               "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', 
               "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    filters.extend([*string.punctuation])
    
    text = word_tokenize(text)
    keywords = [word for word in text if word not in filters]
    keywords = set(keywords)
    
    # Add lexigraphically similar words 
    to_add = set()
    for word in keywords:
        similar = get_similar(word)
        for sim_word in similar:
            to_add.add(sim_word)
    
    for word in to_add:
        keywords.add(word)

    return keywords


def construct_index(KeywordMap):
    """
    input: mapping of certID to keyword
    return: inverted_index 
           an inverted index that maps each keyword to the CertID that corresponds to it. 
    """
    index = {}

    for CertID, keywords in KeywordMap.items():
        print(f"Constructing - Processing keywords for Cert {CertID}")
        for keyword in keywords:
            CertList = []
            if keyword in index:
                CertList = index[keyword]
                CertList = set(CertList)
                CertList.add(CertID)
                CertList = list(CertList)
            else:
                CertList.append(CertID)
            index[keyword] = CertList
    
    return index

def get_similar(keyword):
    similar = set()
    wordlist = wordnet.synsets(keyword)
    for word in wordlist:
        sublist = word.similar_tos()
        sublist.extend(word.also_sees())
        for similar_to in sublist:
            lemmas = similar_to.lemmas()
            for lemma in lemmas:
                similar.add(lemma.name())
                for deriv in lemma.derivationally_related_forms():
                    similar.add(deriv.name())
    return similar


def main():
        
    keyword_index = {}
    for i in range(45):       
        filepath = "info_pages/" + str(i+1) + ".htm"
        with open(filepath, 'r') as file:
            content = file.read().replace('\n', '')
        content = soup_parsing(content)

        
        keyword_index[i+1] = get_keywords(content)

        print(f"retrieved keywords for id: {i+1}")

    for key, value in keyword_index.items():
        print(f"{key} : {len(value)}")

    inverted_index = construct_index(keyword_index)
    #print(json.dumps(inverted_index, indent=4))
    print(len(inverted_index))
    with open('var/index_test.json', 'w') as fp:
        json.dump(inverted_index, fp, indent=1)

if __name__=="__main__": 
    main() 