# scaledWikiSearch

A search engine for large data dumps from Wikipedia. Takes as input a large data dump from Wikipedia and indexes it. After indexing, quickly returns the top 10 titles of articles that best match various types of queries. 

## Usage

- Clone the repository

    ```git clone git@github.com:Tinkidinki/scaledWikiSearch.git```

- There are two data dumps, `large.xml` and `small.xml` already available in the `data_dumps` folder. If you would prefer to run the search engine on some other Wikipedia data dump, add the `xml` file of the dump to this folder. 

- In the `start.py` file, modify the `DATA_DUMP` variable to the name of the data dump you would like to use.

- To start the indexing process:

    ```python3 start.py```
    This will cause the index to get created in the `created_files` folder. For the `large.xml` data dump, this process takes about a minute.

- To search:

    ```python3 search.py```

- You will be prompted with:

    ```Enter query or press e to exit```


## Examples

The following examples are for the `large.xml` data dump.

- Find articles that contain a certain term anywhere in the article
    - Input
        ```
        basketball
        ```
    - Output

        ```
        Time taken: 0.010598710999999872 s
        2014–15 Louisville Cardinals men's basketball team
            
        2014–15 Dayton Flyers men's basketball team
            
        2014–15 Creighton Bluejays men's basketball team
            
        Norman Powell
            
        2014–15 Villanova Wildcats men's basketball team
            
        2014–15 VCU Rams men's basketball team
            
        2014–15 Boise State Broncos men's basketball team
            
        Mike Jones (basketball, born 1965)
            
        2014–15 Nebraska Cornhuskers men's basketball team
            
        Byron Rimm II
        ```

- Queries can have multiple terms 

    - Input
        ```
        yoga swimming
        ```

    - Output
        ```
        Time taken: 0.0009433650000001403 s
        England at the 2014 Commonwealth Games
            
        Wikipedia:WikiProject Occult/Prospectus
            
        Wikipedia:WikiProject Parapsychology/Prospectus
            
        Matheus Santana
            
        Eleni Avlonitou
            
        Wikipedia:WikiProject Spam/LinkReports/mobilelandsystems.net
            
        Wikipedia:WikiProject Spam/Local/mobilelandsystems.net
            
        Wikipedia:WikiProject Spam/LinkReports/ewi2.com
            
        Wikipedia:WikiProject Spam/Local/ewi2.com
            
        Wikipedia:WikiProject Spam/LinkReports/junshiwo.com
        ```

- Find articles with certain terms only in the `infobox` field. (The available fields are `title`, `body`, `link`, `ref`, `infobox` and `category`.) 
    - Input
        ```
        infobox:weight
        ```
    - Output:
        ```
        Time taken: 0.0048827220000000615 s
        Mathews Mr Easy
            
        Vintage Ultralight SR-1 Hornet
            
        Laureen Nussbaum
            
        Harvey Manger-Weil
            
        Lucian Danilencu
            
        Marko Virtanen
            
        Little Shasta Church
            
        Risto Dufva
            
        Anthony Myles (basketball, born 1982)
            
        Pekka Tirkkonen
        ```

- A mix of field queries and regular queries
    - Input
        ```
        India category:people politics
        ```
    - Output
        ```
        Time taken: 0.021459215000000142 s
        1931 New Year Honours
            
        Anubrata Mandal
            
        Women in positions of power
            
        Indo-European migrations
            
        Loktantrik Janata Dal
            
        Wikipedia:WikiProject Spam/LinkReports/events.ccc.de
            
        Tasmina Ahmed-Sheikh
            
        Cases of political abuse of psychiatry in the Soviet Union
            
        Vivek Lall
            
        Wikipedia:Copyright problems/2014 April 26
        ```

## Behind the Scenes

### Parsing
The data dump is parsed with the help of an `XMLReader` object which takes as input a `ContentHandler` object. `wikiHandler` is the content handler present in `start.py` to handle parsing of Wikipedia data dumps. During parsing, the content is tokenized after stemming and removal of stop-words. 

### Inverted Index Creation
Several inverted indices, that is, indices that maps terms to a list of documents, while also containing information about the number of occurences of the term in each document, are created during the parsing phase. The terms in each index are alphabetically sorted.

### Merging Large Indices
Given that the content in all the indices may not fit in the RAM at once, the indices are merged using the `k-way merge` algorithm, that only loads a portion of each index, and continuously writes the sorted version into the `final_index` file.  Python `shelves` are used for the final index.

### tf-idf ranking
When a query is made, the 10 document titles that are returned are the ones with the highest `tf-idf` scores. `tf-idf` stands for `term frequency-inverse document frequency`. First, each term in the query receives an inverse-document frequency (idf), which is basically inversely proportional to the number of documents in the dump that the term occurs in. The higher the idf of a term in the query, the more important the term is. Second, for each term, a list of documents are ranked based on the frequency of occurence of the term in the document (tf). Finally, every document gets a tf-idf score: (the importance of the term itself) * (the frequency with which the term occurs in the document). The top scoring documents for all terms in the query are returned. 



