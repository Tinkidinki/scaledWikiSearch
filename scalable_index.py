import cPickle
from heapq import *


'''
Assumption: There are f files of inverted indices of the following form.
Both the outer term dictionary, and the inner posting lists are dicts.
All the terms are sorted in alphabetical order.
For field queries, ranking will have to be done at search time. 
{
    term: {doc_id: [], doc_id: []},
    term: {doc_id: [], doc_id: []}
}

Each file = file_list[no]
File pointer associated with each file = fp_list[no]
Unickler associated with each file = unpickler_list[no]
Dictionary associated with each file = dict_list[n]
Dictionary pointer associated with each file = dp_list[no]

'''



'''Merges posting lists maintaining the sorting order'''
def merge_posting_lists(list_of_dicionaries):
    #return sorted_dictionary
    pass
    


def scale_index(num_files):
    #open all files
    #load_more into all dictionaries
    #dictionary indices are all 0.
    #put the terms pointed to by the dictionary index in the heapq
    #take the smallest out, find which all were equal to that
    #increment their dicionary pointers
    #if the dictionary pointer crosses the dictionary, load more, and make the pointer 0
    #get the merged posting list, and add it to the write dictionary
    #When write dictionary gets big enough, shelve it

    #do IDF values later

    # When the dictionaries were saved, assume they were pickled in pieces, 
    # So unpickling gets out the right amount.

    #Why we don't just have a lot of files instead of this buffer thing - can't get everything to main memory. 

    
    # This heap will stores the word that each dictionary index points to
    heap = []

    # This is the write buffer for the final index
    write_buffer = {}

    # Open all the index files, and load a part of their dictionaries into the respective buffer
    # Initialise all the dicionary pointers to 0, and push their corresponding terms into the heap
    for i in range(num_files):
        fp_list[i] = open(file_list[i], 'rb')
        unpickler_list[i] = Pickle.UnPickler(fp_list[i])
        dict_list[i] = unpickler_list[i].load()
        dp_list[i] = 0
        heappush(heap, dict_list[i].keys()[0])

    
    # Collects all the posting list for a given word from all the dicionaries
    posting_lists = []

    # Keeps running till no words left in the heap
    while(heap):
        smallest_term = heappop(heap)

        #Go through the full list of buffers
        for i in range(dict_list):

            # For those whose pointers point to a term equal to the smallest term, 
            # append their dictionaries to posting list, and increment pointer
            # push the word that the pointer now points to, to the heap
            if dict_list[i].keys()[dp_list[i]] == smallest_term:
                posting_lists.append(dict_list[i][dp_list[i]])
                dp_list[i]+=1
                heappush(heap, dict_list[i].keys()[dp_list[i]])

                # If buffer is exhausted, load more from the file. 
                # If file is empty, delete the buffer
                if dp_list[i] > READ_SEG_LENGTH:
                    try:
                        dict_list[i] = unpickler_list(i).load()
                        dp_list[i] = 0
                    except EOFError as e:
                        del dict_list[i]

        #After collecting all posting lists, append to write_buffer, clear posting_lists
        write_buffer[smallest_term] = merge_posting_lists(posting_lists)
        posting_lists = []
    

        # Once, write_buffer is too big, shelve the dicionary content, and clear write_buffer
        if len(write_dicionary)> WRITE_SEG_LENGTH:
            index.upate(write_dicionary)
            write_dictionary = {}

    # Shelve the leftover write_buffer
    index.update(write_dictionary)




                    

        


        
    
    