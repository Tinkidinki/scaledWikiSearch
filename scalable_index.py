import pickle
import os
from heapq import *
import shelve


READ_SEG_LEN = 100
WRITE_SEG_LEN = 100000
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
def merge_posting_lists(list_of_dictionaries):
    # The list is in the following form:
    # [{doc_id: [], doc_id: []},{doc_id: [], doc_id: []},{doc_id: [], doc_id: [], doc_id:[]}]
    #print(list_of_dictionaries)
    final_d = {}
    for d in list_of_dictionaries:
        final_d.update(d)
    sorted_keys = sorted(final_d.keys(), key=lambda x:final_d[x][0])
    final_list = []
    i = 0
    for key in sorted_keys:
        final_list.append([key])
        final_list[i].extend(final_d[key])
        i+=1

    #print(final_list)

    return final_list
    
    


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

    #final index
    index = shelve.open("created_files/final_index")
    # This heap will stores the word that each dictionary index points to
    heap = []

    # This is the write buffer for the final index
    write_buffer = {}

    #Initialise the various lists
    fp_list = []
    unpickler_list = []
    dict_list = []
    dp_list = []

    # Open all the index files, and load a part of their dictionaries into the respective buffer
    # Initialise all the dicionary pointers to 0, and push their corresponding terms into the heap
    for i in range(num_files):
        if (os.stat("created_files/index_"+str(i)).st_size):
            fp_list.append(open("created_files/index_"+str(i), 'rb'))
            unpickler_list.append(pickle.Unpickler(fp_list[-1]))
            dict_list.append(unpickler_list[-1].load())
                
            dp_list.append(0)
            heappush(heap, dict_list[-1].keys()[0])
    #         print("HEAP")
    #         print(heap)

    # print (fp_list)
    # print (dict_list)
    # print (unpickler_list)
    # print (dp_list)

    
    # Collects all the posting list for a given word from all the dicionaries
    posting_lists = []
    heap_run = 0
    # Keeps running till no words left in the heap
    while(heap):
        heap_run+=1
        smallest_term = heappop(heap)

        while(heap and heap[0] == smallest_term):
            heappop(heap)
        to_del = []

        #Go through the full list of buffers
        for i in range(len(dict_list)):
        

            # For those whose pointers point to a term equal to the smallest term, 
            # append their dictionaries to posting list, and increment pointer
            # push the word that the pointer now points to, to the heap
            # print("TOP CHECK")
            # print (heap_run)
            # print(dict_list[i])
            #print(i,len(dict_list[i]), dp_list[i])
            if dict_list[i].keys()[dp_list[i]] == smallest_term:
                posting_lists.append(dict_list[i][smallest_term])
                dp_list[i]+=1
                
                if dp_list[i] >= len(dict_list[i]):
                    try:
                        dict_list[i] = unpickler_list[i].load()
                        dp_list[i] = 0
                    except EOFError as e:
                        to_del.append(i)
                        continue

                # print("CHECKK")        
                # print(len(dict_list[i]))
                # print(dp_list[i])
                heappush(heap, dict_list[i].keys()[dp_list[i]])

                # If buffer is exhausted, load more from the file. 
                # If file is empty, delete the buffer
        
        for i in reversed(to_del):
            del fp_list[i], unpickler_list[i], dp_list[i], dict_list[i]

        # print("lengths")
        # print(len(fp_list), len(unpickler_list), len(dp_list), len(dict_list))

               

        #After collecting all posting lists, append to write_buffer, clear posting_lists
        # print ("smallest term:", smallest_term)
        # print ("posting list:", posting_lists)
        write_buffer[smallest_term] = merge_posting_lists(posting_lists)

        posting_lists = []
    

        # Once, write_buffer is too big, shelve the dicionary content, and clear write_buffer
        if len(write_buffer)> WRITE_SEG_LEN:
            index.update(write_buffer)
            write_buffer = {}

    # Shelve the leftover write_buffer
    #index.update(write_buffer)
    #print(dict(index))
    index.close()




                    

        


        
    
    