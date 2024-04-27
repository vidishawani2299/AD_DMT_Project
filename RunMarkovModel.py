import deampy.plots.histogram as hist
import deampy.plots.sample_paths as path

import InputData as D
from MarkovClasses import Cohort, MultiCohort

# create a cohort
myCohort = Cohort(id=1,
                  pop_size=D.POP_SIZE,
                  transition_prob_matrix=D.get_trans_prob_matrix(D.TRANS_MATRIX))

# simulate the cohort over the specified time steps
myCohort.simulate(n_time_steps=D.SIM_TIME_STEPS)

# plot the sample path (survival curve)
path.plot_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve',
    x_label='Simulation Year',
    y_label='Number Alive',
    file_name='figs/survival_curve.png')

# plot the histogram of survival times
hist.plot_histogram(
    data=myCohort.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1,
    file_name='figs/histogram.png')

# print the patient survival time
print('Mean survival time (years):',
      myCohort.cohortOutcomes.meanSurvivalTime)
# print mean time to AIDS
print('Mean time until SEVERE State (years)',
      myCohort.cohortOutcomes.meanTimeToSEVERE)

# create multiple cohorts
multiCohort = MultiCohort(
    ids=range(D.N_COHORTS),   # [0, 1, 2 ..., N_COHORTS-1]
    pop_sizes=[D.POP_SIZE]*D.N_COHORTS,
    transition_prob_matrix=D.get_trans_prob_matrix(D.TRANS_MATRIX)# [COHORT_POP_SIZE, COHORT_POP_SIZE, ..., COHORT_POP_SIZE]
)

# simulate all cohorts
multiCohort.simulate(D.SIM_TIME_STEPS)

# print projected mean survival time (years)
print('Projected mean survival time (years)',
      multiCohort.multiCohortOutcomes.statMeanSurvivalTime.get_mean()) # check what to use for confidence interval

# print projection interval
print('95% projection (prediction, percentile, or uncertainty) interval of average survival time (years)',
      multiCohort.multiCohortOutcomes.statMeanSurvivalTime.get_PI(alpha=D.ALPHA))

print('Projected mean time to severe state (years)',
      multiCohort.multiCohortOutcomes.statMeanTimeToSEVERE.get_mean())

# print projection interval
print('95% projection (prediction, percentile, or uncertainty) interval of mean time to severe state (years)',
      multiCohort.multiCohortOutcomes.statMeanTimeToSEVERE.get_PI(alpha=D.ALPHA))