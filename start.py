import xml.sax
import re
import heapq
import shelve

import nltk
nltk.download('stopwords')

from parse_utils import *
from word_processing import *
from inverted_index import *
# from file_processing import *
from scalable_index import *

get_titles = shelve.open("created_files/get_titles")
Handler = ""

DATA_DUMP = "large.xml"
PAGES_PER_FILE = 400

class wikiHandler(xml.sax.ContentHandler):
    def __init__(self, index_folder):
        self.page = {"id": "", "title":"", "body":"", "links":"", "categories":"", "infobox":"", "refs":""}
        self.page_no = 0
        self.current_data = ""
        self.dictionary = {}
        self.index_folder = index_folder
        self.file_no = 0
        self.pages_so_far = 0
        self.x=0

    def reset(self):
        self.page = {"id": "", "title":"", "body":"", "links":"", "categories":"", "infobox":"", "refs":""}
        

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.current_data = tag
        self.page["id"] = str(self.page_no)
        self.x+=1
        
        
    def characters(self, content):
        if (self.current_data == "title"):
            self.page["title"]+=content
            # self.page["body"]+=content
        elif (self.current_data == "text"):
            self.page["body"]+=content
        
        
    def endElement(self, tag):
        if (tag == "page"):
            self.dictionary[self.page["id"]] = self.page["title"]
            self.page_no+=1
            self.pages_so_far+=1

            self.page["body"], self.page["infobox"] = get_infobox(self.page["body"])
            self.page["body"], self.page["categories"] = get_categories(self.page["body"])
            self.page["body"], self.page["links"] = get_links(self.page["body"])
            self.page["body"], self.page["refs"] = get_refs(self.page["body"])
            
            for section in self.page.keys():
                if (section == "id"): continue
                self.page[section] = neat_tokens(self.page[section])

            invert_index(self.page)
            self.reset()

        elif (tag == "mediawiki"):
            write_index_to_file(self.file_no)
            scale_index(self.file_no+1)
            get_titles.update(self.dictionary)
            get_titles.close()
        
        if self.pages_so_far == PAGES_PER_FILE:
            write_index_to_file(self.file_no)
            reset_index()
            self.file_no += 1
            self.pages_so_far = 0

            get_titles.update(self.dictionary)
            self.dictionary = {}
    
   
       

    

if (__name__ == "__main__"):

    parser = xml.sax.make_parser()

    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = wikiHandler("index")
    parser.setContentHandler( Handler )
    parser.parse("data_dumps/"+DATA_DUMP)

def index_wrapper(data_dump, index_folder):
    parser = xml.sax.make_parser()

    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    global Handler
    Handler = wikiHandler(index_folder)
    parser.setContentHandler( Handler )
    parser.parse(data_dump)
    

def regular_query(query):
    global Handler
    word = query[0]
    index = get_index()
    dictionary = Handler.get_dictionary()

    output_ids = heapq.nlargest(10, index["body"][word], index["body"][word].get)
    return [dictionary[output_id] for output_id in output_ids]
    
def search_wrapper(queries):
    outputs = []
    for query in queries:
        output = regular_query(query)
        outputs.append(output)
    return outputs
