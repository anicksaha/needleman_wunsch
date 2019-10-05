import sys, os
import argparse
import random
import matplotlib.pyplot as plt
from standard_needleman import needleman_wunsch
from standard_needleman import compute
from anchored_needleman import anchored_needleman_wunsch
import time
import numpy as np

def make_arg_parser():
    parser = argparse.ArgumentParser(prog='main.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-q","--query",
                      default=argparse.SUPPRESS,
                      required=True,
                      help="Path to query fasta [required]")
    parser.add_argument("-r","--reference",
                      default=argparse.SUPPRESS,
                      required=True,
                      help="Path to reference fasta [required]")
    parser.add_argument("-m","--matches",
                      default=None,
                      help="Path to Matches file [optional]")
    return parser

def read_sequence(filepath):
    with open(filepath) as f:
        s = f.readlines()
    res = ''
    for i in range(1,len(s)):
       res += s[i].rstrip()
    return res

def read_matches(filepath):
    matches = []
    with open(filepath) as f:
        for line in f:
            line_list = line.strip().split("\t")
            line_list = [int(i) for i in line_list] # convert to int
            matches.append(line_list)
    return matches

# python main.py -q Human_HOX.fa -r Fly_HOX.fa -m Match_HOX.txt

if __name__ == '__main__':
    parser = make_arg_parser()
    args = parser.parse_args()
    Q = read_sequence(filepath = args.query)
    R = read_sequence(filepath = args.reference)
    
    if args.matches == None:
        matches_ = None
    else:
        matches_ = read_matches(filepath=args.matches)

    gap_penalty = -2
    match_score = 1
    mismatch_score = -3

    if matches_ == None:
        # Standard Needleman-Wunsch
        [score, query_with_gaps, ref_with_gaps] = needleman_wunsch(Q = Q, R = R,
            gap_penalty = gap_penalty, match_score = match_score, mismatch_score = mismatch_score)
    else:
        # Anchored Needleman-Wunsch
        [score, query_with_gaps, ref_with_gaps] = anchored_needleman_wunsch(Q = Q, R = R,
            matches = matches_, gap_penalty = gap_penalty, match_score = match_score, mismatch_score = mismatch_score)

    print(compute(query_with_gaps,ref_with_gaps))
    print('Score: ' + str(score) + '\n')
    print('Aligned Query Sequence: ' + '\n' + query_with_gaps + '\n' )
    print('Aligned Reference Sequence: ' + '\n' + ref_with_gaps + '\n')

    # Random sequences 10,000 times   
 
    scores_random_sequences = []

    t1 = time.clock()

    idx = 1
    Q_ = list(Q)
    R_ = list(R)
    for i in range(1000):
        print(idx)
        idx+=1
        
        Q_ = np.random.permutation(Q_)
        R_ = np.random.permutation(R_)
        # random.shuffle(Q_)
        # random.shuffle(R_)
        Q_rand = "".join(Q_)
        R_rand = "".join(R_)
    
        if matches_ == None:
            # Standard Needleman-Wunsch
            [curr_score,_,_] = needleman_wunsch(Q = Q_rand, R = R_rand,
                gap_penalty = gap_penalty, match_score = match_score, mismatch_score = mismatch_score)
        else:
            # Anchored Needleman-Wunsch
            [curr_score,_,_] = anchored_needleman_wunsch(Q = Q_rand, R = R_rand,
                matches = matches_, gap_penalty = gap_penalty, match_score = match_score, mismatch_score = mismatch_score)
        
        scores_random_sequences.append(curr_score)

    t2 = time.clock()
    print(t2 - t1)

    # print(scores_random_sequences)
    # print(len(scores_random_sequences))

    # Plotting
    
    n, bins, patches = plt.hist(x= scores_random_sequences, bins='auto', 
                                color='#0504aa', alpha=0.7, rwidth=0.85)
    
    plt.axvline(x = score, linewidth = 3, color = 'r')
    
    plt.title('Alignment Scores for 10000 Random Sequences')
    plt.xlabel('Alignment Score')
    plt.ylabel('Frequency')
    
    curr_plot_name = 'Plot_HOX.png'
    plt.savefig(curr_plot_name)