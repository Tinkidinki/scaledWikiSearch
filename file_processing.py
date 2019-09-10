import pickle


# '''Writes the inverted index to the correct file'''
# def write_index_to_file(index):
#     for section in index.keys():
#         with open(section, "a") as f:
#             for word in index[section].keys():
#                 f.write(word+": ")
#                 for id in index[section][word].keys():
#                     f.write(id+" "+str(index[section][word][id])+" ")
#                 f.write("\n")



'''Merges files'''


def write_index_to_file(index, index_folder):
    for section in index.keys():
        with open (index_folder+"/"+section, "wb") as f:
            pickle.dump(index[section], f, pickle.HIGHEST_PROTOCOL)

def write_dic_to_file(dic, index_folder):
    with open (index_folder+"/dictionary", "wb") as f:
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)