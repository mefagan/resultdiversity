INDEX_DIR = "index/"
import sys
import os
from os import path
import lucene
import org.apache.lucene.analysis.standard
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
#from lucene import IndexSearcher
from org.apache.lucene.index import IndexWriter
from org.apache.lucene.index import DirectoryReader

#from lucene import IndexReader
import org.apache.lucene.index
from org.apache.lucene.index import IndexReader
from org.apache.lucene.search import IndexSearcher
#from org.apache.lucene.index import IndexReader
from java.io import File
#from lucene import QueryParser
from org.apache.lucene.queryparser.classic import QueryParser
#from lucene import SimpleFSDirectory
from org.apache.lucene.store import SimpleFSDirectory
#from lucene import Version
from org.apache.lucene.util import Version
from maxMinDispersion import calculateMaxMin
from findMaxDistance import findMaxDistance
from functionScore import functionScore
from maxCoverage import calculateMaxCoverage
import pickle
import tornado.ioloop
import tornado.web

doc_urls = pickle.load(open("doc_urls.p", "rb"))
new_urls = pickle.load(open("new_urls.p", "rb"))
distanceMatrix = pickle.load(open("distances.p", "rb"))
inv_map = dict((v, k) for k, v in doc_urls.iteritems())


def retrieveDocs(q):
    STORE_DIR ="IndexFiles.index"
    lucene.initVM()    
    analyzer = StandardAnalyzer()
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    dir  = SimpleFSDirectory(File(STORE_DIR).toPath())
    #directory = FSDirectory.getDirectory(File(STORE_DIR))
    reader = DirectoryReader.open(dir)
    #reader = IndexReader.open(SimpleFSDirectory(File("index/")))
    searcher = IndexSearcher(DirectoryReader.open(dir))
 
    query  = QueryParser("contents", analyzer).parse(q)
    #query = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer).parse(q)
    #query = QueryParser(Version.LUCENE_30, "text", analyzer).parse(q)
    MAX = 1000
    hits = searcher.search(query, MAX)
    nonDiverse = []
    docsToScores = {}
        #create a list of html files with relevant websites
    rQ = []
    print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
    for hit in hits.scoreDocs:
        print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
        #print doc.get("contents").encode("utf-8")
        #print(new_urls[str(hit.doc)])
        result = str(hit.score)+ " " + str(hit.doc) + " " + hit.toString()
        if (len(nonDiverse)<10):
            nonDiverse.append(new_urls[str(hit.doc)])
        #find the document that corresponds to the html website and append to a list for min distance
        website = new_urls[str(hit.doc)]
        #html_files numbers of the hit websites added to rQ
        rQ.append(inv_map[website])
        docsToScores[int(inv_map[website])] = hit.score
        print(inv_map[website])
    return docsToScores, rQ, nonDiverse
