import numpy as np
from deampy.markov import MarkovJumpProcess
from deampy.plots.sample_paths import PrevalencePathBatchUpdate
import deampy.statistics as stats
import deampy.econ_eval as econ

from InputData import HealthStates



class Patient:
    def __init__(self, id, parameters):
        """ initiates a patient
        :param id: ID of the patient
        """
        self.id = id
        self.params = parameters
        self.stateMonitor = PatientStateMonitor(parameters=parameters)

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        # random number generator
        rng = np.random.RandomState(seed=self.id)
        # Markov jump process
        markov_jump = MarkovJumpProcess(transition_prob_matrix=self.params.probMatrix)

        k = 0  # simulation time step

        # while the patient is alive and simulation length is not yet reached
        while self.stateMonitor.get_if_alive() and k < n_time_steps:

            # sample from the Markov jump process to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = markov_jump.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # update health state
            self.stateMonitor.update(time_step=k, new_state=HealthStates(new_state_index))

            # increment time
            k += 1


class PatientStateMonitor:
    """ To update patient outcomes (years survived, cost, etc.) throughout the simulation. """

    def __init__(self, parameters):
        self.currentState = parameters.initialHealthState
        self.survivalTime = None
        self.timeToSEVERE = None
        self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time_step, new_state):
        if new_state == HealthStates.ADJ_DEATH:
            self.survivalTime = time_step + 0.5  # Correct for half-cycle effect.
        if self.timeToSEVERE is None and new_state == HealthStates.SEVERE:
            self.timeToSEVERE = time_step + 0.5

        self.costUtilityMonitor.update(k=time_step, current_state=self.currentState, next_state=new_state)
        self.currentState = new_state

    def get_if_alive(self):
        return self.currentState != HealthStates.ADJ_DEATH


class PatientCostUtilityMonitor:
    def __init__(self, parameters):
        self.params = parameters
        self.totalDiscountedCost = 0
        self.totalDiscountedUtility = 0

    def update(self, k, current_state, next_state):
        # Update cost, calculating half-cycle for transitions
        cost = 0.5 * (self.params.semiAnnualStateCosts[current_state.value] +
                      self.params.semiAnnualStateCosts[next_state.value])

        # Calculate utility if the state is associated with a utility
        utility = 0
        if current_state != HealthStates.ADJ_DEATH and next_state != HealthStates.ADJ_DEATH:
            utility = 0.5 * (self.params.stateUtilities[current_state.value] +
                             self.params.stateUtilities[next_state.value])

        # Treatment cost adjustments based on state
        if next_state == HealthStates.SEVERE:
            cost += 0.5 * self.params.annualTreatmentCost # Only half cycle treatment cost if next state is SEVERE
        else:
            cost += self.params.annualTreatmentCost

        # Apply discounting
        discounted_cost = econ.pv_single_payment(payment=cost, discount_rate=self.params.discountRate / 2,
                                                 discount_period=k + 1)
        discounted_utility = econ.pv_single_payment(payment=utility, discount_rate=self.params.discountRate / 2,
                                                    discount_period=k + 1)

        # Update total discounted cost and utility
        self.totalDiscountedCost += discounted_cost
        self.totalDiscountedUtility += discounted_utility


# class PatientStateMonitor:
#     """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
#     def __init__(self, parameters):
#
#         self.currentState = parameters.initialHealthState    # current health state
#         self.survivalTime = None      # survival time
#         self.timeToSEVERE = None        # time to reach severe state
#         self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)
#
#     def update(self, time_step, new_state):
#         """
#         update the current health state to the new health state
#         :param time_step: current time step
#         :param new_state: new state
#         """
#
#         # update survival time
#         if new_state == HealthStates.ADJ_DEATH:
#             self.survivalTime = time_step + 0.5  # corrected for the half-cycle effect
#
#         # update time until AIDS (only if the patient has never developed AIDS before)
#         if self.timeToSEVERE is None and new_state == HealthStates.SEVERE:
#             self.timeToSEVERE = time_step + 0.5  # corrected for the half-cycle effect
#
#         # update cost and utility
#         self.costUtilityMonitor.update(k=time_step,
#                                        current_state=self.currentState,
#                                        next_state=new_state) # add information for this from costUtilityMonitor
#
#         # update current health state
#         self.currentState = new_state
#
#     def get_if_alive(self):
#         """ returns true if the patient is still alive """
#         if self.currentState != HealthStates.ADJ_DEATH:
#             return True
#         else:
#             return False
#
#
# class PatientCostUtilityMonitor:
#     def __init__(self, parameters):
#
#         # model parameters for this patient
#         self.params = parameters
#
#         # total cost and utility
#         self.totalDiscountedCost = 0
#         self.totalDiscountedUtility = 0
#
#     def update(self, k, current_state, next_state):
#         """ updates the discounted total cost and health utility
#         :param k: simulation time step
#         :param current_state: current health state
#         :param next_state: next health state
#         """
#
#         # update cost
#         cost = 0.5 * (self.params.semiAnnualStateCosts[current_state.value] +
#                       self.params.semiAnnualStateCosts[next_state.value])
#         # update utility
#         utility = 0.5 * (self.params.stateUtilities[current_state.value] +
#                          self.params.stateUtilities[next_state.value])
#
#         # add the cost of treatment
#         # if HIV death will occur, add the cost for half-year of treatment
#         if next_state == HealthStates.SEVERE:
#             cost += 0.5 * self.params.annualTreatmentCost
#         else:
#             cost += 1 * self.params.annualTreatmentCost
#
#         # update total discounted cost and utility (corrected for the half-cycle effect)
#         self.totalDiscountedCost += econ.pv_single_payment(payment=cost,
#                                                            discount_rate=self.params.discountRate / 2,
#                                                            discount_period= k + 1)
#         self.totalDiscountedUtility += econ.pv_single_payment(payment=utility,
#                                                               discount_rate=self.params.discountRate / 2,
#                                                               discount_period= k + 1)
#
#         print("Attempting to access index:", next_state.value)
#         print("State Utilities Length:", len(self.params.stateUtilities))



class Cohort:
    def __init__(self, id, pop_size, parameters):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        """
        self.id = id
        self.popSize = pop_size
        self.params = parameters
        self.cohortOutcomes = CohortOutcomes()  # outcomes of this simulated cohort

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        """
        # populate and simulate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              parameters=self.params)
            # simulate
            patient.simulate(n_time_steps)

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        # calculate cohort outcomes
        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []         # patients' survival times
        self.timeToSEVERE = []          # patients' times to AIDS
        self.nLivingPatients = None     # survival curve (sample path of number of alive patients over time)
        self.costs = []                 # patients' discounted costs
        self.utilities = []             # patients' discounted utilities
        self.statSurvivalTimes = None   # summary statistics for survival time
        self.statTimeToSEVERE = None    # summary statistics for discounted cost
        self.statCost = None            # summary statistics for discounted cost
        self.statUtilities = None       # summary statistics for discounted utility

    def extract_outcome(self, simulated_patient):
        """ extracts outcomes of a simulated patient
        :param simulated_patient: a simulated patient"""

        # record survival time and time until AIDS
        if simulated_patient.stateMonitor.survivalTime is not None:
            self.survivalTimes.append(simulated_patient.stateMonitor.survivalTime)
        if simulated_patient.stateMonitor.timeToSEVERE is not None:
            self.timeToSEVERE.append(simulated_patient.stateMonitor.timeToSEVERE)

        # discounted cost and utilities
        self.costs.append(simulated_patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)
        self.utilities.append(simulated_patient.stateMonitor.costUtilityMonitor.totalDiscountedUtility)

    def calculate_cohort_outcomes(self, initial_pop_size):
        """ calculates the cohort outcomes
        :param initial_pop_size: initial population size
        """

        # summary statistics
        self.statSurvivalTimes = stats.SummaryStat(name="Survival Time", data=self.survivalTimes)
        self.statTimeToSEVERE = stats.SummaryStat(name="Time To Severe State", data=self.timeToSEVERE)
        self.statCost = stats.SummaryStat(name="Discounted Cost", data=self.costs)
        self.statUtilities = stats.SummaryStat(name="Discounted Utilities", data=self.utilities)


        # survival curve
        self.nLivingPatients = PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=initial_pop_size,
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )

    def print_costs(self):
        print("Costs for each patient in this cohort:")
        for i, cost in enumerate(self.costs):
            print(f"Patient {i + 1}: ${cost:.2f}")

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

    def simulate(self, n_time_steps):
        """ simulates all cohorts """

        for i in range(len(self.ids)):

            # create a cohort
            cohort = Cohort(id=self.ids[i], pop_size=self.popSizes[i],
                            parameters=self.params)

            # simulate the cohort
            cohort.simulate(n_time_steps=n_time_steps)

            # outcomes from simulating all cohorts
            self.multiCohortOutcomes.extract_outcomes(simulated_cohort=cohort)

        # calculate the summary statistics of from all cohorts
        self.multiCohortOutcomes.calculate_summary_stats()


class MultiCohortOutcomes:
    def __init__(self, parameters):

        self.survivalTimes = []  # two-dimensional list of patient survival times from all simulated cohort
        self.meanSurvivalTimes = []  # list of average patient survival time for all simulated cohort
        self.survivalCurves = []  # list of survival curves from all simulated cohorts
        self.statMeanSurvivalTime = None  # summary statistics of mean survival time
        self.timeToSEVERE = []
        self.meanTimeToSEVERE = []
        self.statMeanTimeToSEVERE = None
        self.params = parameters
    def extract_outcomes(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort
        :param simulated_cohort: a cohort after being simulated"""

        # store all patient survival times from this cohort
        self.survivalTimes.append(simulated_cohort.cohortOutcomes.survivalTimes)

        # append the survival curve of this cohort
        self.survivalCurves.append(simulated_cohort.cohortOutcomes.nLivingPatients)

        # store time to SEVERE state from cohort
        self.timeToSEVERE.append(simulated_cohort.cohortOutcomes.timeToSEVERE)

    def calculate_summary_stats(self):
        """
        calculate the summary statistics
        """

        # calculate average patient survival time for all simulated cohorts
        for obs_set in self.survivalTimes:
            self.meanSurvivalTimes.append(sum(obs_set)/len(obs_set))

        for obs_set in self.timeToSEVERE:
            self.meanTimeToSEVERE.append(sum(obs_set)/len(obs_set))

        # summary statistics of mean survival time
        self.statMeanSurvivalTime = stats.SummaryStat(name='Mean survival time',
                                                      data=self.meanSurvivalTimes)
        self.statMeanTimeToSEVERE = stats.SummaryStat(name='Time to SEVERE',
                                                      data=self.meanTimeToSEVERE)

    def get_cohort_CI_mean_survival(self, cohort_index, alpha):
        """
        Returns the confidence intervals for both mean survival time and time to SEVERE state for a specified cohort.
        :param cohort_index: index of the cohort [0, 1, ...]
        :param alpha: significance level for the confidence interval
        :return: a dictionary containing both confidence intervals
        """

        # Calculate CI for mean survival time of the cohort
        stat_survival = stats.SummaryStat(name='Summary statistics',
                                          data=self.survivalTimes[cohort_index])
        survival_ci = stat_survival.get_t_CI(alpha=alpha)

        # Calculate CI for time to SEVERE state of the cohort
        stat_time_severe = stats.SummaryStat(name='Time to SEVERE state',
                                             data=self.timeToSEVERE[cohort_index])
        severe_ci = stat_time_severe.get_t_CI(alpha=alpha)

        # Return a dictionary containing both confidence intervals
        return {
            'survival_ci': survival_ci,
            'severe_ci': severe_ci
        }

    def get_cohort_PI_survival(self, cohort_index, alpha):
        """
        Returns the prediction intervals for both survival time and time to SEVERE state for a specified cohort.
        :param cohort_index: index of the cohort [0, 1, ...] corresponding to the 1st, 2nd, ... simulated cohort
        :param alpha: significance level for the prediction interval
        :return: a dictionary containing both prediction intervals
        """

        # Calculate PI for survival time of the cohort
        stat_survival = stats.SummaryStat(name='Summary statistics',
                                          data=self.survivalTimes[cohort_index])
        survival_pi = stat_survival.get_PI(alpha=alpha)

        # Calculate PI for time to SEVERE state of the cohort
        stat_time_severe = stats.SummaryStat(name='Time to SEVERE state',
                                             data=self.timeToSEVERE[cohort_index])
        severe_pi = stat_time_severe.get_PI(alpha=alpha)

        # Return a dictionary containing both prediction intervals
        return {
            'survival_pi': survival_pi,
            'severe_pi': severe_pi
        }