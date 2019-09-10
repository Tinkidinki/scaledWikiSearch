import pickle, heapq
from word_processing import *


def search_wrapper(path_to_index, queries):
    dictionary = {}
    body = {}

    with open(path_to_index+"/dictionary", 'rb') as handle:
        dictionary = pickle.load(handle)

    with open(path_to_index+"/body", 'rb') as handle:
        body = pickle.load(handle)

    with open(path_to_index+"/body", 'rb') as handle:
        body = pickle.load(handle)
    
    with open(path_to_index+"/body", 'rb') as handle:
        body = pickle.load(handle)

    outputs = []
    for query in queries:
        query = neat_tokens(query)
        word = query[0]
        output_ids = heapq.nlargest(10, body[word], body[word].get)
        output = [dictionary[output_id] for output_id in output_ids]
        outputs.append(output)
    return outputs
