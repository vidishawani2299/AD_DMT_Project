import deampy.plots.histogram as hist
import deampy.plots.sample_paths as path

import InputData as data
import MarkovClassesSensitivity as model
import SensitivityParamClasses as param
import SensitivitySupport as support

POP_SIZE = 500             # cohort population size
N_COHORTS = 100              # number of cohorts
therapy = param.Therapies.DMT_30  # selected therapy - DMT treatment

# create multiple cohort
multiCohort = model.MultiCohort(
    ids=range(N_COHORTS),
    pop_sizes=POP_SIZE,
    parameters=therapy)

multiCohort.simulate(n_time_steps=data.SIM_TIME_STEPS)

# print the outcomes of this simulated cohort
support.print_outcomes(multi_cohort_outcomes=multiCohort.multiCohortOutcomes,
                       therapy_name=therapy)
# plot the sample paths when prescribed DMT
path.plot_sample_paths(
    sample_paths=multiCohort.multiCohortOutcomes.survivalCurves,
    title='Survival Curves',
    x_label='Time-Step (Year)',
    y_label='Number Survived',
    transparency=0.5)

# plot the histogram of mean survival time when prescribed DMT
hist.plot_histogram(
    data=multiCohort.multiCohortOutcomes.meanSurvivalTimes,
    title='Histograms of Mean Survival Time',
    x_label='Survival Time (year)',
    bin_width=0.5,
    x_range=[5, 20])