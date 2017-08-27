import os
import sys
from recordtype import recordtype
#would require a nltk library at this place

MyStruct = recordtype("MyStruct", "ip branches leaf parent words depth")

#mongo still needed

mast_ip = '172.20.52.8'

class Trie :
	def __init__(self) :
		self.trie_root = MyStruct(ip=mast_ip, branches={}, leaf=False, parent = "",  words=[], depth = 0)
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
		split_filename_result = self.split_filename(filename[:filename.find('<')])

		print "Filenames ",split_filename_result

		for each_word in split_filename_result :
			
			#each_word = lemmatized word
			print "each word is :",each_word
			self.update(each_word.lower()) # all lower case words

		#print self.trie_root



	def update(self, word) :
		#may be for update and read we should use mutexes in each branch of the tree  ---------->
		word_length = len(word)
		#print "word in upation is :",word
		temp_pointer_root = self.trie_root
		for char in word :
			word_length -= 1
		#	print char,

			if char in temp_pointer_root.branches :
			#	print " --> ok"
				temp_pointer_root = temp_pointer_root.branches[char]
			else :
			#	print " --> not ok"
				last_pointer = temp_pointer_root  #parent
				temp_pointer_root =  MyStruct(ip='172.26.34.190', branches={}, leaf=False, parent = last_pointer, words=[], depth = 0)
				last_pointer.branches.update({char : temp_pointer_root}) # updating child pointer of parent

			temp_pointer_root.words += [self.curr_word.lower()]

			#if word_length == 0 : #last charecter
				#print self.curr_word + 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk'
			#	temp_pointer_root.words += [self.curr_word]
				#print "Collection of words : ",temp_pointer_root.words

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
		#	print "Depth is :" ,temp_pointer_root.parent.depth
			
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
		#print result_array

		return result_array


	def search_get_json2(self, filename) :
		# a database stub mongo-db so that we can insert any new word request that comes ----------->
		split_filename_result = self.split_filename(filename)

		result_dic = {}  # this will be used to calculate the rank of the search strings

		for each_word in split_filename_result :
			#each_word = lemmatized word
			result = self.lookup(each_word)
			print result
			print "------------"

			if not result == False :
				#result_dic.update({each_word:result})
				for elem in result :
					print elem + 'kkk'
					part1 = elem[:elem.find('<')]
					part2 = elem[elem.find('>') + 1:]
					print part1
					print part2
					if not each_word in result_dic :
						result_dic.update({each_word : {part2:[part1]}})
						#print result_dic
					else :
						if not part2 in result_dic[each_word] :
							result_dic[each_word].update({part2:[part1]})
						else :
							if not part1 in result_dic[each_word][part2] :
								result_dic[each_word][part2] += [part1]
						#print result_dic
				# result[0] .. contains lookup array of work 1
				# result[1] .. contains lookup array of work 2

		return result_dic



	def search_get_json(self, filename) :
		filename = filename.lower()
		print "Now searching in trie :"
		# a database stub mongo-db so that we can insert any new word request that comes ----------->
		split_filename_result = self.split_filename(filename)
		count = -1
		result_dic = {}  # this will be used to calculate the rank of the search strings

		#print "file is ",split_filename_result

		for each_word in split_filename_result :
			#each_word = lemmatized word
			
			result = self.lookup(each_word)
		#	print result
		#	print "------------"

			if not result == False :
				#result_dic.update({each_word:result})
				for elem in result :
					count += 1
		#			print elem + 'kkk'
					part1 = elem[:elem.find('<')]
					part2 = elem[elem.find('>') + 1:]
					result_dic.update({count : {'filename' : part1, 'id' :part2}})
					#result_dic.update({count : {'filename' : elem}})
		return result_dic



	def lookup(self, word) :
		word_length = len(word)
		print "Lookign up for the wor"
		temp_pointer_root = self.trie_root

		for char in word :
			word_length -= 1
			print "char :",char

			if char in temp_pointer_root.branches :
				temp_pointer_root = temp_pointer_root.branches[char]
			else :
				return False

			if word_length == 0 :
				print "word len is 0", temp_pointer_root.words
				return temp_pointer_root.words



	def split_filename(self,filename) :
		#assuming that the file has an extension at the end wwhich we should ignore
		filename = filename.strip()
		split_filename_result = filename.split()
		split_filename_result[-1] = split_filename_result[-1].split('.')[0]

		return split_filename_result


'''def main() :
	argv = sys.argv
	file = argv[1]

	print "testng"
	
	fHandle = open(file, "r")
	data = fHandle.read()
	fHandle.close()

	t_obj = Trie()

	for line in data.split('\n') :
		t_obj.insert(line)

	print "Searching : client333 : ",
	result = t_obj.search_get_json("client333.py")
	print result

	print "Searching : client333.py : ",
	result = t_obj.search_get_json("client333.py")
	print result

	print "Searching : deep : ",
	result = t_obj.search_get_json("deep")
	print result
	
	t_obj = Trie()
	t_obj.insert("swarnima<id>3434")
	t_obj.insert("swarn.py<id>3434")
	t_obj.insert("swarni.py<id>3434")
	t_obj.insert("swart.py<id>3434")
	t_obj.search_get_json("swar.py")

if __name__ == "__main__" :
	main()
'''
