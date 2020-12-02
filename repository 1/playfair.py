# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:59:57 2020

Refer to the instructions on Canvas for more information.

"I have neither given nor received help on this assignment."
author: Inhan Park
"""

from string import ascii_lowercase

def createTable(phrase):
    '''
    Given an input string, create a lowercase playfair table.  The
    table should include no spaces, no punctuation, no numbers, and 
    no Qs -- just the letters [a-p]+[r-z] in some order.  Note that 
    the input phrase may contain uppercase characters which should 
    be converted to lowercase.
    
    Input:   string:         a passphrase
    Output:  list of lists:  a ciphertable
    '''
    stringCT = phrase.lower()
    
    remove_elem = '''q!()-[]{};:'"\, <>./?@#$%^&*_~'''
    alphabet = 'abcdefghijklmnoprstuvwxyz'
    
    for elem in stringCT:
        if elem in remove_elem:
            stringCT = stringCT.replace(elem, '')
          
    tempCT = ''
    for elem in stringCT:
        if elem not in tempCT:
            tempCT = tempCT + elem
    
    stringCT = tempCT
    
    for elem in alphabet:
        if elem not in stringCT:
            stringCT = stringCT + elem
            
    tableCT = [0,0,0,0,0]
    index = 0
    
    for i in range (0, 5):
        tempCT_table = [0,0,0,0,0]
        for j in range (0, 5):
            tempCT_table[j] = stringCT[index]
            index = index + 1
        tableCT[i] = tempCT_table
        

    return tableCT


def splitString(plaintext):
    '''
    Splits a string into a list of two-character pairs.  If the string
    has an odd length, append an 'x' as the last character.  As with
    the previous function, the bigrams should contain no spaces, no
    punctuation, no numbers, and no Qs.  Return the list of bigrams,
    each of which should be lowercase.
    
    Input:   string:  plaintext to be encrypted
    Output:  list:    collection of plaintext bigrams
    '''
    stringSS = plaintext.lower()
    remove_elem = '''q!()-[]{};:'"\, <>./?@#$%^&*_~'''
    for elem in stringSS:
        if elem in remove_elem:
            stringSS = stringSS.replace(elem, '')
            
    if len(stringSS)%2 == 1:
        stringSS = stringSS + 'x'
        
    list = []
        
    for i in range(0, int(len(stringSS)/2)):
        list.append(stringSS[(0+i*2):(2+i*2)])

    return list


def playfairRuleOne(pair):
    '''
    If both letters in the pair are the same, replace the second
    letter with 'x' and return; unless the first letter is also
    'x', in which case replace the second letter with 'z'.
    
    You can assume that any input received by this function will 
    be two characters long and already converted to lowercase.
    
    After this function finishes running, no pair should contain two
    of the same character   
    
    Input:   string:  plaintext bigram
    Output:  string:  potentially modified bigram
    '''
    
    
    if pair[0] == pair[1]:
        if pair[0] != 'x':
            pair = pair[0] + 'x'
        else:
            pair = pair[0] + 'z'
        
    return pair
    
    
    
    

def playfairRuleTwo(pair, table):
    '''
    If the letters in the pair appear in the same row of the table, 
    replace them with the letters to their immediate right respectively
    (wrapping around to the left of a row if a letter in the original
    pair was on the right side of the row).  Return the new pair.
    
    You can assume that the pair input received by this function will 
    be two characters long and already converted to lowercase, and
    that the Playfair Table is valid.
    
    Input:   string:         potentially modified bigram
    Input:   list of lists:  ciphertable
    Output:  string:         potentially modified bigram
    '''
    
    for j in table:
        if pair[0] in j and pair[1] in j:
            if j.index(pair[1]) == 4:
                pair = j[j.index(pair[0]) + 1] + j[0]
            else :
                pair = j[j.index(pair[0]) + 1] + j[j.index(pair[1]) + 1]
        
    return pair
    


def playfairRuleThree(pair, table):
    '''
    If the letters in the pair appear in the same column of the table, 
    replace them with the letters immediately below respectively
    (wrapping around to the top of a column if a letter in the original
    pair was at the bottom of the column).  Return the new pair.
    
    You can assume that the pair input received by this function will 
    be two characters long and already converted to lowercase, and
    that the Playfair Table is valid.
    
    Input:   string:         potentially modified bigram
    Input:   list of lists:  ciphertable
    Output:  string:         potentially modified bigram
    '''    
    transpose_table = []
    
    for index in range(len(table[0])):
        row = []
        for item in table:
            row.append(item[index])
        transpose_table.append(row)
        
    for j in  transpose_table:
        if pair[0] in j and pair[1] in j:
            if j.index(pair[1]) == 4:
                pair = j[j.index(pair[0]) + 1] + j[0]
            else :
                pair = j[j.index(pair[0]) + 1] + j[j.index(pair[1]) + 1]
        
    return pair
    


def playfairRuleFour(pair, table):
    '''
    If the letters are not on the same row and not in the same column, 
    replace them with the letters on the same row respectively but in 
    the other pair of corners of the rectangle defined by the original 
    pair.  The order is important -- the first letter of the ciphertext
    pair is the one that lies on the same row as the first letter of 
    the plaintext pair.
    
    You can assume that the pair input received by this function will 
    be two characters long and already converted to lowercase, and
    that the Playfair Table is valid.  
    
    Input:   string:         potentially modified bigram
    Input:   list of lists:  ciphertable
    Output:  string:         potentially modified bigram
    '''
        
    index1_1 = 0
    index1_2 = 0
    index2_1 = 0
    index2_2 = 0
    
    for line in table:
        if pair[0] in line:
            first_line = line
            index1_1 = table.index(first_line)
            index1_2 = first_line.index(pair[0])
        if pair[1] in line:
            second_line = line
            index2_1 = table.index(second_line)
            index2_2 = second_line.index(pair[1])
                
    if (index1_1 != index2_1) and (index1_2 != index2_2):
        pair = table[index1_1][index2_2] + table[index2_1][index1_2]
            
    return pair
    
    
    

def encrypt(pair, table):
    '''
    Given a character pair, run it through all four rules to yield
    the encrypted version!
    
    Input:   string:         plaintext bigram
    Input:   list of lists:  ciphertable
    Output:  string:         ciphertext bigram
    '''
    pair = playfairRuleOne(pair)
    pair = playfairRuleTwo(pair, table)
    pair = playfairRuleThree(pair, table)
    pair = playfairRuleFour(pair, table)
    return pair

def joinPairs(pairsList):
    '''
    Given a list of many encrypted pairs, join them all into the 
    final ciphertext string (and return that string)
    
    Input:   list:    collection of ciphertext bigrams
    Output:  string:  ciphertext
    '''
    length = len(pairsList)
    result =''
    
    for i in range(0, length):
        result = result + pairsList[i]

    return result

def main():
    '''
    Example main() function; can be commented out when running your
    tests
    '''
    testCreateTable()
    testSplitString()
    testPlayFairRuleOne()
    testPlayFairRuleTwo()
    testPlayFairRuleThree()
    testPlayFairRuleFour()
    testEncrypt()
    testJoinPairs()
 #   table = createTable("i am entering a pass phrase")
 #   splitMessage = splitString("this is a test message")
 #   pairsList = []

 #   print(table) # printed for debugging purposes
    
  #  for pair in splitMessage:
        # Note: encrypt() should call the four rules
 #       pairsList.append(encrypt(pair, table))
 #   cipherText = joinPairs(pairsList)    
    
 #   print(cipherText) #printed as the encrypted output
    #output will be hjntntirnpginprnpm


###############################################################

# Here is where you will write your test case functions
    
# Below are the tests for createTable()
def testCreateTable():
    assert createTable("i am entering a pass phrase") == [ ['i', 'a', 'm', 'e', 'n'], ['t', 'r', 'g', 'p', 's'], ['h', 'b', 'c', 'd', 'f'], ['j', 'k', 'l', 'o', 'u'], ['v', 'w', 'x', 'y', 'z'] ]
    assert createTable('abcdefghijklmnopqrstuvwxyzzzz') == [['a','b','c','d','e'],['f','g','h','i','j'],['k','l','m','n','o'],['p','r','s','t','u'],['v','w','x','y','z']]
    assert createTable('qwerty uio.pasdf/ghj,klzx\cvb?nm') == [['w', 'e', 'r', 't', 'y'], ['u', 'i', 'o', 'p', 'a'], ['s', 'd', 'f', 'g', 'h'], ['j', 'k', 'l', 'z', 'x'], ['c', 'v', 'b', 'n', 'm']]
    assert createTable('qwerty') == [['w', 'e', 'r', 't', 'y'], ['a', 'b', 'c', 'd', 'f'], ['g', 'h', 'i', 'j', 'k'], ['l', 'm', 'n', 'o', 'p'], ['s', 'u', 'v', 'x', 'z']]


def testSplitString():
    assert splitString("this is my plaintext") == ["th", "is", "is", "my", "pl", "ai", "nt", "ex", "tx"]
    assert splitString('remove ALl qQQQq') == ['re', 'mo', 've', 'al', 'lx']
    assert splitString('aqnsqw??/er') == ['an', 'sw', 'er']
    assert splitString('THIS IS MY PLAINTEXT!!!?!!') == ["th", "is", "is", "my", "pl", "ai", "nt", "ex", "tx"]


def testPlayFairRuleOne():
    # This comment explains what test2() is testing for, and is followed by code
    assert playfairRuleOne('aa') == 'ax', 'rule one'
    assert playfairRuleOne("th") == "th", 'rule one'
    assert playfairRuleOne('xx') == 'xz', 'rule one'
    assert playfairRuleOne('cx') == 'cx', 'rule one'


def testPlayFairRuleTwo():
    table = createTable("i am entering a pass phrase")
    assert playfairRuleTwo('am', table) == 'me', 'rule two'
    assert playfairRuleTwo('in',table) == 'ai', 'rule two'
    assert playfairRuleTwo('tp',table) == 'rs', 'rule two'
    assert playfairRuleTwo('ed',table) == 'ed', 'rule two'

def testPlayFairRuleThree():
    table = createTable("i am entering a pass phrase")
    assert playfairRuleThree('th', table) == 'hj', 'rule three'
    assert playfairRuleThree('gl', table) == 'cx', 'rule three'
    assert playfairRuleThree('tv', table) == 'hi', 'rule three'
    assert playfairRuleThree('ax', table) == 'ax', 'rule three'

def testPlayFairRuleFour():
    table = createTable("i am entering a pass phrase")
    assert playfairRuleFour('fm', table) == 'cn', 'rule four'
    assert playfairRuleFour('as', table) == 'nr', 'rule four'
    assert playfairRuleFour('jw', table) == 'kv', 'rule four'
    assert playfairRuleFour('do', table) == 'do', 'rule four'

def testEncrypt():
    table = createTable("i am entering a pass phrase")
    assert encrypt('gg', table) == 'cm', 'encrypt part'
    assert encrypt('aa', table) == 'mw', 'encrypt part'
    assert encrypt('xx', table) == 'yv', 'encrypt part'
    assert encrypt('cx', table) == 'lm', 'encrypt part'

def testJoinPairs():
    assert joinPairs(['cn','nr','kv','do']) == 'cnnrkvdo', 'joinpairs part'
    assert joinPairs(['cm','mw','yv','lm']) == 'cmmwyvlm', 'joinpairs part'
    assert joinPairs(['wx','zc','ad','fb']) == 'wxzcadfb', 'joinpairs part'
    assert joinPairs(['as','df','gh','jk']) == 'asdfghjk', 'joinpairs part'


    
###############################################################    
    
if __name__ == "__main__":
    main()        