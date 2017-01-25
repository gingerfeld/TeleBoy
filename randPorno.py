import requests
import html_decode
import random
import re
import time


class titledLink:
    def __init__(self,title,link):
        self.title=title
        self.link=link

def getRedirectURL(startURL,historyNum):
    for i in range(1000):
        response = requests.get(startURL, allow_redirects = True)
        if(response.history):
            if(historyNum >=0):
                return response.history[historyNum]
            else:
                return response
        print('Failed to redirect ' + startURL)
    return False
    

def randNSFW():
    redirect = getRedirectURL('https://www.reddit.com/r/randnsfw/top/?sort=top&t=all',1)
    r = re.compile('reddit.com(.*?)/top/')
    m = r.search(redirect.url)
    if m:
        title = html_decode.html_decode(m.group(1))
        return titledLink(title, redirect.url)
    else:
        print("Failed NSFW: " + redirect.url)
        return False

def randPornhub():
    if(random.randint(0,1) == 1):
        startURL = 'http://www.pornhub.com/gay/random'
    else:
        startURL = 'http://www.pornhub.com/random'
    redirect = getRedirectURL(startURL,-1)
    
    r = re.compile('<title>(.*?) - Pornhub.com</title>')
    m = r.search(redirect.text)
    if m:
        title = html_decode.html_decode(m.group(1))
        return titledLink(title, redirect.url)

    else:
        print("Couldn't find title in: " + redirect.url)
        return False
def porno():
    print('Finding porno')
    message = 'Weird, there was some mistake. Try again?'

    comments = [
        'You sick freak.',
        'You pervert.',
        'You must be a pornographic connoseur.',
        'You really like that kind of thing?',
        "Everyone in it was someone's child.",
        'Have fun!',
        'Try not to go blind.',
        'How dare you.',
        'Ugh.',
        'How do you sleep at night?',
        'Who hurt you?',
        'What made you this way?',
        'Try not to get anything on the screen. I live there.',
        ]

    if random.randint(0, 1) == 0:
        randomTLink = randPornhub()
    else:
        randomTLink = randNSFW()

    randComment = comments[random.randint(0, len(comments) - 1)]

    decoded_title = html_decode.html_decode(randomTLink.title)
    
    message = html_decode.html_decode('Please enjoy [' + decoded_title + '](' + randomTLink.link + '). ' + randComment)
    return message
#print(porno())
