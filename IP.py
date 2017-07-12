from netifaces import interfaces, ifaddresses, AF_INET

class IP:
	def __init__(self):
		pass

	def get_my_ip(self):
		for ifaceName in interfaces():
			addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
			# print '%s: %s' % (ifaceName, ', '.join(addresses))
			addresses = [x for x in addresses if x.find('127') == -1 and x.find('No') == -1]
			if len(addresses):
				return addresses[0]
		return None

print IP().get_my_ip()