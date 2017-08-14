
from __future__ import division  # Python 2 users only
import os
import nltk, re, pprint
from nltk.util import bigrams
from nltk import word_tokenize
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def remove_stop_words(text):
	stop = stopwords.words('english')
	return [i for i in text.split() if i not in stop]

def new_list(lists):
	new_list = []
	for l in lists:
		new_list.append(remove_stop_words(l))

	return new_list

def getSimilarity(list1, list2):
	dic1 = {}
	dic2 = {}
	for each in list1:
		if each in dic1:
			dic1[each] = dic1[each] + 1
		else:
			dic1[each] = 1

	for each in list2:
		if each in dic2:
			dic2[each] = dic2[each] + 1
		else:
			dic2[each] = 1

	sim = 0
	for each in dic1:
		if each in dic2:
			sim = sim + min(dic1[each], dic2[each])

	size1 = len(list1)
	size2 = len(list2)
	m = min(size1, size2)
	if(m == 0):
		return 0
	else:
		return float(sim) / m


def remove_stop_words(text):
	stop = stopwords.words('english')
	return [i for i in text.split() if i not in stop]

def get_unigram(text_list):
	# text_list is a list of strings
	new_list = []
	for i in range(len(text_list)):
		new_list.append(remove_stop_words(text_list[i]))

	return new_list

def get_bigram(text_list):
	# text_list is a list of strings
	new_list = []
	for i in range(len(text_list)):
		new_list.append(list(bigrams(text_list[i])))

	return new_list

def main_function(foldername,filename,papername,new_filename,num):

	files = []
	text_list = []
	for file_name in os.listdir(os.getcwd() + "/" + foldername):
		files.append(file_name)

	# we got the files 
	# now we will read all the files and store it in textlist

	for file in files:
		f = open(foldername + "/"+file,'r')
		data = f.read()
		text_list.append(data)
		f.close()

	'''# till her ewe got all the files 
	# now get the abstract 
	a_list = get_dict(filename,papername)
	save_obj(a_list,"a_list")'''
	a_list = load_obj("a_list").values()
	print len(a_list)

	# a_list = a_list.value()
	# print a_list
	# a = dict(a_list)
	# print a.values()

	abstract_list = []
	for l in a_list:
		abstract_list.append(l["abstract"])

	texts = len(text_list)
	abstracts = len(abstract_list)

	# we got both the list now we need to convert into unigram and bigram 
	print "start"
	text_list1 = get_unigram(text_list)
	text_list2 = get_bigram(text_list1)
	abstract_list1 = get_unigram(abstract_list)
	abstract_list2 = get_bigram(abstract_list1)

	# after removing stop words
	# abstract_list = new_list(abstract_list)
	# next 

	# now we will go through all the text in wiki 
	average = []
	avg = open(new_filename,"w")
	for i in range(abstracts):
		print i
		new_list = []
		new_list.append(a_list[i]["name"])
		avg.write(str(i+1)+")\t"+a_list[i]["name"]+"\n\n")
		article = []
		each_wiki = abstract_list[i]
		article = [each_wiki] + text_list
		# we got the list now start
		tfidf = TfidfVectorizer().fit_transform(article)
		cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
		cosine_similarities = list(cosine_similarities[1:])
		'''related_docs_indices = cosine_similarities.argsort()[:- (num +2):-1]
		related_docs_indices = related_docs_indices[1:] # for removing first one 
		c = cosine_similarities[related_docs_indices]
		fl.write(str(i+1)+")\t"+a_list[i]["name"]+"\n\n")
		new_new_list = []
		for j in range(len(related_docs_indices)):
			fl.write(str(c[j]) +"\t"+ str(files[related_docs_indices[j]-1]) +"\n")
			new_new_list.append([c[j],str(files[related_docs_indices[j]-1])])
			# -1 is necessary here because the there is one more at the top in the list of wiki pages

		fl.write("\n\n")
		new_list.append(new_new_list)
		tfidf2.append(new_list)'''

		cosine_list1 = []
		cosine_list2 = []
		for j in range(texts):
			cosine_list1.append(getSimilarity(abstract_list1[i],text_list1[j]))
			cosine_list2.append(getSimilarity(abstract_list2[i],text_list2[j]))

		# till here we got 
		c = []
		new_b = []
		if(len(cosine_similarities) == len(cosine_list2)):
			for k in range(len(cosine_similarities)):
				c.append((cosine_list1[k] + cosine_list2[k] + cosine_similarities[k])/3)

			del cosine_similarities
			del cosine_list2
			del cosine_list1
			carr = np.array(c)
			top = list(carr.argsort()[-num:][::-1])
			for each in top:
				avg.write(str(c[each]) +"\t"+ str(files[each]) +"\n")
				new_b.append([c[each],str(files[each])])

		else:
			print "error"

		avg.write("\n\n")
		new_list.append(new_b)
		average.append(new_list)

	avg.close()
	save_obj(average,"average")

if __name__ == '__main__':
	main_function("Wiki","disk_merge","papers","output_average.txt",50)

