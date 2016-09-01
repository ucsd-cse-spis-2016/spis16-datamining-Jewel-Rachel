from data import smallData
import string, pprint, numpy
from collections import defaultdict, Counter
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import wordcloudgen as wordcloud
import make_plots as plot

# Video Game Review Data: http://cses.ucsd.edu/spis/reviews_Video_Games_5.json (231,780 reviews)
# Movie Review Data: http://cses.ucsd.edu/spis/reviews_Movies_and_TV_5.json (1,697,533 reviews)
# CD Review Data: http://cses.ucsd.edu/spis/reviews_CDs_and_Vinyl_5.json (1,097,592 reviews)
# Car Review Data: http://cses.ucsd.edu/spis/reviews_Automotive_5.json (20,473 reviews)


if __name__ == "__main__":
    # pulls data from the web
    data = smallData("http://cses.ucsd.edu/spis/reviews_Movies_and_TV_5.json",75000)

    # gets word sentiment list
    ## w = get_word_weights(data)

    # makes graphs
    ## helpfulGraphs(data)
    ## wordCountGraphs(data, w[3], w[1])

    # makes predictions
    ## p = predicted(w[1], w[3]) 

    # returns most and least positive words
    ## wordSentiment = w[0]
    ## wordSentiment[:10] -- shows top 10 most positive words
    ## wordSentiment[-10:] -- shows top 10 most negative words

    # returns the number of times each word has appeared
    ## allWords = word_count_dict(data) -- ex: allWords['awesome']

    # creates a wordcloud
    ## makeWordcloud(w[0][:50]) -- makes wordcloud of 50 most positive words
    ## makeWordcloud(w[0][-50:]) -- makes wordcloud of 50 most negative words


# Wordcloud Functions

def toWordcloudForm(weightsAndWords):
    listOfDicts = []
    listOfWeightsAndWords = list(weightsAndWords)
    altered = False
    if listOfWeightsAndWords[0][0]<0:
        for p in listOfWeightsAndWords:
            p[0] *= -1
        listOfWeightsAndWords.reverse()
        altered = True
    for p in listOfWeightsAndWords:
        listOfDicts.append({"text": p[1], "weight": p[0]})
    if altered:
        for p in listOfWeightsAndWords:
            p[0] *= -1
    return listOfDicts

def makeWordcloud(listOfWeightsAndWords):
    listOfDicts = toWordcloudForm(listOfWeightsAndWords)
    t = wordcloud.TagCloud()
    print t.draw(listOfDicts)

def makeWordcloud_freq(listOfWords):
    listOfDicts = toWordcloudForm_freq(listOfWords)
    t = wordcloud.TagCloud()
    print t.draw(listOfDicts)

def toWordcloudForm_freq(listOfWords):
    dictOfWords = word_IDs(listOfWords)
    listOfDicts = []
    for p in listOfWords.keys():
        listOfDicts.append({"text": p, "weight": dictOfWords[p]})
    return listOfDicts

# WordWeight Fcns

def text_to_wordlist(text):
    r = [c for c in text if c not in set(string.punctuation)]
    rs = ''.join(r)
    rs = rs.lower()
    rs = rs.split()
    return rs

def word_count_dict(data):
    wordCountDict = defaultdict(int)
    for d in data:
        for w in text_to_wordlist(d['reviewText']):
            wordCountDict[w]+=1
    return wordCountDict
            
def word_count(data, stops):
    wordCountDict = defaultdict(int)
    for d in data:
        for w in text_to_wordlist(d['reviewText']):
            if w not in stops:
                wordCountDict[w]+=1
    wordCounts = [[wordCountDict[w],w] for w in wordCountDict]
    wordCounts.sort()
    wordCounts.reverse()
    return wordCounts

def top_words(data, stops):
    wordCounts =  word_count(data, stops)
    topWords = [w[1] for w in wordCounts[:1000]]
    return topWords

def word_IDs(topWords):
    wordId = dict(zip(topWords,range(1000)))
    return wordId

def feature(reviewText, data, topWords, wordId):
    feat = [0]*len(topWords)
    r = text_to_wordlist(reviewText)
    for w in r:
        if w in topWords:
            feat[wordId[w]] += 1
    feat.append(1) #offset
    return feat

def get_word_weights(data):
    print 'Working...'
    stops = stopwords.words('english')
    topWords = top_words(data, stops)
    print '  top_words completed'
    wordId = word_IDs(topWords)
    feat = [feature(d['reviewText'], data, topWords, wordId) for d in data]
    X = [f for f in feat]
    print '  X completed'
    y = [d['overall'] for d in data]
    print '  y completed'
    theta = numpy.linalg.lstsq(X,y)[0] # theta = (m,b)
    print '  theta completed'
    wordweights = [[theta[i],topWords[i]] for i in range(1000)]
    wordweights.sort()
    wordweights.reverse()
    print 'done'
    return (wordweights, theta, topWords, feat)

# Predictor Functions

def predictor(review, theta):
    ''' Calculates the predicted rating using the dot-product of the review feature and theta'''
    return sum(r_i*t_i for r_i,t_i in zip(review,theta))

def predicted(theta, feat):
    predicted = []
    for f in feat:
        p = predictor(f, theta)
        predicted.append(p)
    return predicted

# Discard Functions

def discardEmpty(data):
    helpful = []
    for d in data:
        if d['helpful'][1] != 0:
            helpful.append(d)
    return helpful

def discardSmall(data):
    useful = []
    for d in data:
        if d['helpful'][1] > 3:
            useful.append(d)
    return useful

# Helpfulness Functions

def getHelpfulIndex(data):
    newData = discardEmpty(data)
    good = defaultdict(int)
    all = defaultdict(int)
    amount = defaultdict(int)
    for d in newData:
        n = str(d['overall'])
        good[n] += d['helpful'][0]
        all[n] += d['helpful'][1]
        amount[n] += 1
    keys = good.keys()
    helpIndex = []
    for key in keys:
        d = {}
        d['1 rating'] = float(key)
        d['2 average votes'] = float(all[key]) / amount[key]
        d['3 percent helpful'] = float(good[key])/all[key]*100
        helpIndex.append(d)
    helpIndex.sort()
    return helpIndex

def helpfulPrep(data):
    newdata = discardEmpty(data)
    newdata = discardSmall(data)
    return newdata

def plotly_plots(data):
    data = helpfulPrep(data)
    helpIndex = getHelpfulIndex(data)
    X = [[1,h['1 rating']] for h in helpIndex]
    
    y1 = [[1,h['2 average votes']] for h in helpIndex]
    title = 'Product rating vs. average helpfulness votes per review'
    xtitle = 'Product rating'
    ytitle = 'Average helpfulness votes'
    line(X,y1,title,xtitle,ytitle)

    y2 = [[1,h['3 percent helpful']] for h in helpIndex]
    title2 = 'Product rating vs. percent rated helpful'
    xtitle2 = 'Product rating'
    ytitle2 = 'Percent rated helpful'
    line(X,y2,title2,xtitle2,ytitle2)

def helpfulGraphs(data):
    ''' Creates graphs based on the rating and the helpfulness of each review'''
    data = helpfulPrep(data)
    helpIndex = getHelpfulIndex(data)
    X = [[1,h['1 rating']] for h in helpIndex]

    # rating vs votes per review
    plt.subplot(2,2,3)
    axes = plt.gca()
    axes.set_xlim([1,5])
    y1 = [[1,h['2 average votes']] for h in helpIndex]
    plt.title('Review rating vs average votes per review')
    plt.ylabel('Average helpfulness votes')
    plt.xlabel('Rating')
    plt.plot(X, y1, color = 'red')

    #rating vs helpful percent
    plt.subplot(2,2,1)
    axes = plt.gca()
    axes.set_xlim([1,5])
    axes.set_ylim([0,100])
    y2 = [[1,h['3 percent helpful']] for h in helpIndex]
    plt.title('Review rating vs percent rated helpful')
    plt.ylabel('Percent rated helpful')
    plt.xlabel('Rating')
    plt.plot(X, y2, color = 'blue')

    #wordcount vs helpfulness
    words = getWordCounts(data)
    plt.subplot(2,2,2)
    axes = plt.gca()
    axes.set_xlim([0,1200])
    axes.set_ylim([0,1])
    x = [w[0] for w in words]
    print 'x length=', len(x)
    y = [float(r['helpful'][0])/r['helpful'][1] for r in data]
    print 'y length=', len(y)
    plt.title('wordCount vs helpfulness')
    plt.xlabel('wordCount')
    plt.ylabel('helpfulness')
    plt.scatter(x,y)

    plt.show()

# Word Count Functions

def getWordOccurrences(data):
    occurrences = []
    for d in data:
        w = text_to_wordlist(d['reviewText'])
        oc = Counter(w)
        occurrences.append(oc)
    return occurrences

def getWordCounts(data):
    wordCounts = []
    for d in data:
        w = text_to_wordlist(d['reviewText'])
        wordCount = len(w)
        wordCounts.append( (wordCount,d['overall']) )
    return wordCounts

def wordCountGraphs(data, feat, theta):
    predict = predicted(theta, feat)
    print 'predicted completed'
    wordCounts = getWordCounts(data)
    print 'wordcounts completed'
    x = [p for p in predict]
    print 'x completed'
    Y = [w[0] for w in wordCounts]
    print 'Y completed'
    axes = plt.gca()
    axes.set_ylim([0,2000])
    
    #rating vs wordcount scatter
    plt.subplot(221)
    plt.title('rating vs wordcount')
    plt.ylabel('wordcount of review')
    plt.xlabel('rating of review')
    plt.scatter(x, Y, color = 'blue')
    print 'plot completed'

    #rating vs wordcount 
    plt.subplot(224)
    plt.title('rating vs average wordcount')
    averageDict = defaultdict(int)
    for w in wordCounts:
        averageDict[str(w[0])] += w[1]
    average = []
    for i in range(1,6):
        average.append( (i,averageDict[str(i)]) )
    xa = [r[0] for r in average]
    Ya = [r[1] for r in average]
    plt.ylabel('average wordcount of reviews')
    plt.xlabel('rating of review')
    axes = plt.gca()
    axes.set_xlim([1,5])
    plt.plot(xa, Ya)

    plt.show()
