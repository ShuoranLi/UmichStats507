#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 20:55:38 2019

@author: shuoranli
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import functools as ft

class MRSumStats(MRJob):
    
    def mapper(self,_,line):
        yield (line.split()[0],(1,float(line.split()[1]),
                          (float(line.split()[1]))**2))
    def combiner(self,key,values):
        yield (key,ft.reduce(lambda x,y:(x[0]+y[0],x[1]+y[1],x[2]+y[2]),values)) 
    def reducer_processing(self,key,values):
        yield (key,ft.reduce(lambda x,y:(x[0]+y[0],x[1]+y[1],x[2]+y[2]),values)) 
    def reducer_final(self,key,values):
        # Use (n-1) as the denominator of sample variance formula
        yield (key,ft.reduce(lambda x,y:(x[0]+y[0],
                                         x[1]+y[1]/y[0],
                                         x[2]+(y[2]-y[1]**2/y[0])/(y[0]-1)),
                                         values,
                                         (0,0,0))) 
    def steps(self):
        return [
                MRStep(mapper = self.mapper,
                       combiner = self.combiner,
                       reducer = self.reducer_processing),
                MRStep(reducer = self.reducer_final)]
        
if __name__ == '__main__':
    MRSumStats.run()
        