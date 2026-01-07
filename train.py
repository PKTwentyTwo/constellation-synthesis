'''This is the program to generate training data for the main program.'''
import os
import subprocess
import sys
import lifelib
import dataman

#Set up the lifetree:
if len(sys.argv) > 1:
    rule = sys.argv[1]
else:
    rule = input('Enter a rule.\n>')
rule = rule.replace('/', '').lower()
try:
    sess = lifelib.load_rules(rule)
except:
    print('Rule '+rule+' not valid, defaulting to b3s23...')
    sess = lifelib.load_rules('b3s23')
lt = sess.lifetree(n_layers = 1, memory = 1000)
#Time for my favourite part of functional programming: creating a giant pile of functions
#that will collapse as soon as one thing goes wrong.

