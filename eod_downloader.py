import urllib
import urllib2
import datetime
import os

#input
last_monday_date = datetime.datetime(2017,6,5)
key = 'uj5y2eckpq'
exchange = 'AMEX'

#generate list of dates in previous week
date_list = []

for i in range(0,5):
    new_date = last_monday_date + datetime.timedelta(days=i)
    foo = new_date.strftime('%Y%m%d')
    date_list.append(foo)


#downloader



for date in date_list:
    elements = []
    elements.append(str(exchange))
    elements.append('_')
    elements.append(str(date))
    elements.append('.txt')

    url  = 'http://eoddata.com/data/filedownload.aspx?e=%s&sd=%s&ed=%s&d=9&k=%s&o=d&ea=1&p=0'%(exchange,date,date,key)
    print url

    file_name = os.path.join('C:/Users/USER/PycharmProjects/Data archives/dummy',''.join(elements))
    urllib.urlretrieve(url,file_name)




testfile = urllib.URLopener()
testfile.retrieve('http://eoddata.com/data/filedownload.aspx?e=AMEX&sd=20170608&ed=20170608&d=9&k=uj5y2eckpq&o=d&ea=1&p=0', "test.txt")