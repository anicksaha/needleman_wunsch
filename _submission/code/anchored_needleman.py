from standard_needleman import needleman_wunsch

def anchored_needleman_wunsch(Q, R, matches, gap_penalty, match_score, mismatch_score):

    global_score = 0 # Global Score
    Q_idx1 = 0 # starting index for Query
    R_idx1 = 0 # starting index for Reference
    query_with_gaps = ''
    ref_with_gaps = ''

    for match in matches:
        Q_idx2 = match[0] - 1
        R_idx2 = match[2] - 1
        
        # Unmatched group
        [local_score, local_query_with_gaps, local_ref_with_gaps] = needleman_wunsch(Q = Q[Q_idx1:Q_idx2], 
            R = R[R_idx1:R_idx2], gap_penalty = gap_penalty, match_score = match_score, mismatch_score = mismatch_score)
        
        query_with_gaps += local_query_with_gaps
        ref_with_gaps += local_ref_with_gaps
        global_score += local_score

        Q_idx1 = match[1]
        R_idx1 = match[3]
        query_with_gaps += Q[match[0]-1:match[1]]
        ref_with_gaps += R[match[2]-1:match[3]]
        global_score += len(Q[match[0]-1:match[1]]) # match[1] - match[0] + 1

    # Last unmatched group
    [local_score, local_query_with_gaps, local_ref_with_gaps] = needleman_wunsch(Q = Q[Q_idx1:len(Q)], 
        R = R[R_idx1:len(R)], gap_penalty = gap_penalty, match_score = match_score, mismatch_score = mismatch_score)
        
    query_with_gaps += local_query_with_gaps
    ref_with_gaps += local_ref_with_gaps
    global_score += local_score

    return [global_score, query_with_gaps, ref_with_gaps]