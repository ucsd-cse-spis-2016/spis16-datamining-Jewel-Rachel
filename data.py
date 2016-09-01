import urllib

def parseData(fname):
    for l in urllib.urlopen(fname):
        yield eval(l)

def smallData(fname, size):
    print 'Reading data...'
    gen = parseData(fname)
    data = []
    for i in range(size):
        data.append(gen.next())
    print 'done'
    return data

def allData(fname):
    print 'Reading data...'
    data = list(parseData(fname))
    print "done"
    return data
