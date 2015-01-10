# -*- coding: utf-8 -*- 
import os, re
import pickle
from Queue import Queue 
import time
import parse_pcap, parse_log
import threading
import config


#os.chdir() os.remove() os.removedirs os.walk

def get_data_path():
	return os.getcwd()+os.sep+'data'+os.sep

def check_file_change():
	hash_table = 'file.table'

	file_tables = {}

	if os.path.exists(hash_table) and os.path.getsize(hash_table)>0:
		# load dict
		f = open(hash_table,"rb")
		file_tables = pickle.load(f)
		f.close()

	file_list = os.listdir(get_data_path())
	for filename in file_list:
		try:
			file_tables[filename] #check new file or not
		except:
			file_tables[filename] = 0 #if new set idle

	print file_tables

	for filename in file_tables:
		if file_tables[filename] == 0:
			ext = os.path.splitext(filename)[1]
			if ext == '.pcap':
				add_to_queue({'filename':filename, 'type': 'pcap'})
			elif ext == '.log':
				add_to_queue({'filename':filename, 'type': 'log'})
			else:
				pass #add tshark process
			file_tables[filename] = 1 #set processing

	# save dict
	f = open(hash_table,"wb")
	pickle.dump(file_tables, f)
	f.close()

def add_to_queue(item):
	global queue
	queue.put(item)

def worker():
	global queue
	while True:
		try:
			item = queue.get()
			print 'Proccessing ' + item['filename']
			if item['type'] == 'pcap':
				parse_pcap.parse_pcap(get_data_path()+item['filename'])
			elif item['type'] == 'log':
				parse_log.parse_log(get_data_path()+item['filename'])
		except Exception, e:
			print e
		finally:
			queue.task_done()

if __name__ == "__main__": 
	queue = Queue()
	while True:
		if queue.empty():
			time.sleep( config.check_interval )
			check_file_change() #check every 3 sec
		else:
			for i in range(config.num_worker_threads):
				t = threading.Thread(target=worker)
				t.daemon = True
				t.start()
			queue.join()   # block until all tasks are done


