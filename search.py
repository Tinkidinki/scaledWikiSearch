import pickle, heapq
from word_processing import *
import shelve
from math import *
import time

#NUMBER OF DOCS
N = 100000000

mapping = {"doc_id":0, "total":1, "title":2, "body":3, "link":4, "ref":5, "infobox":6,"category":7}

index = shelve.open("created_files/final_index")

title = shelve.open("created_files/get_titles")

def extract_regular_query(word):
    # take care of no queries also
    # extract words posting list
    # count number of docs = idf
    # return a dictionary, for each doc = log(tf)*log(N/idf)

    tf_idf_dic = {}
    try:
        posting_list = index[word]
    except Exception as e:
        return {}
    idf = len(posting_list)
    for doc_list in posting_list:
        tf_idf_dic[doc_list[mapping["doc_id"]]] = log(doc_list[mapping["total"]])*log(N/idf)
    return tf_idf_dic

def extract_field_query(field, word):
    try:
        posting_list = index[word]
    except:
        return {}
    idf = 0
    tf_idf_dic = {}
    for doc_list in posting_list:
        if doc_list[mapping[field]]:
            idf +=1
            tf_idf_dic[doc_list[mapping["doc_id"]]] = log(doc_list[mapping[field]])
    
    for doc in tf_idf_dic.keys():
        tf_idf_dic[doc]*=log(N/idf)
        
    # Find the frequencies using the mapping, take log
    # Count number of docs with word in field
    # return dictionary, for each doc = log(tf)*log(idf)
    return tf_idf_dic

def merge_lists(doc_list):
    # Argument of the form: [{doc_id: tfidf, doc_id: tfidf, doc_id: tfidf}, {}, {}]
    merged_dictionary = {}
    for d in doc_list:
        for key in d.keys():
            if key in merged_dictionary:
                merged_dictionary[key] += d[key]
            else:
                merged_dictionary[key] = d[key]

    return heapq.nlargest(10, merged_dictionary.keys(), key=lambda k: merged_dictionary[k])

def get_titles(doc_id_list):
    return [title[x] for x in doc_id_list]

def search_wrapper(query):

    doc_list = []

    terms = query.split()
    for term in terms:
        if ":" in term:
            (field, word) = term.split(":") 
            processed_list = neat_tokens(word)
            if processed_list:
                doc_list.append(extract_field_query(field, processed_list[0]))
        else:
            processed_word = neat_tokens(term)[0]
            doc_list.append(extract_regular_query(processed_word))
    
    doc_id_list = merge_lists(doc_list)
    output = get_titles(doc_id_list)

    return output

def main():
    while(True):
        print("Enter query or enter e to exit:")
        query = input()
        t = time.process_time()
        if (query=='e'):
            break
        outputs = search_wrapper(query)
        print("Time taken:", time.process_time()-t, "s")
        if (not outputs):
            print("No matching documents!\n")
        for o in outputs:
            print(o)


main()



main
