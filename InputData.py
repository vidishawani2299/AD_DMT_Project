from enum import Enum
import numpy as np
N_COHORTS = 10
POP_SIZE = 10000         # cohort population size
SIM_TIME_STEPS = 20    # length of simulation (half years)
# check cycle length
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate
RR_DMT = 0.30

ANNUAL_STATE_COST = []
ANNUAL_STATE_UTILITY = []

class HealthStates(Enum):
    """ health states of patients with HIV """
    PREDEM = 0
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    ADJ_DEATH = 4

TRANS_MATRIX = [
    [70,  28,    0,   0,   2],   # CD4_200to500
    [0,     61,    15,    0,    3],   # CD4_200
    [0,     0,      62,    23,   8],
    [0,     0,      0,    1,   21],
    [0,     0,      0,    0,   1]# AIDS
    ]




def get_trans_prob_matrix(trans_matrix):
    """
    :param trans_matrix: transition matrix containing counts of transitions between states
    :return: transition probability matrix
    """

    # initialize transition probability matrix
    trans_prob_matrix = []

    # for each row in the transition matrix
    for row in trans_matrix:
        # calculate the transition probabilities
        prob_row = np.array(row)/sum(row)
        # add this row of transition probabilities to the transition probability matrix
        trans_prob_matrix.append(prob_row)

    return trans_prob_matrix
print(get_trans_prob_matrix(TRANS_MATRIX))


def get_trans_prob_matrix_dmt_30(trans_prob_matrix_soc, relative_risk_dmt):
    matrix_dmt = []
    for row in trans_prob_matrix_soc:
        matrix_dmt.append(np.zeros(len(row)))  # adding a row [0, 0, 0, 0]

    # populate the combo matrix
    # calculate the effect of combo-therapy on non-diagonal elements

    for s in range(len(matrix_dmt)):  # Iterate through all rows of matrix_dmt
        if s < 3:  # Check if the current row index is less than 3
            for next_s in range(s, len(trans_prob_matrix_soc[s])):
                # Apply the changes only to the first three rows
                matrix_dmt[s][next_s] = trans_prob_matrix_soc[s][next_s] - (
                            relative_risk_dmt * trans_prob_matrix_soc[s][next_s])
        else:
            # For rows 3 and beyond, copy them unchanged from trans_prob_matrix_soc
            matrix_dmt[s] = trans_prob_matrix_soc[s][:]

    # diagonal elements are calculated to make sure the sum of each row is 1
    # for s in range(len(matrix_dmt)):
    #     matrix_dmt[s][s] = 1 - sum(matrix_dmt[s][s+1:])

    return matrix_dmt


print(get_trans_prob_matrix_dmt_30(get_trans_prob_matrix(TRANS_MATRIX),0.30))