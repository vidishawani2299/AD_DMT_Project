import InputData as data
import MarkovClasses as model
import ParameterClasses as param
import Support as support

# simulating donepezil
# create a cohort
cohort_SOC = model.Cohort(id=0,
                           pop_size=data.POP_SIZE,
                           parameters=param.Parameters(therapy=param.Therapies.SOC))
# simulate the cohort
cohort_SOC.simulate(n_time_steps=data.SIM_TIME_STEPS)

# simulating dmt
# create a cohort
cohort_DMT30 = model.Cohort(id=1,
                            pop_size=data.POP_SIZE,
                            parameters=param.Parameters(therapy=param.Therapies.DMT_30))
# simulate the cohort
cohort_DMT30.simulate(n_time_steps=data.SIM_TIME_STEPS)

# print the estimates for the mean survival time and mean time to severe state
support.print_outcomes(sim_outcomes=cohort_SOC.cohortOutcomes,
                       therapy_name=param.Therapies.SOC)
support.print_outcomes(sim_outcomes=cohort_DMT30.cohortOutcomes,
                       therapy_name=param.Therapies.DMT_30)

# print comparative outcomes
support.print_comparative_outcomes(sim_outcomes_soc=cohort_SOC.cohortOutcomes,
                                   sim_outcomes_dmt=cohort_DMT30.cohortOutcomes)

# report the CEA results
support.report_CEA_CBA(sim_outcomes_soc=cohort_SOC.cohortOutcomes,
                       sim_outcomes_dmt=cohort_DMT30.cohortOutcomes)

# graphs
support.plot_survival_curves_and_histograms(sim_outcomes_soc=cohort_SOC.cohortOutcomes,
                                            sim_outcomes_dmt=cohort_DMT30.cohortOutcomes)


# create multicohort
multiCohort = model.MultiCohort(
    ids=range(data.N_COHORTS),   # [0, 1, 2 ..., N_COHORTS-1]
    pop_sizes=[data.POP_SIZE]*data.N_COHORTS,
    parameters=param.Parameters(therapy=param.Therapies.SOC)# [COHORT_POP_SIZE, COHORT_POP_SIZE, ..., COHORT_POP_SIZE]
)

multiCohort1 = model.MultiCohort(
    ids=range(data.N_COHORTS),   # [0, 1, 2 ..., N_COHORTS-1]
    pop_sizes=[data.POP_SIZE]*data.N_COHORTS,
    parameters=param.Parameters(therapy=param.Therapies.DMT_30)# [COHORT_POP_SIZE, COHORT_POP_SIZE, ..., COHORT_POP_SIZE]
)

# simulating multicohorts
multiCohort.simulate(n_time_steps=data.SIM_TIME_STEPS)
multiCohort1.simulate(n_time_steps=data.SIM_TIME_STEPS)

# multicohort
support.plot_survival_curves_and_histograms_multi(multi_cohort_outcomes_soc = multiCohort.multiCohortOutcomes,
                                                  multi_cohort_outcomes_dmt30 = multiCohort1.multiCohortOutcomes)