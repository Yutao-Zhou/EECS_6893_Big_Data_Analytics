#!/usr/bin/env python

import pyspark
import sys
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import os

if len(sys.argv) != 3:
  raise Exception("Exactly 2 arguments are required: <inputUri> <outputUri>")

inputUri=sys.argv[1]
outputUri=sys.argv[2]

sc = pyspark.SparkContext()
lines = sc.textFile(sys.argv[1])
words = lines.flatMap(lambda line: line.split(" ")).filter(lambda x: x != "")
user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
stop = [w.title() for w in stopwords.words('english')]
stop += stopwords.words('english')
stopWords = sc.parallelize(stop)
filteredWords = words.subtract(stopWords)
wordCounts = filteredWords.map(lambda word: (word, 1)).reduceByKey(lambda count1, count2: count1 + count2)
frequencyMap = wordCounts.sortBy(lambda pair: -pair[1]).take(10)
print(frequencyMap)
saveRdd = sc.parallelize(frequencyMap)
saveRdd.saveAsTextFile(outputUri)