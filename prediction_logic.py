## json node doc representation

# {
# 	"node_key": "unique key ",
# 	"node_info": {},
# 	"childs": [{node1},{node2}, ..],
# 	"creation_time": "1110101425"
# }

import pickle
import os
from datetime import datetime

class Logic:

	__nodes_detail = dict()
	__sessions = []
	# __nodes = None

	def __init__(self):
		try:
			print("in constructor")
			with open(os.getcwd()+"/node_details.pickle","r") as f:
				self.__nodes_detail = pickle.load(f)
			with open(os.getcwd()+"/sessions.pickle","r") as f:
				self.__sessions = pickle.load(f)
			# with open(os.getcwd()+"/nodes.pickle","r") as f:
			# 	self.__nodes = pickle.load(f)
		except IOError:
			with open(os.getcwd()+"/node_details.pickle","w") as f:
				pickle.dump({},f)
				self.__nodes_detail = {}
			with open(os.getcwd()+"/sessions.pickle","w") as f:
				pickle.dump([],f)
				self.__sessions = []
			# with open(os.getcwd()+"/nodes.pickle","w") as f:
			# 	pickle.dump([],f)
			# 	self.__nodes = []


	def add(self,moved_from="",for_node=None,moved_to=None,time="",session_id="",id=""):
		try:
			if for_node is not None and moved_to is not None:
				d = dict()
				d['from_node'] = moved_from
				d['time'] = time
				d['to_node'] = moved_to
				d['session'] = session_id
				d['id'] = id

				if self.__nodes_detail.has_key(str(for_node)):
					#track according to node moved to
					if str(moved_to) in self.__nodes_detail[str(for_node)]['moved_to'].keys():
						self.__nodes_detail[str(for_node)]['moved_to'][str(moved_to)].append(d)
					else:
						self.__nodes_detail[str(for_node)]['moved_to'][str(moved_to)] = [d]

					#track according to node moved from
					if str(moved_from) in self.__nodes_detail[str(for_node)]['moved_from'].keys():
						self.__nodes_detail[str(for_node)]['moved_from'][str(moved_from)].append(d)
					else:
						self.__nodes_detail[str(for_node)]['moved_from'][str(moved_from)] = [d]
				
				else:
					ndict = dict()
					ndict['node_key'] = for_node
					ndict['node_info'] = ""
					ndict['moved_to'] = { str(moved_to):[d] }
					ndict['moved_from'] = { str(moved_from): [d]}
					ndict['creation_time'] = datetime.today().isoformat()
					self.__nodes_detail[str(for_node)] = ndict
			else:
				raise Exception("arguments cannot be 'None'")
		except Exception as e:
			return str(e)

	def get_next_node(self,moving_from,previous_node=None,conditional=False):
		try:
			if conditional is False:#algo no previous dependency
				if self.__nodes_detail.has_key(str(moving_from)):
					future_node = None
					count_temp = 0
					for node in self.__nodes_detail[str(moving_from)]['moved_to'].keys():
						if len(self.__nodes_detail[str(moving_from)]['moved_to'][str(node)]) > count_temp:
							count_temp = len(self.__nodes_detail[str(moving_from)]['moved_to'][str(node)])
							future_node = str(node)
					print "--- f node state ---"
					print future_node
					return self.returning_node_structure(future_node)
				else:
					raise Exception("Node DoesNotExist")

			else:#algo for previous dependency ,conditional dependency
				if previous_node is not None:
					fnode_count_tracker = dict()
					for node in self.__nodes_detail[str(moving_from)]['moved_from'][str(previous_node)]:
						try:
							print fnode_count_tracker

							fnode_count_tracker[str(node['to_node'])] = fnode_count_tracker[str(node['to_node'])]+1
						except KeyError:
							fnode_count_tracker[str(node['to_node'])] = 1

					future_node = None
					count_temp = 0
					print fnode_count_tracker
					for key in fnode_count_tracker.keys():
						if int(fnode_count_tracker[str(key)]) > count_temp:
							future_node = str(key)
							count_temp = int(fnode_count_tracker[str(key)])

					return self.returning_node_structure(future_node)
				else:
					raise Exception("'previous_node' cannot be None .")

		except Exception as e:
			print e
			return str(e)

	
	def returning_node_structure(self,node_key):
		try:
			node = dict()
			node['key'] = self.__nodes_detail[str(node_key)]['node_key']
			node['creation_time'] = self.__nodes_detail[str(node_key)]['creation_time']
			node['info'] = self.__nodes_detail[str(node_key)]['node_info']
			return node
		except KeyError:
			return {'key':str(node_key)}

	def fetch_traversal(self,session_id):
		pass


	def __del__(self):
		# before descructing
		print("in destructor")
		with open(os.getcwd()+"/node_details.pickle","w") as f:
			pickle.dump(self.__nodes_detail,f)
		with open(os.getcwd()+"/sessions.pickle","w") as f:
			pickle.dump(self.__sessions,f)



## Docs :
## Node structure in storage

# {'sam': {'creation_time': '2018-03-06T12:38:12.188388',
#          'moved_from': {'a': [{'from_node': 'a',
#                                'session': 'xyz',
#                                'time': '',
#                                'to_node': 'b'},
#                               {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'b'},
#                               {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'b'},
#                               {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'c'},
#                               {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'd'},
#                               {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'd'},
#                               {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'e'},
#                               {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'c'},
#                               {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'b'},
#                               {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'b'}
#                               ],
#                         'c': [{'from_node': 'c', 'session': 'xyz', 'time': '', 'to_node': 'b'}],
#                         'd': [{'from_node': 'd', 'session': 'xyz', 'time': '', 'to_node': 'b'}]
#                         },

#          'moved_to': {'b': [{'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'b'},
#                             {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'b'},
#                             {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'b'},
#                             {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'b'},
#                             {'from_node': 'c', 'session': 'xyz', 'time': '', 'to_node': 'b'},
#                             {'from_node': 'd', 'session': 'xyz', 'time': '', 'to_node': 'b'},
#                             {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'b'}
#                             ],
#                       'c': [{'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'c'},
#                             {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'c'}],
#                       'd': [{'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'd'},
#                             {'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'd'}],
#                       'e': [{'from_node': 'a', 'session': 'xyz', 'time': '', 'to_node': 'e'}]
#                       },
#          'node_info': '',
#          'node_key': 'a'}
# }