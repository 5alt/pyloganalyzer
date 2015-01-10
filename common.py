# -*- coding: utf-8 -*- 
import re
import sys 
from urllib import unquote
import MySQLdb
import config

def load_get_rules():
	rules_get = 'get_rules.txt'
	#generate pattern list
	f = open(rules_get, 'rb')
	rulelist_get = [re.compile(x.strip(), re.M|re.I) for x in f.readlines() if len(x.strip()) != 0]
	f.close()
	return rulelist_get

def load_post_rules():
	rules_post = 'post_rules.txt'
	#generate pattern list
	f = open(rules_post, 'rb')
	rulelist_post = [re.compile(x.strip(), re.M|re.I) for x in f.readlines() if len(x.strip()) != 0]
	f.close()
	return rulelist_post

def apply_get_rules(line):
	rules_get = load_get_rules()
	for rule in rules_get:
		if rule.search(unquote(line)):
			print rule.pattern + '-->' + line
			return rule.pattern
	return None

def apply_post_rules(line):
	rules_post = load_post_rules()
	for rule in rules_post:
		if rule.search(unquote(line)):
			print rule.pattern + '-->' + line
			return rule.pattern
	return None

def add_to_mysql(cursor, data):
	columns = ['method', 'status_code', 'useragent', 'filename', 'rule', 'url', 'uri', 'raw_data']
	for col in columns:
		try:
			data[col]
		except:
			data[col] = ''
	sql = "INSERT INTO `logs` (`method`, `status_code`, `useragent`, `filename`, `rule`, `url`, `uri`, `raw_data`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
	params = (data['method'], data['status_code'], data['useragent'], data['filename'], data['rule'], data['url'], data['uri'], data['raw_data'])
	cursor.execute(sql, params)

def connect_to_mysql():
	try:
		return MySQLdb.connect(host=config.mysql_host, port=3306,user=config.mysql_user, passwd=config.mysql_pwd,db=config.mysql_db, charset='utf8')
	except Exception, e:
		print e
		sys.exit()
