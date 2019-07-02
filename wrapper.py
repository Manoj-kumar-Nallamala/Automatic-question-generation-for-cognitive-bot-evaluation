import os, re
#from py2neo import Graph, Node, Relationship
import pickle
from collections import OrderedDict 

def generate_entity(s = "Does Cisco IOS XE Everest 16.6.2 has Software Features YANG Data Models."):
	#s = str(input())

	#s = '''
	#Does Cisco IOS XE Everest 16.6.1 has Hardware Features Cisco SFP.
	#Does Cisco IOS XE Everest 16.6.2 has Software Features YANG Data Models.
	#Does Cisco Catalyst 9300 Series Switches support the Cisco QSA Module.
	#Does Cisco IOS XE Everest 16.6.1 has Software Features Cisco Protocol Bypass.
	#'''

	if '(' in s:
		s = re.sub('\(.*\)[ ?]', '', s)


	in_file = "test.txt"
	with open(in_file, 'a') as f:
		f.write(s)
#		print(s)

	os.system("java -mx10g -cp './stanford-corenlp-full/*' edu.stanford.nlp.pipeline.StanfordCoreNLP -props server.properties -file %s" % in_file)

	os.remove(in_file)

	s = []
	with open(in_file+".out", 'r')as f:
		s = f.readlines()



	entity = {'PRODUCT': ['Cisco IOS XE Everest 16.6.4', 'Cisco IOS XE Everest 16.6.3', 'Cisco IOS XE Everest 16.6.2', 'Cisco IOS XE Everest 16.6.1', 'Cisco IOS XE Everest 16.5.1a', 'Cisco IOS XE Everest', 'Everest', 'Cisco IOS XE'], 'HW_FEATURE': ['MultiGigabit Ethernet', 'rear USB 3.0 port', 'Breakout cables', 'UPoE', 'UPOE', 'PoE','Universal Power Over Ethernet', 'C9300-48UXM-E', 'C9300-48UXM-A', 'C9300-24UX', 'Cisco QSA Module','SFP', 'SFP+', 'Audio Video Bridging', 'NDAC', 'Multigigabit Ethernet', '2.5G Multigigabit Ethernet', '10G UPOE', 'PoE+', '10/100/1000 Ethernet', '10/100/1000 PoE+', 'Catalyst 9300 48-port', 'Universal Power Over Ethernet', 'Network Device Admission Control'], 'SW_FEATURE': ['NSF', 'ETA', 'GIR', 'IGMP', 'LISP', 'SMU', 'SSO', 'Nonstop Forwarding Support', 'Encrypted Traffic Analytics', 'Graceful Insertion and Removal', 'Graceful Insertion', 'Graceful Removal', 'Internet Group Management Protocol', 'Virtual Private Network', 'Locator ID Separator Protocol', 'Software Maintenance Upgrade', 'Stateful Switchover', 'GRE', 'Software-defined', 'Protocol Bypass', 'SGACL', 'VPLS', 'SoO', 'eBGP', 'iBGP', 'Generic Routing Encapsulation', 'ZTP', 'iPXE', 'Source Group Access Control List', 'DNS Proxy', 'VRF-Lite', 'external BGP', 'eBGP', 'internal BGP', 'iBGP', 'Bluetooth', 'GLBP', 'PerfMon', 'VRF Aware', 'NDAC', 'AES MACsec', 'YANG Data Models', 'Stateful switchover', 'Stateful Switchover', 'Stack Manager', 'High availabiltiy', 'Ethernet over MPLS', 'Route Target Rewrite', '6PE', 'IPv6 Provider Edge', 'IPv6 VPN', 'Provider 6VPE', '6VPE', 'EIGRP', 'Preboot Execution Environment Client', 'iPXE', 'Zero-Touch Provisioning', 'ZTP', 'Model-Driven Telemetry', 'malware analysis', 'crypto audit', 'host link encryption', 'Site of Origin', 'SoO'], 'SWITCH': ['Cisco Catalyst 3850 Series', 'Cisco Catalyst 9300 Series', 'C9300-24T-E', 'C9300-24T-A', 'C9300-24P-E', 'C9300-24P-A', 'C9300-24U-E', 'C9300-24U-A', 'C9300-24UX-A', 'C9300-24UXM-E', 'C9300-24UXM-A', 'C9300-48T-E', 'C9300-48T-A', 'C9300-48P-E', 'C9300-48U-E', 'C9300-48U-A'], 'MODULE': ['Fan Module', 'C9300-NM-4M', 'MultiGigabit Ethernet Uplink Network Module', 'Network Module', 'Transciever Module', 'C9300-NM-8X', 'C9300-NM-4G', 'C9300-NM-8X', 'C9300-NM-2Q', 'C3850-NM-4-1G', 'C3850-NM-2-10G', 'C3850-NM-4-10G', 'C3850-NM-8-10G', 'C3850-NM-2-40G'], 'VERSION': ['Software Version', 'Hardware Version', 'Release Version', 'Version'], 'CONFIG': ['Software Configuration', 'Hardware Configuration', 'Configuration', 'Stack Set-up', 'Set-up', 'Processor Speed', 'DRAM', 'Number of Colors', 'Resolution', 'Font Size', '80G uplink', '480 Gigabit', '80G uplink', 'bandwidth'], 'NET_TYPE': ['LAN', 'WAN', 'VPN', 'IPsec VPN', 'multicast device', 'multicast hosts', 'multiaccess network'], 'PMA': ['Multiprotocol Label Switching', 'BGP', 'Routing', 'SHA-2', 'SHA-1', 'SHA-128', 'SHA-256', 'Method', 'SSH', 'Encryption', 'IS-IS', 'Bump-in-the-wire', 'Border Gateway', 'IPv6', 'IPv4 command', 'IPv4 MPLS', 'VPN IPv6', 'MPLS', 'GLBP'], 'DLRIL': ['Description / Information', 'File', 'URL'], 'SOFTWARE': ['Boot Loader', 'Microcode', 'CAT9K_IOSXE', 'Google Chrome', 'Microsoft Internet Explorer', 'Mozilla Firefox', 'Safari', 'Chrome', 'Windows 7', 'Mac OS X 10.11'], 'COMMAND': ['EXEC', 'clean', 'copy', 'describe', 'expand', 'install', 'uninstall', 'verify', 'add file tftp', 'activate', 'commit', 'rollback to committed', 'abort', 'remove'], 'LICENCE': ['Network Essentials', 'Network Advantage', 'Right-to-use', 'RTU', 'DNA Essentials', 'DNA Advantage', 'Add-on license', 'Licence Levels'], 'CAPABILITIES': ['Security', 'IoT', 'Mobility', 'Cloud'], 'LAYERS': ['Layer1', 'Layer2', 'Layer3'], 'ARCHITECTURE': ['ASIC architecture', 'Unified Access Data Plane', 'UADP', 'SD-Access', '128-bit', '256-bit', 'x86', '64-bit'], 'POWER_MODE': ['StackWise-480', 'StackPower', 'Stackable 24', '490W with 1100 WAC', '350 WAC', '715 WAC', '1100 WAC']}


	ner_1,ner_2, relation, key1, key2 = [],[],[],[],[]
	for i, e in enumerate(s):
		if 'RelationMention' in e:
			rel = e
			relation.append(re.sub('type|[[=,]','',rel.split()[1]))

		elif 'NER' in e:
			n_1 = s[i+1]
			nerr_1 = ' '.join(n_1.split()[:-2])
			ner_1.append(nerr_1)
				
			if s[i+2] != '\n':
				if '?' in s[i+2]:
					n_2 = s[i+2].replace('?','')
					nerr_2 = ' '.join(n_2.split()[:-2])		
					ner_2.append(nerr_2)
	
				else:
					n_2 = s[i+2]
					nerr_2 = ' '.join(n_2.split()[:-2])		
					ner_2.append(nerr_2)
			
	'''
			if s[i+3] != '\n':
				n_3 = s[i+3]
				nerr_3 = ' '.join(n_3.split()[:-2])		
				ner_2.append(nerr_3)
		
				if s[i+4] != '\n':
					n_4 = s[i+4]
					nerr_4 = ' '.join(n_4.split()[:-2])		
					ner_2.append(nerr_4)

					if s[i+5]:
						n_5 = s[i+5]
						nerr_5 = ' '.join(n_5.split()[:-2])		
						ner_2.append(nerr_5)
	'''		
			
	'''
	g = Graph(host="localhost", password="tcs@12345")
	g.delete_all()
	tx = g.begin()
	'''
	#if len(relation) == len(ner_2):
	#	ner_1 = ner_1 * len(relation)

	list_of_triples = []
	for n1, r, n2 in zip(ner_1, relation, ner_2):
	#	print(n1, r, n2)
		list_of_triples.append([n1, r, n2])



	with open("cisco_triples.pickle","wb") as pi:
		pickle.dump(list_of_triples, pi)

	with open("cisco_triples.pickle", "rb") as fp:   # Unpickling
		l = pickle.load(fp)
	#	for t in l:
	#		print(t)
		

	#print("-"*20,ner_1, relation, ner_2)	



	k1,k2,ab = '','',''
	d = OrderedDict()

	for i1, r, i2 in zip(ner_1, relation, ner_2):
		#print("^"*50,i1, i2)
		if '.' in i2:
			i2 = i2.replace(".","")
		for k, v in entity.items():
			if i1 in v:
				k1 = k
			elif i2 in v:
				k2 = k

#		print("/"*20,k1, i1, r, k2, i2)
		d[k1] = i1
		d[k2] = i2
#	print(d)
	return d


print(generate_entity())
'''
	a = Node(k1, name=i1)
	tx.create(a)
	
	b = Node(k2, name=i2)
	tx.create(b)

	ab = Relationship(a, r, b)
	tx.create(ab)



tx.commit()
'''
#g.run("match (a:PRODUCT) return a.SW_FEATURE limit 2").to_data_frame()
#g.exists(ab)



#g = Graph(host="localhost", password="tcs@12345")
#tx = g.begin()

#a = Node("Person", name="Alice")
#tx.create(a)

#b = Node("Person", name="Bob")
#ab = Relationship(a, "KNOWS", b)


#tx.create(ab)
#tx.commit()
#g.exists(ab)
