import string
import re
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer 

stem_dict = {}

def remove_url(s):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)

def remove_punctuation(s):
    return s.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))


def remove_stop_words(words):
    stop_words = set(stopwords.words('english')) 
    return [w for w in words if not w in stop_words and len(w)>2] 

def stem(word):
    global stem_dict
    ps = PorterStemmer()
    if word in stem_dict:
        return stem_dict[word]
    else:
        stem_dict[word] = ps.stem(word)
        return stem_dict[word]

def remove_non_alpha(s):
    return re.sub("[^a-zA-Z]+", " ", s)


'''Goal: Takes a string, and returns a neat list of words'''
def neat_tokens(s):
    # s = remove_url(s)
    #print("CALLEDDDD")
    s = remove_punctuation(s)
    s = remove_non_alpha(s)
    #print(s)
    s = s.lower()
    words = s.split()
    words = remove_stop_words(words)
    words = [stem(word) for word in words]

    return words
