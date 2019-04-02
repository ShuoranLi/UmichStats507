#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 02:40:49 2019

@author: shuoranli
"""

from mrjob.job import MRJob
import re

word_reg = re.compile(r"[a-zA-Z][a-zA-Z']*\-[a-zA-Z']+|[a-zA-z]+\'?[a-zA-Z]*")

class MRWordCount(MRJob):
    
    def mapper(self,_,line):
        # yield each word in the line
        for word in word_reg.findall(line):
            yield (word.lower(), 1)
    def combiner(self,word, counts):
        yield (word, sum(counts))
        
    def reducer(self, word, counts):
        yield (word, sum(counts))

if __name__ == '__main__': 
    MRWordCount.run()