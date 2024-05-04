from enum import Enum
import numpy as np

N_COHORTS = 10         # number of cohorts
POP_SIZE = 10000       # cohort population size
SIM_TIME_STEPS = 20    # length of simulation (half years)
ALPHA = 0.05           # significance level for calculating confidence intervals
DISCOUNT = 0.03        # annual discount rate
RR_DMT = 0.30          # effectiveness of DMT

SEMI_ANNUAL_STATE_COST = [3875,      # PREDEM
                          3875,      # MILD
                          25000,     # MODERATE
                          25000,     # SEVERE
                          0]         # ADJ_DEATH

STATE_UTILITY = [0.83,      # PREDEM
                 0.78,      # MILD
                 0.69,      # MODERATE
                 0.27,      # SEVERE
                 0]         # ADJ_DEATH

DMT30_COST = 56000/2
SOC_COST = 2040/2

class HealthStates(Enum):
    """ health states of patients with AD"""
    PREDEM = 0
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    ADJ_DEATH = 4

TRANS_MATRIX = [
    [70,  28,    0,   0,   3],            # PREDEM
    [0,     62,    32,    2,    3],       # MILD
    [0,     0,      62,    24,   8],      # MODERATE
    [0,     0,      0,    100,   22],     # SEVERE
    [0,     0,      0,    0,   1]         # ADJ_DEATH
    ]

# transition probability matrix for standard of care
def get_trans_prob_matrix(trans_matrix):
    """
    :param trans_matrix: transition matrix containing counts of transitions between states
    :return: transition probability matrix
    """
    trans_prob_matrix = [] # initializing matrix
    for row in trans_matrix:
        prob_row = np.array(row)/sum(row) # for each row, contruct transition probabilities
        trans_prob_matrix.append(prob_row)

    return trans_prob_matrix

# printing transition probability matrix for standard of care
print(get_trans_prob_matrix(TRANS_MATRIX))

# transition probability matrix for DMT
def get_trans_prob_matrix_dmt_30(trans_prob_matrix_soc, relative_risk_dmt):
    """
    :param trans_prob_matrix_soc: transition probability matrix for standard of care
    :param relative_risk_dmt: effectiveness of DMT
    :return: transition probability matrix adjusted for DMT at predementia stage

    """
    matrix_dmt = [] # initialize matrix
    for row in trans_prob_matrix_soc:
        matrix_dmt.append(np.zeros(len(row)))  # for each row, construct transition probabilities

    for s in range(len(matrix_dmt)):  # Iterate through all rows of matrix_dmt
        if s < 3:  # Check if the current row index is less than 3
            for next_s in range(len(trans_prob_matrix_soc[s])):
                if next_s != s:  # Apply the changes only to non-diagonal elements
                    matrix_dmt[s][next_s] = trans_prob_matrix_soc[s][next_s] - (
                            relative_risk_dmt * trans_prob_matrix_soc[s][next_s])

        else:
            # make sure that first element is same as before
            # For rows 3 and beyond, copy them unchanged from trans_prob_matrix_soc
            matrix_dmt[s] = trans_prob_matrix_soc[s][:]

        # Now calculate probability for diagonal elements in the first three rows
    for s in range(3):  # Iterate through the first three rows of matrix_dmt
        for next_s in range(len(trans_prob_matrix_soc[s])):
            if next_s == s:  # Apply the calculation only to diagonal elements
                row_sum = np.sum(matrix_dmt[s][:next_s]) + np.sum(matrix_dmt[s][next_s + 1:])
                matrix_dmt[s][next_s] = 1 - row_sum

    return matrix_dmt

# printing transition probability matrix for DMT at predementia stage
print(get_trans_prob_matrix_dmt_30(get_trans_prob_matrix(TRANS_MATRIX),0.30))