# Author: April Wright
# License: BSD
# Usage:
# python parse_script.py true_tree '*extension'
# in which the true tree is the tree while the true dates, and *extension is the extension
# of the sim replicants. *extension MUST be in quotes, or glob won't expand it right.

# coding: utf-8
import dendropy
from dendropy.calculate import treemeasure
import pandas
import sys
import glob
import numpy as np
right_vecmin = []
right_vecmax = []

def initializer():
#Load Tree
	tree = dendropy.Tree.get(path=sys.argv[1], schema="nexus", rooting="force-unrooted")
#Get Edges from tree
	edges = [edge.length for edge in tree.preorder_edge_iter()]
	edges[0] = 0
#Start a pandas dataframe
	df = pandas.DataFrame(pandas.Series(edges, edges),columns=['true'])
#Use the correct edges as the header
	return(df)

def get_tree_list():
	container = [file for file in glob.glob(sys.argv[2])]
	treelist = dendropy.TreeList()	
	for file in container:
		print("processing file %s" % file)
		tree = dendropy.Tree.get(path=file, schema="nexus", extract_comment_metadata=True, rooting="default-unrooted")
		treelist.append(tree)
	return(treelist, container)
	
def proc_trees(treelist):
	print treelist
	df_list = []
	for tree in treelist:
		print('Calculating tree: %s' % tree)
		node_hpd = [nd.annotations.findall(name='length_hpd95') for nd in tree.preorder_node_iter()]
		node_med = [nd.annotations.findall(name='length_median') for nd in tree.preorder_node_iter()]
		kvs = [nd.values_as_dict() for nd in node_hpd]
		gnocchi = [kv.values() for kv in kvs]
		max = [line[0][1] for line in gnocchi]
		min = [line[0][0] for line in gnocchi]
		df['min'] = pandas.Series(min, index=df.index)
		df[['min']] = df[['min']].astype(float)
		df['max'] = pandas.Series(max, index=df.index)
		df[['max']] = df[['max']].astype(float)
		df['boolcol'] = df['min'] < df['true']
		df['boolcolmax'] = df['max'] > df['true']
		kvs = [nd.values_as_dict() for nd in node_med]
		gnocchi = [kv.values() for kv in kvs]
		med = [float(line[0]) for line in gnocchi]
		df['med'] = pandas.Series(med, index=df.index)
		df['devcol'] = df['med'] - df['true']
		df_list.append(df)
	return(df_list)

def count_correct(df_list, container):
	for file in container:
		print('Exporting %s' % file)
		for df in df_list:
			min_true = (df.boolcol==True).sum()
			max_true = int((df.boolcolmax==True).sum())
			count = int(df.boolcol.count())
			df.to_csv("%s.csv" % file)
		
	return(min_true, max_true)	
	
#def io_time(df, file):
	
	
if __name__ == "__main__":
	df = initializer()
	treelist, file = get_tree_list()
	df_list = proc_trees(treelist)
	min, max = count_correct(df_list, file)
