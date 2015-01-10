# -*- coding: utf-8 -*- 
import re
import dpkt
from urlparse import urlparse
from common import *

#http://www.commercialventvac.com/dpkt.html#mozTocId319619 for reference
#tshark -r capture2014-12-20_20_14_59.pcap -2 -R "http.request.method==GET || http.request.method==POST" -F pcap -w outfile.pcap


def parse_pcap(filename):
	try:
		f = open(filename, 'rb')
	except:
		print "Error reading file. Please make sure the file exists"
		return
		
	try:
		pcap = dpkt.pcap.Reader(f)
	except:
		print "Error reading file. Please make sure the file is a valid pcap file."
		return

	flag = True
	for ts, buf in pcap:
		if flag:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			#make sure we are dealing with ip (2048)
			if type(ip) == str:
				flag = False
			elif not eth.type ==2048:
				continue
		if not flag:
			ip = dpkt.ip.IP(buf)
		#make sure we are dealing with tcp (proto=6)
		if ip.p == 6:
			tcp = ip.data
			#assuming http is running on port 80 tcp.dport == 80 and dst.ipaddr is our ip!!!
			if len(tcp.data) > 0:
				index = 1
				getvals = ""
				try:
					#mysql connect
					conn = connect_to_mysql()
					cursor = conn.cursor()
					http = dpkt.http.Request(tcp.data)
					url = http.uri
					#build entry data
					entry = {}
					entry['url'] = url
					entry['filename'] = filename
					entry['useragent'] = http.headers['user-agent']
					entry['method'] = http.method
					entry['status_code'] = 'unknown'
					entry['uri'] = urlparse(entry['url']).path
					entry['rule'] = apply_get_rules(url)
					if entry['rule']:
						entry['raw_data'] = entry['url']
						add_to_mysql(cursor, entry)
					#deal with post data
					if http.method == "POST":
						#print url
						entry['rule'] = apply_post_rules(http.body) #TODO
						if entry['rule']:
							entry['raw_data'] = http.body
							add_to_mysql(cursor, entry)
				except Exception, e:
					#print e
					pass
				finally:
					conn.commit()
					cursor.close() 
					conn.close()
		
	f.close()
#dpkt.http.Request.headers {'host': 'www.kame.net', 'connection': 'Keep-Alive', 'accept': '*/*', 'user-agent': 'Wget/1.12 (linux-gnu)'}
#dpkt.http.Request.body
#dpkt.http.Reply.status
#dpkt.http.Reply.body
#dpkt.http.Reply.headers
if __name__ == "__main__": 
	parse_pcap('sqlmap.pcap')
