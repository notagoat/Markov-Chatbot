#!/usr/bin/env python
#Sika v1.1
#Todo:
# - Add checks for questions (regex)
# - Find training data
#   - Podcast transcripts (HI?)
# - Allow more varied responses using synonyms?
# - Add twitter support
# - find method of training using the loop

import pickle
import random
import sys

text = open("text.txt","r")
chain = {}
def pickler():
    def generate_trigram(words):
        if len(words) < 3:
            return
        for i in range(len(words) - 2):
            yield (words[i], words[i+1], words[i + 2])

    for line in text.readlines():
        words = line.split()
        for word1, word2, word3 in generate_trigram(words):
            key = (word1, word2)
            if key in chain:
                chain[key].append(word3)
            else:
                chain[key] = [word3]

    pickle.dump(chain, open("conversation.p", "wb"))

def reply(firstword):
    chain = pickle.load(open("conversation.p", "rb"))

    text = []
    sword1 = "NOW"
    sword2 = firstword

    while True:
        sword1, sword2 = sword2, random.choice(chain[(sword1, sword2)])
        if sword2 == "END":
            break
        text.append(sword2)

    fintext = ' '.join(text)
    return fintext

def inputrun():
    inputwords = ""
    printed = False

    for i in range(len(botinput)):
        try:
            inputwords = inputwords + botinput[i] + " "
            output = reply(botinput[i])
            if printed == False:
                print(botinput[i] + " " + output)
            printed = True
        except (KeyError):
            pass
    if printed == False:
        print("What?")
    newstring = "NOW " + inputwords + "END"
    #print(newstring)
    with open("text.txt", "a") as out:
        out.write(newstring + "\n")

def conversationhandler():
    global botinput
    EndBool = False
    while (EndBool == False):
        inputstring = input("> ")
        if (inputstring == "Goodbye"):
            print("Goodbye for now!")
            break
        botinput = inputstring.split()
        pickler()
        inputrun()

def main():
    conversationhandler()

if __name__ == "__main__":
    main()
