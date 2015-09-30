import random, urllib2, re, enchant
from BeautifulSoup import BeautifulSoup

global dictionary, twoGrams, threeGrams
dictionary, twoGrams, threeGrams = set([]), {}, {}
realWords = enchant.Dict('en_US')

def nextWord(a):
    return a[random.randrange(0, len(a))]

def addTextToData(s):
    global dictionary, twoGrams, threeGrams
    words = [x.lower() for x in s.strip().split() if re.match('^[a-zA-Z\.\'\,]+', x) and realWords.check(x)]
    dictionary |= set(words)
    for i in range(1, len(words)):
        if words[i - 1] in twoGrams:
            twoGrams[words[i - 1]].append(words[i])
        else:
            twoGrams[words[i - 1]] = [words[i]]

    for i in range(2, len(words)):
        index = words[i - 2] + ' ' + words[i - 1]
        if index in threeGrams:
            threeGrams[index].append(words[i])
        else:
            threeGrams[index] = [words[i]]

def makeSentence(firstWord):
    if not firstWord in twoGrams:
        return
    secondWord = nextWord(twoGrams[firstWord])
    sentence = [firstWord, secondWord]
    for i in range(10 + random.randrange(0, 20)):
        index = ' '.join(sentence[-2:])
        if index in threeGrams:
            sentence.append(nextWord(threeGrams[index]))
        elif sentence[-1] in twoGrams:
            sentence.append(nextWord(twoGrams[sentence[-1]]))
        else:
            break
    print ' '.join(sentence)
    print

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

page = urllib2.urlopen('http://alexekoren.com')

urlStack = ['http://metrolyrics.com']
checkedStack = []
while len(urlStack) > 0:
    url = urlStack[0]
    urlStack = urlStack[1:]
    #print url
    checkedStack.append(url)

    try:
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)
        for link in soup.findAll('a'):
            href = link.get('href')
            if not href:
                continue
            if href[:4] == 'http' and not href in checkedStack:
                urlStack.append(link.get('href'))
        text = soup.find(id='lyrics-body')
        if not text:
            continue
        if len(text) == 0:
            continue
        text = text.findAll(text=True)
        lines = []
        for line in text:
            lines.append(unicode(line.string).strip())
        for x in range(len(lines) - 1):
            if len(lines[x]) > 5:
                addTextToData(lines[x])
            '''if len(lines[x + 1]) == 0:
                if not lines[x]:
                    continue
                addTextToData(lines[x])'''
        if len(lines[-1]) > 0:
            addTextToData(lines[-1])
        firstWord = random.sample(dictionary, 1)[0]
        makeSentence(firstWord)
    except urllib2.HTTPError:
        continue
        
        
