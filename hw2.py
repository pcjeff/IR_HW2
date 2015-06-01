import numpy
import sys, getopt
import time
from collections import defaultdict

d = 0.85
fi = 10**-6
output_file = 'test.pagerank'

def page_rank(graph_size, trans_table):
    iteration = 0
    no_outlink_pagerank_sum = 0
    rank_vec = []
    rank_vec.append(numpy.ones((graph_size,), dtype=numpy.float64))
    rank_vec.append(numpy.zeros((graph_size,), dtype=numpy.float64))
    no_outlink_node = []
    for i in xrange(1, graph_size+1):
        if trans_table[i] == []:
            no_outlink_node.append(i)
    while True:
        start = time.time()
        no_outlink_pagerank_sum = 0
        for i in xrange(1, graph_size+1):
            if trans_table[i] != []:
                outlink_num = trans_table[i][0]
                for out_linked_node in trans_table[i][1:]:
                    rank_vec[(iteration+1)%2][out_linked_node-1] += rank_vec[(iteration%2)][i-1]/outlink_num
                #with outlink
            else:
                rank_vec[(iteration+1)%2][i-1] -= rank_vec[(iteration)%2][i-1]/(graph_size-1)
                no_outlink_pagerank_sum += rank_vec[(iteration)%2][i-1]
                #no outlink 
        rank_vec[(iteration+1)%2] += no_outlink_pagerank_sum/(graph_size-1)
        rank_vec[(iteration+1)%2] = (1-d) + d*rank_vec[(iteration+1)%2]
        end = time.time()
        print 'iteration.' + str(iteration) + ': ' + str(numpy.linalg.norm(rank_vec[0]-rank_vec[1]))
        print 'time_total: ' + str(end-start)
        if numpy.linalg.norm(rank_vec[0]-rank_vec[1]) < fi:
            return rank_vec[(iteration+1)%2]
        else:
            rank_vec[iteration%2] = numpy.zeros((graph_size,))
            iteration +=1
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:e:o:")
    except getopt.GetoptError:
        print 'getopt error'
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-d', '--damp_factor'):
            d = float(arg)
        elif opt in ('-e', '--epsilon'):
            fi = float(arg)
        elif opt in ('-o', '--ouput'):
            output_file = arg
        else: 
            print 'unhandled arg: ' + opt
    if len(args)==1:
        input_file = args[0] 
    else:
        print 'error num of input file, must be one'
    trans_table = defaultdict(list)
    #trans_table
    with open(input_file, 'r') as f:
        graph_size = int(f.readline().strip().split()[1])
        #size of the graph and trans_table
        print 'Read file... ' + input_file
        for line in f:
            node_id, link_info = line.strip().split(':')
            trans_table[int(node_id)] = map(int,link_info.strip().split())
    
    with open(output_file, 'w') as f: 
        print 'Computing page rank...'
        rank_vec = page_rank(graph_size, trans_table)
        print 'Writing page rank...' + output_file
        for i in xrange(graph_size):
            print >> f ,str(i+1) + ':' + str(rank_vec[i])

if __name__ == '__main__':
    exit(main())
