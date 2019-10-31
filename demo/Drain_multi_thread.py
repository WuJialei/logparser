#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import time, threading
sys.path.append('../')
from logparser import Drain

input_dir  = '../logs/test/'  # The input directory of log file
output_dir = 'Drain_test_result/'  # The output directory of parsing results
'''
0: access.log #/apache2		'<a> <b> <c> <d> <e> <f> <Content>'
1: cinder_error.log #/apache2		'<a> <b> <c> <d> <e> <Content>'
2: error.log.1 #/apache2		'<a> <b> <c> <d> <e> <Content>'
3: keystone_access.log #/apache2 	'<a> <b> <c> <d> <Content>'
4: nova_placement_access.log #/apache2 		'<a> <b> <c> <d> <e> <Content>'
5: nova_placement_error.log.1 #/apache2 	'<a> <b> <Content>'
'''
log_files   = ['access.log', 
				'cinder_error.log',
				'error.log.1',
				'keystone_access.log',
				'nova_placement_access.log',
				'nova_placement_error.log.1']  # The input log file name
log_formats = ['<a> <b> <c> <d> <e> <f> <Content>', 
			   '<a> <b> <c> <d> <e> <Content>',
			   '<a> <b> <c> <d> <e> <Content>',
			   '<a> <b> <c> <d> <Content>',
			   '<a> <b> <c> <d> <e> <Content>',
			   '<a> <b> <Content>']  # HDFS log format
cnt = 6


# Regular expression list for optional preprocessing (default: [])
regex      = [
    r'blk_(|-)[0-9]+' , # block id
    r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)', # IP
    r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$', # Numbers
]
st         = 0.5  # Similarity threshold
depth      = 4  # Depth of all leaf nodes


#call LogParser
def call_logParser(n, in_dir, out_dir, dep, st_v, rex_v):
	parser = Drain.LogParser(log_formats[n], indir=in_dir, outdir=out_dir,  depth=dep, st=st_v, rex=rex_v)
	parser.parse(log_files[n])


for i in range(cnt):
	t = threading.Thread(target=call_logParser, args=(i, input_dir, output_dir, depth, st, regex), name='{}_{}'.format('thread', log_files[i]))
	t.start()

