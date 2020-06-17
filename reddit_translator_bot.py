# -*- coding: utf-8 -*-
"""
This is code for a bot that can tranlate submission or comment text in Reddit using the
Googletrans library. It is an unofficial library using the web API of translate.google.com.
Future code may switch over to the official Google Translate API. The max character limit 
currently is 15k based on the documenation for Googletrans.

Currently delete and reply functionality is disabled. New bots have hard ratelimit caps.
This code is more for seeing results in console for right now.

Link to Googletrans 3.0.0 info: https://pypi.org/project/googletrans/
Link to official Google Translate API: https://cloud.google.com/translate/docs
Link to the language encoding info: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

Some supported languages:
af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he,
hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl,
pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw

"""

import praw
import re
from googletrans import Translator
import sys
import time
from datetime import datetime

def comment_vs_submission(input):
    if re.search("comment", type(input).__name__, re.IGNORECASE):
        print("comment")
        return "comment"
    else:
        print("submission")
        return "submission"

bot = praw.Reddit(user_agent='translator_bot v0.1',
                  client_id='',
                  client_secret='',
                   username='',
                   password=''
                  )

# Input parameters
duration = 1.8
subreddit = bot.subreddit('scriptBotTesting')


translator = Translator()
log_file_list = []
start_time = time.time()

# for comment in subreddit.stream.comments(skip_existing=True):
for comment in subreddit.stream.comments():
    if re.search("DeleteTranslation!", comment.body, re.IGNORECASE):
        # comment = reddit.comment(id='dj0bw7q') # assume this comment shows up in your inbox
        parent = comment.parent()  # the comment made by your bot
        grandparent = parent.parent()  # the comment that first triggered the bot
        if comment.author == grandparent.author:  # checks if the person is the one you care about
            if parent.author == "_data_mining_bot_":
                continue
            
                # parent.delete()
          
                print("Delete Successful!")
        
    #     sys.exit()
              
    # format is ("TranslateThis! language"), ex: "TranslateThis! ko" to translate to Korean
    if re.search("TranslateThis!", comment.body, re.IGNORECASE):
        
        needing_translation = comment.parent()
        comment_as_list = comment.body.split()
        
        type_of_parent = comment_vs_submission(needing_translation)
        
        if type_of_parent == "comment":
           parent = bot.comment(needing_translation)
           language_of_text = translator.detect(parent.body).lang
           translation = translator.translate(parent.body, dest=comment_as_list[1])
        else:
            parent = bot.submission(needing_translation)
            language_of_text = translator.detect(parent.title).lang
            translation = translator.translate(parent.title, dest=comment_as_list[1])

        
        print("Language of the text: ", language_of_text)
        print("Language to be translated into: ", comment_as_list[1])
        print("Input: ", translation.origin)
        print("Output: ", translation.text)
        now = str(datetime.now())
        entry_list = []
        entry_list.append(now)
        entry_list.append("scriptBotTesting")
        entry_list.append(language_of_text)
        entry_list.append(comment_as_list[1])
        entry_list.append(translation.origin)
        entry_list.append(translation.text)
        
        log_file_list.append(entry_list)
        
        # creates a log for what is translated
        with open("log.txt", "a+", encoding='utf-8') as f:
            # f.write(str(log_file_list) + "\n")
            for listitem in log_file_list:
                f.write('%s\n' % listitem)
        
        # comment.reply("Translation: " + translation.text + 
        #               "\n\nThis is a language translation bot powered by [Google Translate](translate.google.com)"+
        #               "Find the code [here]()")
        
        # sys.exit()
        
    end_time = time.time() - start_time
    print("End of loop at: ", str(end_time))
    print()
    if end_time > duration:
        break
    
    
    
# # can create the log at the end if testing for a certain amount of time, helps with performance
# with open("log.txt", "a+", encoding='utf-8') as f:
#     # f.write(str(log_file_list) + "\n")
#     for listitem in log_file_list:
#         f.write('%s\n' % listitem)
        