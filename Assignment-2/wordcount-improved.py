from pyspark import SparkConf, SparkContext
import sys
import operator
import re, string

inputs = sys.argv[1]
output = sys.argv[2]

conf = SparkConf().setAppName('word count')
sc = SparkContext(conf=conf)
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+
assert sc.version >= '2.3'  # make sure we have Spark 2.3+

def words_once(line):
	word_sep = re.compile(r'[%s\s]+' % re.escape(string.punctuation))
	split_words = word_sep.split(line)
	for w in split_words:
		w = w.lower()
		yield (w, 1)

def get_key(kv):
	return kv[0]

def output_format(kv):
	k, v = kv
	return '%s %i' % (k, v)

def check_length(x):
	return len(x) > 0	

text = sc.textFile(inputs)
words = text.flatMap(words_once).filter(check_length)
wordcount = words.reduceByKey(operator.add)

outdata = wordcount.sortBy(get_key).map(output_format)
outdata.saveAsTextFile(output)