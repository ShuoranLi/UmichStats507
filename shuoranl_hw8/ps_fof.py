#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 00:24:11 2019

@author: shuoranli
"""

import sys
from pyspark import SparkConf, SparkContext
import itertools
# This script takes two arguments, an input and output
if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' <in> <out>')
    sys.exit(1)
inputlocation = sys.argv[1]
outputlocation = sys.argv[2]

# Set up the configuration and job context
conf = SparkConf().setAppName("TriangleCounting")
sc = SparkContext(conf=conf)

data = sc.textFile(inputlocation)
data = data.map(lambda line: line.split())

def possible_tri(lst):
    # find all combinations of friends of certain person
    combos = list(itertools.combinations(lst[1:],2))
    self_combos = list(map(lambda t:[lst[0]]+list(t) ,combos))
    self_combos_sort = list(map(lambda t:sorted(t),self_combos))
    tuple_pairs = list(map(lambda l:(tuple(l),1), self_combos_sort))
    return tuple_pairs

data_potential_tri = data.flatMap(possible_tri)
num_tri_pairs = data_potential_tri.reduceByKey(lambda x,y:x+y)
# choose triangles whose values >= 2, this means that these three 
# people are mutually acquainted
data_tri = num_tri_pairs.filter(lambda x: x[1]>=2)
data_tri = data_tri.map(lambda x: x[0])
data_tri.saveAsTextFile(outputlocation)

sc.stop()# Let Spark know that the job is done.