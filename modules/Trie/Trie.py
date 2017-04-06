import os
import sys
import pymongo as pmn
from recordtype import recordtype
#would require a nltk library at this place

MyStruct = recordtype("MyStruct", "ip branches leaf parent words depth")

class Trie :
	def __init__(self) :
		self.trie_root = MyStruct(ip='127.0.0.1', branches={}, leaf=False, parent = "",  words=[], depth = 0)
		'''
		Every time a init occurs we will...
		retrieve the words from a pymonga database and ...
		and construct the new trie !
		and also the data base connection will be used fortemp_pointer_root.
		'''
		#self.connection = pymongo.Connection()


	def insert(self, filename) :
		# a database stub mongo-db so that we can insert any new word request that comes ----------->
		self.curr_word = filename
		split_filename_result = self.split_filename(filename)

		for each_word in split_filename_result :
			#each_word = lemmatized word
			self.update(each_word.lower()) # all lower case words


	def update(self, word) :
		#may be for update and read we should use mutexes in each branch of the tree  ---------->
		word_length = len(word)
		temp_pointer_root = self.trie_root
		for char in word :
			word_length -= 1
			print char,

			if char in temp_pointer_root.branches :
				print " --> ok"
				temp_pointer_root = temp_pointer_root.branches[char]
			else :
				print " --> not ok"
				last_pointer = temp_pointer_root  #parent
				temp_pointer_root =  MyStruct(ip='127.0.0.1', branches={}, leaf=False, parent = last_pointer, words=[], depth = 0)
				last_pointer.branches.update({char : temp_pointer_root}) # updating child pointer of parent

			if word_length == 0 : #last charecter
				print word
				temp_pointer_root.words += [self.curr_word]

		#update weight
		self.update_weight_bottom_up(word, temp_pointer_root)


	def update_weight_bottom_up(self, word, temp_pointer_root):
		#this additional complexity is to push a part of the tree into a different 
		depth = 1
		parent_updated = True

		# if the last charecter is not a new leaf taht was added into the tree 
		# then this tree would not work
		while parent_updated  :  # either root reached or not required
			#over here there should be a procedure to shift tree to a new place on the basis of branches and depth ---------->
			print temp_pointer_root.parent.depth
			
			if depth > temp_pointer_root.parent.depth : 
				temp_pointer_root.parent.depth = depth
			else :
				parent_updated = False
			temp_pointer_root = temp_pointer_root.parent

			if temp_pointer_root.parent == "" :
				break



	def search(self, filename) :
		# a database stub mongo-db so that we can insert any new word request that comes ----------->
		split_filename_result = self.split_filename(filename)

		result_array = []  # this will be used to calculate the rank of the search strings

		for each_word in split_filename_result :
			#each_word = lemmatized word
			result = self.lookup(each_word)

			if not result == False :
				result_array += [result] 
				# result[0] .. contains lookup array of work 1
				# result[1] .. contains lookup array of work 2

		return result_array



	def lookup(self, word) :
		word_length = len(word)
		temp_pointer_root = self.trie_root

		for char in word :
			word_length -= 1

			if char in temp_pointer_root.branches :
				temp_pointer_root = temp_pointer_root.branches[char]
			else :
				return False

			if word_length == 0 :
				return temp_pointer_root.words



	def split_filename(self,filename) :
		#assuming that the file has an extension at the end wwhich we should ignore
		filename = filename.strip()
		split_filename_result = filename.split()
		split_filename_result[-1] = split_filename_result[-1].split('.')[0]

		return split_filename_result


def main() :
	argv = sys.argv
	file = argv[1]

	fHandle = open(file, "r")
	data = fHandle.read()
	fHandle.close()

	t_obj = Trie()

	for line in data.split('\n') :
		t_obj.insert(line)

	print "Searching : therefore : ",
	result = t_obj.search("therefore")
	print result

	print "Searching : the : ",
	result = t_obj.search("the")
	print result

	print "Searching : deep : ",
	result = t_obj.search("deep")
	print result

if __name__ == "__main__" :
	main()