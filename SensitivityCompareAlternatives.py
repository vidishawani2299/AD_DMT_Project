import InputData as data
import MarkovClassesSensitivity as model
import SensitivityParamClasses as param
import SensitivitySupport as support

N_COHORTS = 100  # number of cohorts
POP_SIZE = 500  # population size of each cohort

# create a multi-cohort to simulate under SOC treatment
multiCohortSOC = model.MultiCohort(
    ids=range(N_COHORTS),
    pop_sizes=POP_SIZE,
    parameters=param.Therapies.SOC)

multiCohortSOC.simulate(n_time_steps=data.SIM_TIME_STEPS)

# create a multi-cohort to simulate under DMT treatment
multiCohortDMT30 = model.MultiCohort(
    ids=range(N_COHORTS),
    pop_sizes=POP_SIZE,
    parameters=param.Therapies.DMT_30)

multiCohortDMT30.simulate(n_time_steps=data.SIM_TIME_STEPS)

# print the estimates for the mean survival time and mean time to severe stage
support.print_outcomes(multi_cohort_outcomes=multiCohortSOC.multiCohortOutcomes,
                       therapy_name=param.Therapies.SOC)
support.print_outcomes(multi_cohort_outcomes=multiCohortDMT30.multiCohortOutcomes,
                       therapy_name=param.Therapies.DMT_30)

# draw survival curves and histograms
support.plot_survival_curves_and_histograms(multi_cohort_outcomes_soc=multiCohortSOC.multiCohortOutcomes,
                                            multi_cohort_outcomes_dmt30=multiCohortDMT30.multiCohortOutcomes)

# print comparative outcomes
support.print_comparative_outcomes(multi_cohort_outcomes_soc=multiCohortSOC.multiCohortOutcomes,
                                   multi_cohort_outcomes_dmt30=multiCohortDMT30.multiCohortOutcomes)

# report the CEA results
support.report_CEA_CBA(multi_cohort_outcomes_soc=multiCohortSOC.multiCohortOutcomes,
                       multi_cohort_outcomes_dmt30=multiCohortDMT30.multiCohortOutcomes)