from enum import Enum
import InputData as data

class Therapies(Enum):
    """ mono vs. combination therapy """
    SOC = 0
    DMT_30 = 1

class Parameters:
    def __init__(self, therapy):

        # selected therapy
        self.therapy = therapy

        # initial health state
        self.initialHealthState = data.HealthStates.PREDEM

        # annual treatment cost
        if self.therapy == Therapies.DMT_30:
            self.annualTreatmentCost = data.DMT30_COST
        else:
             self.annualTreatmentCost = data.SOC_COST # find SOC cost

        # transition probability matrix of the selected therapy
        self.probMatrix = []

        # calculate transition probabilities between hiv states
        if self.therapy == Therapies.SOC:
            # calculate transition probability matrix for the mono therapy
            self.probMatrix = data.get_trans_prob_matrix(trans_matrix=data.TRANS_MATRIX)

        elif self.therapy == Therapies.DMT_30:
            # calculate transition probability matrix for the combination therapy
            self.probMatrix = data.get_trans_prob_matrix_dmt_30(
                trans_prob_matrix_soc=data.get_trans_prob_matrix(trans_matrix=data.TRANS_MATRIX),
                relative_risk_dmt=data.RR_DMT)

        # annual state costs and utilities
        self.semiAnnualStateCosts = data.SEMI_ANNUAL_STATE_COST  # IF ELSE IF SOMEONE IS IN POST-STROKE STATE OR NOT,COST ARRAY STAYS THE SAME
        self.stateUtilities = data.STATE_DISUTILITY

        # # discount rate
        self.discountRate = data.DISCOUNT
    
if __name__ == '__main__':
    matrix_soc = data.get_trans_prob_matrix(data.TRANS_MATRIX)
    matrix_antic = data.get_trans_prob_matrix_dmt_30(matrix_soc, data.RR_DMT)
