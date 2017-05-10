#from htmlparser import parsehtml
from stripHTML import strip_tags
from removeStopWords import stripStopWords
import sys, threading, time
from datetime import datetime
from findMinDistance import findMinDistance
import lucene
import os
from getWordsFromText import getWordsFromText
import pickle
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
#from lucene import StandardAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
#from lucene import Document, Field
from org.apache.lucene.document import Document, Field, FieldType
#from lucene import IndexSearcher
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
#from lucene import IndexReader
from org.apache.lucene.index import IndexReader
#from lucene import QueryParser
from org.apache.lucene.queryparser.classic import QueryParser
#from lucene import SimpleFSDirectory
from org.apache.lucene.store import SimpleFSDirectory
#from lucene import Version
from org.apache.lucene.util import Version

new_urls = {}

doc_urls = pickle.load(open("doc_urls.p", "rb"))



if __name__ == '__main__':
    INDEX_DIR ="IndexFiles.index"
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    storeDir = os.path.join(base_dir, INDEX_DIR)
    if not os.path.exists(storeDir):
        os.mkdir(storeDir)
    lucene.initVM()
    src_dir = "html_files"
    indexDir = "index"
    store = SimpleFSDirectory(File(storeDir).toPath())
    analyzer = StandardAnalyzer()
    analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    #print ("Currently there are %d documents in the index..." % writer.numDocs())
    #print ("Reading lines from directory...")
    i = 0
    for l in os.listdir(src_dir):
        if l.endswith('.DS_Store'):
            continue
        num = int(l)
        l = os.path.join(src_dir, l)
        
        website = doc_urls[str(num)]
        new_urls[str(i)] = website
        print(i, website)
        print(website)
        with open(l, 'r') as myfile:
            data=myfile.read()
            print(l)
        #document, errors = parsehtml(data)
        #print(document)
        document = data
	html = document.decode('utf-8')
        tag_free = strip_tags(html)
        tag_free.encode('utf-8')
        #print(tag_free)
        #stripStopWords(data, i)
        #print(l)
        document = stripStopWords(tag_free, i)
        #print(document)
        i += 1
        #create a list of words in the document
        words = getWordsFromText(document.encode('utf-8'))
        t1 = FieldType()
        t1.setStored(False)
        t1.setTokenized(True)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)
        doc = Document()
        for word in words:
            doc.add(Field("contents", word, t1))
        #create a document to add to the index
            #print(word)
            #add a field to the document
            #field = Field("text", word.lower(), Field.Store.YES, Field.Index.ANALYZED)
            #add the field to the document
        #add the document to the index
        writer.addDocument(doc)
    #ticker = Ticker()
    print("commit index")
    #threading.Thread(target=ticket.run).start()
    writer.commit()
    writer.close()
    #ticker.tick = False
    print("done")
    

    #print ("Indexed lines from stdin (%d documents in index)" % (writer.numDocs()))
    #print ("About to optimize index of %d documents..." % writer.numDocs())
    #writer.optimize()
    #print ("...done optimizing index of %d documents" % writer.numDocs())
    #print ("Closing index of %d documents..." % writer.numDocs())
    #writer.close()
    #print ("...done closing index of %d documents" % writer.numDocs())
    pickle.dump(new_urls, open("new_urls.p","wb"), protocol=2)
    #distanceMatrix = findMinDistance(new_urls)
    #pickle.dump(distanceMatrix, open("distances.p", "wb"), protocol=2)
