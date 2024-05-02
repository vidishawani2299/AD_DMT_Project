import InputData as data
import numpy as np
import deampy.random_variates as rvgs
import scipy.stats as stat
import math
from ParameterClasses import Therapies
from InputData import get_trans_prob_matrix_dmt_30


class Parameters:
    """ class to include parameter information to simulate the model """

    def __init__(self, therapy):

        self.therapy = therapy              # selected therapy
        self.initialHealthState = data.HealthStates.PREDEM     # initial health state
        self.annualTreatmentCost = 0        # annual treatment cost
        self.probMatrix = []                # transition probability matrix of the selected therapy
        self.semiAnnualStateCosts = []          # annual state costs
        self.stateUtilities = []      # annual state utilities
        self.discountRate = data.DISCOUNT   # discount rate

class ParameterGenerator:
    """ class to generate parameter values from the selected probability distributions """

    def __init__(self, therapy):
        self.probMatrixRVG = []  # list of dirichlet distributions for transition probabilities
        self.therapy = therapy
        self.semiannualStateCostRVGs = []  # list of gamma distributions for the annual cost of states
        self.StateDisutilityRVGs = []  # list of beta distributions for the annual utility of states
        self.probMatrixRVG = []  # list of dirichlet distributions for transition probabilities
        self.annualDMT30CostRVG = None  # gamma distribution for the cost of zidovudine
        self.annualSOCCostRVG = None  # gamma distribution for the cost of lamivudine

        # create Dirichlet distributions for transition probabilities
        for row in data.TRANS_MATRIX:
            # note:  for a Dirichlet distribution all values of the argument 'a' should be non-zero.
            # setting if_ignore_0s to True allows the Dirichlet distribution to take 'a' with zero values.
            self.probMatrixRVG.append(
                rvgs.Dirichlet(a=row, if_ignore_0s=True))

        # create gamma distributions for annual state cost
        for cost in data.SEMI_ANNUAL_STATE_COST:  # use gamma dist as cost is not < 0

            # if cost is zero, add a constant 0, otherwise add a gamma distribution
            if cost == 0:
                self.semiannualStateCostRVGs.append(rvgs.Constant(value=0))
            else:
                # find shape and scale of the assumed gamma distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 5 at 20%
                fit_output = rvgs.Gamma.fit_mm(mean=cost, st_dev=cost / 5)
                # append the distribution
                self.semiannualStateCostRVGs.append(
                    rvgs.Gamma(shape=fit_output["shape"], loc=0, scale=fit_output["scale"]))
        fit_output_dmt30 = rvgs.Gamma.fit_mm(mean=data.DMT30_COST, st_dev=data.DMT30_COST / 5)
        fit_output_soc = rvgs.Gamma.fit_mm(mean=data.SOC_COST, st_dev=data.SOC_COST / 5)

        # then create the gamma distribution for the cost of each drug
        self.annualDMT30CostRVG = rvgs.Gamma(shape=fit_output_dmt30["shape"], loc=0, scale=fit_output_dmt30["scale"])
        self.annualSOCCostRVG = rvgs.Gamma(shape=fit_output_soc["shape"], loc=0, scale=fit_output_soc["scale"])

        # create beta distributions for annual state utility
        for utility in data.STATE_DISUTILITY:
            # if utility is zero, add a constant 0, otherwise add a beta distribution
            if utility == 0:
                self.StateDisutilityRVGs.append(rvgs.Constant(value=0))
            else:
                # find alpha and beta of the assumed beta distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 4
                fit_output = rvgs.Beta.fit_mm(mean=utility, st_dev=utility / 4)
                # append the distribution
                self.StateDisutilityRVGs.append(
                     rvgs.Beta(a=fit_output["a"], b=fit_output["b"]))

    def get_new_parameters(self, seed):
        """
        :param seed: seed for the random number generator used to a sample of parameter values
        :return: a new parameter set
        """

        rng = np.random.RandomState(seed=seed)

        # create a parameter set
        param = Parameters(therapy=self.therapy)
        # calculate transition probabilities
        prob_matrix = []  # probability matrix without background mortality added
        # for all health states
        for s in data.HealthStates:
            # if this state is not death
            if s != data.HealthStates.ADJ_DEATH:
                # sample from the dirichlet distribution to find the transition probabilities between hiv states
                # fill in the transition probabilities out of this state
                # gives sample from dritchlet distribution
                prob_matrix.append(self.probMatrixRVG[s.value].sample(rng))
        # calculate transition probabilities between hiv states
        if self.therapy == Therapies.SOC:
            # calculate transition probability matrix for the mono therapy
            param.probMatrix = data.get_trans_prob_matrix(trans_matrix=prob_matrix) # check if simply need to equate it as prob_matrix

        elif self.therapy == Therapies.DMT_30:
            # calculate transition probability matrix for the combination therapy
            param.probMatrix = get_trans_prob_matrix_dmt_30(
                trans_prob_matrix_soc=data.get_trans_prob_matrix(trans_matrix=prob_matrix),
                relative_risk_dmt=data.RR_DMT)

        # sample from gamma distributions that are assumed for annual state costs
        for dist in self.semiannualStateCostRVGs:
            param.semiAnnualStateCosts.append(dist.sample(rng))

        # sample from beta distributions that are assumed for annual state utilities
        for dist in self.StateDisutilityRVGs:
            param.stateUtilities.append(dist.sample(rng))

        # return the parameter set
        return param