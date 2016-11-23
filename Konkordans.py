#! /usr/bin/env python3

# Konkordans 20 november 2016
# Anna Eklund  Elin Karagöz

import codecs
import os, sys
import linecache

index = "/var/tmp/bananaindex"
ut = "/var/tmp/bananaut"
hashfile = "/var/tmp/hashbanana"
korpus = "/info/adk16/labb1/korpus"

def main():
    for arg in sys.argv[1:]:
        if arg == "--create":
            createIndex()
            exit()
        else:
            findWord(arg.lower())
            exit()

def createIndex():
    pos = 0
    hashList = [-1 for x in range(27000)] # alla har värdet -1 och finns 27000 rader, en för varje bokstavskombination aaa->ööö
    index_file = codecs.open(index, "w+", "ISO-8859-1")
    ut_file = codecs.open(ut, "r", "ISO-8859-1")
    line = ""
    prevWords = "" 
    try: 
        for line in ut_file:      
            words = line.split()
            if words[0] != prevWords: # ifall det är ett nytt ord
                wordToHash = str(words[0])
                hashValue = hashify(wordToHash)
                if prevWords != "":
                    index_file.write("\n")
                index_file.write((str(line)).strip("\n"))  # lägg till hela raden, dvs tex "hejsan 560"
                if hashList[hashValue] == -1:
                    hashList[hashValue] = pos
                    pos += len(line)
            else:
                index_file.write(" " + str(words[1]))  # annars vill vi bara lägga till själva siffran, dvs teckenpos
                pos += len(words[1])+1
            prevWords = words[0] 

    finally: 
        index_file.close() 
        ut_file.close()
        hash_file = codecs.open(hashfile,"w+", "ISO-8859-1")
        for entry in hashList:
            hash_file.write(str(entry) + "\n")
        hash_file.close()

def hashify(wordToHash):
    hashWord = [" "," "," "]

    if len(wordToHash) == 1:
        hashWord[0] = wordToHash
        hashWord[1] = " "
        hashWord[2] = " "
    elif len(wordToHash) == 2:
        s =list(wordToHash)
        hashWord[0] = s[0]
        hashWord[1] = s[1]
        hashWord[2] = " "
    else:
        s =list(wordToHash)
        hashWord[0] = s[0]
        hashWord[1] = s[1]
        hashWord[2] = s[2]

    a = hashWord[0]
    b = hashWord[1]
    c = hashWord[2]

    number = hashNumber(a)*900 + hashNumber(b)*30 + hashNumber(c)
    return number

def hashNumber(character): 
    if character == " ":
        num = 0
    elif character == 'å':
        num = 27
    elif character == 'ä':
        num = 28
    elif character == 'ö':
        num = 29
    else:
        num = (ord(character) - 96)
    return num


def findWord(wordToFind): # hitta rätt rad i index-filen där ordet finns & skicka den raden till printKonkordans()
    value = hashify(wordToFind)
    index_file = codecs.open(index, "r", "ISO-8859-1")
    startPos = int(linecache.getline(hashfile, value+1)) # hashfilen är 0-indexerad, 
    index_file.seek(startPos, 0)
    s = index_file.readline()
    sp = s.split()

    while wordToFind != sp[0]: 
        s = index_file.readline()
        sp = s.split()
        if sp[0] > wordToFind:
            print("'" + wordToFind + "'" + " finns inte i Korpus")
            exit()
    index_file.close()
    print("Det finns " + str(len(sp)-1) + " förekomster av ordet" + "\n")
    if len(sp) > 25:
        a = input("Vill du verkligen se alla ord? (y/N) ")
        if a != "y" and a!= "Y":
            print("oké")
            exit()
    printKonkordans(s)

def printKonkordans(lineToPrint): # sök i korpus 
    korp = codecs.open(korpus,"r", "ISO-8859-1")
    find = lineToPrint.split()
    wordToPrint = find[0]
    for x in find[1:]:
        if int(x) < 10:
            korp.seek(int(x), 0)
        else:
            korp.seek(int(x)-10, 0) # flyttar 10 bytes bakåt
        print(korp.read(20+ len(wordToPrint)).replace("\n", " "))
    korp.close()

if __name__ == "__main__":
    main()