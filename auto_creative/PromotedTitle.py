#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zhoujiebin
@contact: garcia.wul@alibaba-inc.com
@date: 2012-09-04 13:03
@version: 0.0.0
@license: Copyright alibaba-inc.com
@copyright: Copyright alibaba-inc.com

"""
import os,sys
curr_path = os.path.dirname(__file__)
sys.path.append(os.path.join(curr_path, '../'))
from settings import  ban_path

class ChunkWord(object):
    def __init__(self, begin, end, chunkLength, coreWeight, weight, content):
        self.begin = begin
        self.end = end
        self.chunkLength = chunkLength
        self.coreWeight = coreWeight
        self.weight = weight
        self.content = content
        self.label = False

    def getBegin(self):
        return self.begin

    def getEnd(self):
        return self.end

    def getWeight(self):
        return self.weight

    def getLabel(self):
        return self.label

    def setLabel(self, label):
        self.label = label
    
    def getChunkLength(self):
        return self.chunkLength

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content

class Position(object):
    def __init__(self, pos, weight):
        self.pos = pos
        self.weight = weight
    
    def getPos(self):
        return self.pos
    
    def getWeight(self):
        return self.weight

class Term(object):
    def __init__(self, term_list):
       self.key = str(term_list[0])
       self.nType = str(term_list[1])
       self.nWeight = int(term_list[2])

class PromotedTitle(object):

    def __init__(self, segmenter):
        self.termObjs_list = []
        self.termLength_list = []
        self.segmenter = segmenter
        self.filter_terms = self.loadFilterTerms()

    def __del__(self):
        pass

    def filterTerms(self, title):
        for term in self.filter_terms:
            while title.find(term) >= 0:
                title = title.replace(term, '')
        
        symbol_list = ['/','【', '】' ,'.', '。',  '[', ']', '￥', '$', '#', '@', '&', '=', '+', '|', ';' ]
        for symbol in symbol_list:
            while title.find(symbol) >= 0:
                title = title.replace(symbol, '')

        return title

    def loadFilterTerms(self):
        sick_terms = file(ban_path['sick_terms']).read().split('\n')
        channel_terms = file(ban_path['channel_terms']).read().split('\n')
        brand_terms = file(ban_path['brand_terms']).read().split('\n')
        return sick_terms[:-1] + channel_terms[:-1] + brand_terms[:-1]

    def getNewTitle(self, title):
        try:
            title = self.filterTerms(title)
            term_list = self.segmenter.do_segment(title)
            self.termObjs_list = []
            self.termLength_list = []
            for term in term_list:
                term_obj = term.split("\1")
                self.termObjs_list.append(Term(term_obj))
                self.termLength_list.append(self.getStrLength(term_obj[0]))
                #print term_obj[0] + '\t' + term_obj[1] + '\t' + term_obj[2] + '\t' + str(self.getStrLength(term_obj[0]))
            chunkWord_list = []
            posOrder = []
            titleLength = 0
            self.makeChunkWord(chunkWord_list, posOrder)
            for pos in posOrder:
                i = pos.getPos()
                chunkLength = chunkWord_list[i].getChunkLength()
                if 40 - titleLength >= chunkLength:
                    chunkWord_list[i].setLabel(True)
                    titleLength += chunkLength
                elif 40 - titleLength >= 4:
                    self.segmentChunkWord(chunkWord_list[i], 40 - titleLength)
                    break
            newTitle = ''
            for chunkWord in chunkWord_list:
                if chunkWord.getLabel():
                    newTitle += chunkWord.getContent()
            return newTitle
        except Exception,t:
            print t
            return ''

    def getStrLength(self, _str):
        _str = _str.decode('utf-8')
        length = 0
        for xstr in _str:
            if len(xstr.encode('utf-8')) == 3:
                length += 2
            elif len(xstr.encode('utf-8')) == 1:
                length += 1
        return length
   
    def isKeyWord(self, term):
        type_set = set(['PP','PP_CORE','CP','CP_XIUSHI','CP_CORE'])
        if term.nType in type_set and term.nWeight >= 9:
            return True
        if term.nWeight >= 12:
            return True
        return False

    def makeChunkWord(self, chunkWord_list, posOrder):
        sumWeight = 0
        sumTermLength = 0
        begin = 0
        count = 0
        content = ""
        for i in range(len(self.termObjs_list)):
            term = self.termObjs_list[i]
            if term.nWeight > 0:
                count += 1
            sumWeight += term.nWeight
            sumTermLength += self.termLength_list[i]
            content += term.key
            if self.isKeyWord(term) or (sumTermLength >= 10 and i == len(self.termObjs_list) - 1):
                weight = float(sumWeight) / (count + 0.000001)
                chunkWord = ChunkWord(begin, i, sumTermLength, term.nWeight, weight, content)
                chunkWord_list.append(chunkWord)

                position = Position(len(chunkWord_list) - 1, chunkWord.getWeight())
                posOrder.append(position)

                sumWeight = 0
                sumTermLength = 0
                count = 0
                content = ""
                begin = i + 1

        posOrder.sort(self.posCmp, reverse=True)
        return True
    
    def segmentChunkWord(self, chunkWord, save):
        if self.termLength_list[chunkWord.getEnd()] > save:
            return False
        sum = chunkWord.getChunkLength()
        i = chunkWord.getBegin()
        while sum > save:
            sum -= self.termLength_list[i]
            i += 1
        
        temp = ""
        first = self.termObjs_list[i].key
        if chunkWord.getBegin() == 0 and len(first) == 3 and len(first.decode('utf-8')) == 1:
            i += 1
        while i <= chunkWord.getEnd():
            temp += self.termObjs_list[i].key
            i += 1
        chunkWord.setContent(temp)
        chunkWord.setLabel(True)
        return True

    def posCmp(self, pos1, pos2):
        return cmp(pos1.getWeight(), pos2.getWeight())

if __name__ == '__main__':
    sys.path.append('../')
    from settings import segmenter

    obj = PromotedTitle(segmenter)
    titleData = file(sys.argv[1]).read().split('\n')

    for title in titleData:
        if title != '':
            #print type(title)
            newTitle = obj.getNewTitle(title.decode('utf8').encode('utf8'))
            print title + '=>' + newTitle + ',length:' + str(obj.getStrLength(newTitle))
