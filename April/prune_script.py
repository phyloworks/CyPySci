import dendropy
import glob
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
import sys

def get_files():
	flist = []
	for file in glob.glob(sys.argv[1]):
		flist.append(file)
	return(flist)

def do_prune(flist):
	print(flist)	

	ts = dendropy.TreeList.get_from_path(flist, "nexus", preserve_underscores=True, tree_offset=4000)
	retain_labels = []
	remove_labels = []

	treeZero = ts[0]
	for node in treeZero.leaf_node_iter():
			if 'T' in node.taxon.label:
				retain_labels.append(node.taxon.label)
			elif 'X' in node.taxon.label:
				remove_labels.append(node.taxon.label)	

	[tree.retain_taxa_with_labels(retain_labels) for tree in ts]
	new_name = './' + flist + '.pruned'
	print(new_name)
	[ts.taxon_namespace.remove_taxon_label(label) for label in remove_labels]
	ts.write(path = new_name, schema = 'nexus')
		
def pruneParallel(flist, threads=2):
    pool = ThreadPool(threads)
    results = pool.map(do_prune, flist)
    pool.close()
    pool.join()
    return results		

if __name__ == '__main__':		
	flist = get_files()
#	print(flist)
	pruneParallel(flist, threads=4)

