#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import time, threading
sys.path.append('../')
from logparser import Drain

input_dir  = '../logs/'  # The input directory of log file
output_dir = 'Drain_test_result/'  # The output directory of parsing results
'''
0: auth.log
1: kern.log
2: Xorg.0.log
'''
log_files   = ['auth.log', 'kern.log', 'Xorg.0.log']  # The input log file name
log_formats = ['<a> <b> <c> <d> <e> <f> <Content>', 
			   '<a> <b> <c> <d> <e> <f> <g> <Content>',
			   '<a> <b> <Content>']  # HDFS log format
cnt = 3


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
