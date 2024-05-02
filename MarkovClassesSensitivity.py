import deampy.statistics as stat
from MarkovClasses import Cohort
from SensitivityParamClasses import ParameterGenerator


class MultiCohort:
    """ simulates multiple cohorts with different parameters """

    def __init__(self, ids, pop_sizes, parameters):
        """
        :param ids: (list) of ids for cohorts to simulate
        :param pop_sizes: (list) of population sizes of cohorts to simulate

        """
        self.ids = ids
        self.popSizes = pop_sizes
        self.params = parameters
        self.multiCohortOutcomes = MultiCohortOutcomes(parameters=parameters)
        self.paramSets = []  # list of parameter sets each of which corresponds to a cohort
        self.paramGenerator = ParameterGenerator(therapy=self.params)

    def simulate(self, n_time_steps):
        """ simulates all cohorts """
        for i in range(len(self.ids)):
            # for each cohort, sample a new distribution
            # get a new set of parameter values
            param_set = self.paramGenerator.get_new_parameters(seed=i)
            # create a cohort
            cohort = Cohort(id=self.ids[i],
                            pop_size=self.popSizes,
                            parameters=param_set)
            # simulate the cohort
            cohort.simulate(n_time_steps=n_time_steps)

            # outcomes from simulating all cohorts
            self.multiCohortOutcomes.extract_outcomes(simulated_cohort=cohort)

        # calculate the summary statistics of from all cohorts
        self.multiCohortOutcomes.calculate_summary_stats()


class MultiCohortOutcomes:
    def __init__(self,parameters):

        self.survivalCurves = []  # list of survival curves from all simulated cohorts

        self.meanSurvivalTimes = []  # list of average patient survival time from each simulated cohort
        self.meanTimeToAIDS = []     # list of average patient time until AIDS from each simulated cohort
        self.meanCosts = []          # list of average patient cost from each simulated cohort
        self.meanQALYs = []          # list of average patient QALY from each simulated cohort

        self.statMeanSurvivalTime = None    # summary statistics of average survival time
        self.statMeanTimeToAIDS = None      # summary statistics of average time until AIDS
        self.statMeanCost = None            # summary statistics of average cost
        self.statMeanQALY = None            # summary statistics of average QALY

    def extract_outcomes(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort
        :param simulated_cohort: a cohort after being simulated"""

        # append the survival curve of this cohort
        self.survivalCurves.append(simulated_cohort.cohortOutcomes.nLivingPatients)

        # store mean survival time from this cohort
        self.meanSurvivalTimes.append(simulated_cohort.cohortOutcomes.statSurvivalTimes.get_mean())
        # store mean time to AIDS from this cohort
        self.meanTimeToAIDS.append(simulated_cohort.cohortOutcomes.statTimeToSEVERE.get_mean())
        # store mean cost from this cohort
        self.meanCosts.append(simulated_cohort.cohortOutcomes.statCost.get_mean())
        # store mean QALY from this cohort
        self.meanQALYs.append(simulated_cohort.cohortOutcomes.statUtilities.get_mean())

    def calculate_summary_stats(self):
        """
        calculate the summary statistics
        """

        # summary statistics of mean survival time
        self.statMeanSurvivalTime = stat.SummaryStat(name='Average survival time',
                                                     data=self.meanSurvivalTimes)
        # summary statistics of mean time to AIDS
        self.statMeanTimeToAIDS = stat.SummaryStat(name='Average time to AIDS',
                                                   data=self.meanTimeToAIDS)
        # summary statistics of mean cost
        self.statMeanCost = stat.SummaryStat(name='Average cost',
                                             data=self.meanCosts)
        # summary statistics of mean QALY
        self.statMeanQALY = stat.SummaryStat(name='Average QALY',
                                             data=self.meanQALYs)