import numpy
import sys
import time
from collections import defaultdict

d = 0.85
fi = 10**-6


def page_rank(graph_size, trans_table):
    iteration = 0
    no_outlink_pagerank_sum = 0
    rank_vec = []
    rank_vec.append(numpy.ones((graph_size,)))
    rank_vec.append(numpy.zeros((graph_size,)))
    no_outlink_node = []
    for i in xrange(1, graph_size+1):
        if trans_table[i] == []:
            no_outlink_node.append(i)
    while True:
        start = time.time()
        for i in xrange(1, graph_size+1):
            if trans_table[i] != []:
                outlink_num = trans_table[i][0]
                for out_linked_node in trans_table[i][1:]:
                    rank_vec[(iteration+1)%2][out_linked_node-1] += rank_vec[(iteration%2)][i-1]/outlink_num
        
        no_outlink_pagerank_sum = 0
        for index in no_outlink_node:
            no_outlink_pagerank_sum += rank_vec[(iteration)%2][index-1]
        
        rank_vec[(iteration+1)%2] += no_outlink_pagerank_sum/graph_size
        rank_vec[(iteration+1)%2] = 0.15 + 0.85*rank_vec[(iteration+1)%2]
        end = time.time()
        print 'iteration.' + str(iteration) + ': ' + str(numpy.linalg.norm(rank_vec[0]-rank_vec[1]))
        print 'time_total' + str(end-start)
        if numpy.linalg.norm(rank_vec[0]-rank_vec[1]) < fi:
            return rank_vec[(iteration+1)%2]
        else:
            rank_vec[iteration%2] = numpy.zeros((graph_size,))
            iteration +=1


def main():
    path = sys.argv[1]
    #path to the file
    trans_table = defaultdict(list)
    #trans_table
    with open(path, 'r') as f:
        graph_size = int(f.readline().strip().split()[1])
        #size of the graph and trans_table
        print 'Read file...'
        for line in f:
            node_id, link_info = line.strip().split(':')
            trans_table[int(node_id)] = map(int,link_info.strip().split())
    
    with open('output.pagerank', 'w') as f: 
        print 'Computing page rank...'
        rank_vec = page_rank(graph_size, trans_table)
        print 'Writing page rank...'
        for i in xrange(graph_size):
            print >> f ,str(i+1) + ':' + str(rank_vec[i])

if __name__ == '__main__':
    exit(main())
