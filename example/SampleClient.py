import xmlrpclib
import threading
import random
import string

class ThreadClass(threading.Thread):
    def run(self):
        s = xmlrpclib.ServerProxy('http://localhost:8000')
        k = 0
        while True:
            #print self.getName() + ' [' + str(i) + '] adding new news with ID: ' + str(s.add_news('tytol','Waldemar Sojka','http://localhost/news01'))
            author_id = random.randint(1, 1000)
            text = "".join([random.choice(string.ascii_letters + ' ') for i in xrange(10000)])
            title = "".join( [random.choice(string.letters) for i in xrange(20)] ).lower()
            nid = s.add_news(title, author_id, text)         
            print self.getName() + ' [' + str(k) + '] adding new news with id ' + str(nid)
            k+=1  

for k in range(20):
    ThreadClass().start()

#s = xmlrpclib.ServerProxy('http://localhost:8000')
#print s.total_news()
#for k in range(9999):
#name = "".join( [random.choice(string.letters) for i in xrange(8)] ).lower()
#email = "".join( [random.choice(string.letters) for i in xrange(8)] ).lower()
#print s.add_author(name, email + '@gmail.com')
#print "".join([random.choice(string.ascii_letters + ' ') for i in xrange(2000)])