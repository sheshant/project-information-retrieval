from __future__ import division  # Python 2 users only
import os
import nltk, re, pprint
from nltk.util import bigrams
from nltk import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import pickle

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

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
	data = file1.read()
	indexes = file2.read().split("\n")
	#print indexes
	print len(indexes)
	papers = data.split("\n\n")
	dic = {}
	for paper in papers:
		paper = paper.split("\n")
		if paper[1] in indexes:
			dic[paper[1]] = {}
			dic[paper[1]]["name"] = paper[2][2:]
			dic[paper[1]]["abstract"] = paper[4][2:]
	return dic

def final_function(foldername,filename,papername,output1,output2,num):

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

	a_list = load_obj("a_list").values()
	print len(a_list)

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
	print "unigram bigram models created"

	# now the comparison begins
	# we need to compare both for unigram and bigram

	unigram = open(output1,"w")
	bigram = open(output2,"w")

	'''for i in range(texts):
		print i
		unigram.write(str(i+1)+")\t"+files[i]+"\n\n")
		bigram.write(str(i+1)+")\t"+files[i]+"\n\n")
		cosine_list1 = []
		cosine_list2 = []
		for j in range(abstracts):
			cosine_list1.append(getSimilarity(text_list1[i],abstract_list1[j]))
			cosine_list2.append(getSimilarity(text_list2[i],abstract_list2[j]))

		arr1 = np.array(cosine_list1)
		arr2 = np.array(cosine_list2)

		top1 = list(arr1.argsort()[-num:][::-1])
		top2 = list(arr2.argsort()[-num:][::-1])

		for each in top1:
			unigram.write(str(cosine_list1[each]) +"\t"+ str(a_list[each][1]) +"\n")

		for each in top2:
			bigram.write(str(cosine_list2[each]) +"\t"+ str(a_list[each][1]) +"\n")

		unigram.write("\n\n")
		bigram.write("\n\n")

	unigram.close()
	bigram.close()'''
	uni = []
	bi = []
	for i in range(abstracts):
		print i,"\t"+ a_list[i]["name"]
		new_list_u = []
		new_list_u.append(a_list[i]["name"])
		new_list_b = []
		new_list_b.append(a_list[i]["name"])
		# write abstracts
		unigram.write(str(i+1)+")\t"+a_list[i]["name"]+"\n\n")
		bigram.write(str(i+1)+")\t"+a_list[i]["name"]+"\n\n")
		cosine_list1 = []
		cosine_list2 = []
		for j in range(texts):
			cosine_list1.append(getSimilarity(abstract_list1[i],text_list1[j]))
			cosine_list2.append(getSimilarity(abstract_list2[i],text_list2[j]))

		arr1 = np.array(cosine_list1)
		arr2 = np.array(cosine_list2)

		top1 = list(arr1.argsort()[-num:][::-1])
		top2 = list(arr2.argsort()[-num:][::-1])

		new_u = []
		new_b = []
		for each in top1:
			unigram.write(str(cosine_list1[each]) +"\t"+ str(files[each]) +"\n") # and here also we have todo changes
			new_u.append([cosine_list1[each],str(files[each])])

		for each in top2:
			bigram.write(str(cosine_list2[each]) +"\t"+ str(files[each]) +"\n")
			new_b.append([cosine_list2[each],str(files[each])])

		unigram.write("\n\n")
		bigram.write("\n\n")
		new_list_u.append(new_u)
		new_list_b.append(new_b)
		uni.append(new_list_u)
		bi.append(new_list_b)


	unigram.close()
	bigram.close()
	save_obj(uni,"unigram")
	save_obj(bi,"bigram")

if __name__ == '__main__':
	final_function("Wiki","disk_merge","papers","output_unigram.txt","output_bigram.txt",50)

