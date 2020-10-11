# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import re
from unittest import result
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory:
    def __init__(self, guid, title, description, link, pubDate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubDate
    
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description

    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Takes Phrase

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        if not self.valid_phrase(phrase):
            raise Exception(f"{phrase} is an Invalid Phrase")

        self.phrase = phrase.lower()

    def is_phrase_in(self, text):

        # Remove punctuation
        text = re.sub(fr"[{string.punctuation}]+", " ", text)
        
        # Remove whitespace
        text = re.sub("\s{2,}", " ", text)

        # Lowercase
        text = text.lower()
        # Check for phrase in text
        return re.match(f".*{self.phrase}(\s|$)", text) is not None

    def valid_phrase(self, phrase: str):
        # NOT:
        # Contains punctuation
        # Contains multiple spaces
        hasPunctuation = lambda w: any(c in string.punctuation for c in w)
        hasSpaces = lambda w: re.match(".*\s{2,}", w)
        if hasPunctuation(phrase) or hasSpaces(phrase):
            print(f"{phrase} is an invalid phrase.")
            return False

        return True

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story: NewsStory):
        return self.is_phrase_in(story.get_title())
        
# story = NewsStory('', 'Purple!!! Cow!!!', '', '', datetime.now())
# x = TitleTrigger('PURPLE COW')
# print(x.evaluate(story))
# exit()

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story: NewsStory):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, datestring):
        date = datetime.strptime(datestring, r"%d %b %Y %H:%M:%S")
        date = date.replace(tzinfo=pytz.timezone("EST"))
        self.date = date

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story: NewsStory):
        storyDate = story.get_pubdate()
        storyDate = storyDate.replace(tzinfo=pytz.timezone("EST"))
        if storyDate < self.date:
            return True
        return False

class AfterTrigger(TimeTrigger):
    def evaluate(self, story: NewsStory):
        storyDate = story.get_pubdate()
        storyDate = storyDate.replace(tzinfo=pytz.timezone("EST"))
        if storyDate > self.date:
            return True
        return False

# COMPOSITE TRIGGERS

# Problem 7

# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger: Trigger):
        self.compositeTrigger = trigger

    def evaluate(self, story):
        return not self.compositeTrigger.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1: Trigger, trigger2: Trigger):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        isTriggered1 = self.trigger1.evaluate(story)
        isTriggered2 = self.trigger2.evaluate(story)
        return isTriggered1 and isTriggered2

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1: Trigger, trigger2: Trigger):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        isTriggered1 = self.trigger1.evaluate(story)
        isTriggered2 = self.trigger2.evaluate(story)
        return isTriggered1 or isTriggered2

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    doesTrigger = lambda s: any(t.evaluate(s) for t in triggerlist)
    return [story for story in stories if doesTrigger(story)]



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    triggerDict = {}
    resultingTriggers = []

    for line in lines:
        triggerData = line.split(',')
        if triggerData[0] == "ADD":
            triggersToAdd = triggerData[1:]
            resultingTriggers = [triggerDict[t] for t in triggersToAdd]
            # print(f"Adding {resultingTriggers}")
        elif triggerData[1] in ["AND", "OR", "NOT"]:
            print(triggerData)
            triggerName = triggerData[0]
            triggerType = triggerData[1]
            triggerArgs = [triggerDict[t] for t in triggerData[2:]]
            
            # print(f"New Conditional Trigger {triggerName}, {triggerType}, {triggerArgs}")

            if triggerType == "AND": newTrigger = AndTrigger(*triggerArgs)
            elif triggerType == "OR": newTrigger = OrTrigger(*triggerArgs)
            elif triggerType == "NOT": newTrigger = NotTrigger(*triggerArgs)
            else: raise Exception(f"{triggerType} is an Invalid Trigger Type")

            triggerDict[triggerName] = newTrigger
        else:
            triggerName = triggerData[0]
            triggerType = triggerData[1]
            triggerArgs = triggerData[2:]
            # print(f"New Trigger {triggerName}, {triggerType}, {triggerArgs}")

            if triggerType == "TITLE": newTrigger = TitleTrigger(*triggerArgs)
            elif triggerType == "DESCRIPTION": newTrigger = DescriptionTrigger(*triggerArgs)
            elif triggerType == "AFTER": newTrigger = AfterTrigger(*triggerArgs)
            elif triggerType == "BEFORE": newTrigger = BeforeTrigger(*triggerArgs)
            else: raise Exception(f"{triggerType} is an Invalid Trigger Type")

            triggerDict[triggerName] = newTrigger

    # ADD,...t # Add Triggers to List
    # tname,TYPE, ...args
    return resultingTriggers
        



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("Canada")
        # t4 = OrTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed - BROKEN
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

