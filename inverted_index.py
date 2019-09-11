from sortedcontainers import SortedDict
import pickle
# inverted_index = {"title":{}, "body":{}, "links":{}, "refs":{}, "infobox":{}, "categories":{}}

READ_SEG_LEN = 100
'''
Inverted index structure:
{
    term: {doc_id: [], doc_id: []},
    term: {doc_id: [], doc_id: []}
}
Each list consists of frequencies: [total, title, body, links, refs, info, cat]
0: total
1: title
2: body
3: links
4: refs
5: info
6: cat
'''

# Check why everything does not print properly :(, only infobox prints)
inverted_index= SortedDict()
index = {"total":0, "title":1, "body":2, "links":3, "refs":4, "infobox":5,"categories":6}



def reset_index():
    global inverted_index
    inverted_index = SortedDict()

def get_index():
    global inverted_index
    return inverted_index


def invert_index(page):
    doc_id = page["id"]
    for section in page.keys():
        if (section == "id"):
            continue
        for word in page[section]:
            ind = index[section]
            if word not in inverted_index.keys():
                inverted_index[word] = {}
            if doc_id not in inverted_index[word].keys():
                inverted_index[word][doc_id] = [0,0,0,0,0,0,0]
            
            inverted_index[word][doc_id][ind] += 1  #Add section frequency
            inverted_index[word][doc_id][0] += 1   #Add total frequency

            
def print_index():
    for term in inverted_index.keys():
        print(term + ":\n")
        for doc_id in inverted_index[term].keys():
            print (doc_id + ":" + str(inverted_index[term][doc_id]))

def write_index_to_file(file_no):
    with open("created_files/index_"+str(file_no), "wb") as f:
        pickler = pickle.Pickler(f)
        
        for i in range(0, len(inverted_index), READ_SEG_LEN):
            pickler.dump(SortedDict({k:inverted_index[k] for k in inverted_index.islice(i, i+READ_SEG_LEN)}))
        
        

    
                
                    


            
