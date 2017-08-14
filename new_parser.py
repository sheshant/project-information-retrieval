
from __future__ import division  # Python 2 users only
import numpy as np
import os
import nltk, re, pprint
from nltk import word_tokenize
from nltk.corpus import stopwords
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


def get_list(filename):

	file = open(filename,'r')
	data = file.read()
	papers = data.split("\n\n")
	list = []
	for paper in papers:
		paper = paper.split("\n")
		temp = []
		temp.append(paper[1][1:])
		temp.append(paper[2][2:])
		temp.append(paper[4][2:])
		list.append(temp)

	# list has 
	# 1 ) id
	# 2 ) name
	# 3 ) abstract
	# cool now we need to make list of all text
	return list

def get_dict(filename1, filename2):


	file1 = open(filename1, 'r')
	file2 = open(filename2, 'r')
	print "here 1"
	data = file1.read()
	print "here 2"
	indexes = file2.read().split("\n")
	#print indexes
	print len(indexes)
	papers = data.split("\n\n")
	print len(papers)
	print papers[0].split("\n")[1]
	print len(papers[0].split("\n")[1]) - len(indexes[0])
	dic = {}
	i = 0
	for paper in papers:
		paper = paper.split("\n")
		if paper[0] in indexes:
			print i
			i = i + 1
			dic[paper[0]] = {}
			dic[paper[0]]["name"] = paper[2][2:]
			dic[paper[0]]["abstract"] = paper[4][2:]
	return dic


def main_function(foldername,filename,papername,new_filename,num):

	fl = open(new_filename,"w")
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

	# after removing stop words
	# abstract_list = new_list(abstract_list)
	# next 

	# now we will go through all the text in wiki 
	tfidf2 = []
	for i in range(len(abstract_list)):
		print i
		new_list = []
		new_list.append(a_list[i]["name"])
		article = []
		each_wiki = abstract_list[i]
		article = [each_wiki] + text_list
		# we got the list now start
		tfidf = TfidfVectorizer().fit_transform(article)
		cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
		related_docs_indices = cosine_similarities.argsort()[:- (num +2):-1]
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
		tfidf2.append(new_list)

	fl.close()
	save_obj(tfidf2,"tfidf")




	'''tfidf = TfidfVectorizer().fit_transform(text_list)

	# get the size 
	s = tfidf.shape
	row = s[0]
	col = s[1]

	fl = open(new_filename,"w")
	for i in range(row):
		cosine_similarities = linear_kernel(tfidf[i:i+1], tfidf).flatten()
		related_docs_indices = cosine_similarities.argsort()[:- (num +2):-1]
		c = cosine_similarities[related_docs_indices]
		doc_name = []
		similarity = []
		fl.write(str(i+1)+")\t"+files[i]+"\n\n")
		for j in range(len(related_docs_indices)):
			if related_docs_indices[j] != i:
				doc_name.append(files[related_docs_indices[j]])
				similarity.append(c[j])
				fl.write(str(c[j]) +"\t"+ str(files[related_docs_indices[j]]) +"\n")

		fl.write("\n\n")
																	.close()'''																																																																																																																																																																																																																												




if __name__ == '__main__':
	main_function("Wiki","disk_merge","papers","new_output.txt",50)