import deampy.plots.histogram as hist
import deampy.plots.sample_paths as path

import InputData as data
import MarkovClassesSensitivity as model
import SensitivityParamClasses as param
import SensitivitySupport as support

POP_SIZE = 500             # cohort population size
N_COHORTS = 100              # number of cohorts
therapy = param.Therapies.SOC  # selected therapy

# create multiple cohort
multiCohort = model.MultiCohort(
    ids=range(N_COHORTS),
    pop_sizes=POP_SIZE,
    parameters=therapy)

multiCohort.simulate(n_time_steps=data.SIM_TIME_STEPS)

# print the outcomes of this simulated cohort
support.print_outcomes(multi_cohort_outcomes=multiCohort.multiCohortOutcomes,
                       therapy_name=therapy)