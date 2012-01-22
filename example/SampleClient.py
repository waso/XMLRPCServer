import xmlrpclib
import threading
import random
import string
from datetime import datetime
import time

class AddAuthors(threading.Thread):
    def run(self):
        s = xmlrpclib.ServerProxy('http://localhost:8000')
        k = 0
        while True:
            #print self.getName() + ' [' + str(i) + '] adding new news with ID: ' + str(s.add_news('tytol','Waldemar Sojka','http://localhost/news01'))
            author_id = random.randint(1, 1000)
            text = "".join([random.choice(string.ascii_letters + ' ') for i in xrange(1000)])
            title = "".join( [random.choice(string.letters) for i in xrange(20)] ).lower()
            nid = s.add_news(title, author_id, text)         
            print self.getName() + ' [' + str(k) + '] adding new news with id ' + str(nid)
            k+=1

class ThreadClass(threading.Thread):
    def run(self):
        s = xmlrpclib.ServerProxy('http://localhost:8000')
        avg = [];
        for k in range(10):
            text = "".join([random.choice(string.ascii_letters + ' ') for i in xrange(1)])
            tstart = datetime.now()
            try:
                s.total_news_by_text(text)
            except:
                pass
            tend = datetime.now()
            diff = tend - tstart
            avg.append(diff.seconds)
        print (sum(avg)/len(avg))

for k in range(150):
    ThreadClass().start()
