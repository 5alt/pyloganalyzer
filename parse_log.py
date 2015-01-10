# -*- coding: utf-8 -*- 
import re
from urlparse import urlparse
from common import *

def parse_log(logs):
	'Return tuple of dictionaries containing file data.'
	def make_entry(x):
		return { 
			'method':x.group('method'),
			'server_ip':x.group('ip'),
			'url':x.group('url'),
			'time':x.group('time'),
			'status_code':x.group('status_code'),
			'referral':x.group('referral'),
			'useragent':x.group('agent'),
			}
	log_re = '(?P<ip>[.:0-9a-fA-F]+) - - \[(?P<time>.*?)\] "(?P<method>.*?) (?P<url>.*?) HTTP/1.\d" (?P<status_code>\d+) \d+( "(?P<referral>.*?)")?( "(?P<agent>.*?)")?'
	search = re.compile(log_re).search
	#for each line, print the line which match the pattern
	try:
		conn = connect_to_mysql()
		cursor = conn.cursor()
		with open(logs, 'rb') as flog:
			for logline in flog:
				x = search(logline)
				if x:
					entry = make_entry(x)
					if entry['status_code'] != '404':
						entry['rule'] = apply_get_rules(entry['url'])
						if entry['rule']:
							entry['uri'] = urlparse(entry['url']).path
							entry['filename'] = logs
							entry['raw_data'] = entry['url']
							add_to_mysql(cursor, entry)
	except Exception, e:
		print e
		pass
	finally:
		conn.commit()
		cursor.close() 
		conn.close()

if __name__ == "__main__": 
	parse_log('access.log')