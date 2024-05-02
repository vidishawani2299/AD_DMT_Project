import deampy.econ_eval as econ
import deampy.plots.histogram as hist
import deampy.plots.sample_paths as path
import deampy.statistics as stat

import InputData as data


def print_outcomes(multi_cohort_outcomes, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param multi_cohort_outcomes: outcomes of a simulated multi-cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and prediction interval of patient survival time
    survival_mean_PI_text = multi_cohort_outcomes.statMeanSurvivalTime.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2)

    # mean and prediction interval text of time to AIDS
    time_to_HIV_death_PI_text = multi_cohort_outcomes.statMeanTimeToAIDS.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2)

    # mean and prediction interval text of discounted total cost
    cost_mean_PI_text = multi_cohort_outcomes.statMeanCost.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2, form=',')

    # mean and prediction interval text of discounted total QALY
    utility_mean_PI_text = multi_cohort_outcomes.statMeanQALY.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} uncertainty interval:".format(1 - data.ALPHA, prec=0),
          survival_mean_PI_text)
    print("  Estimate of mean time to AIDS and {:.{prec}%} uncertainty interval:".format(1 - data.ALPHA, prec=0),
          time_to_HIV_death_PI_text)
    print("  Estimate of mean discounted cost and {:.{prec}%} uncertainty interval:".format(1 - data.ALPHA, prec=0),
          cost_mean_PI_text)
    print("  Estimate of mean discounted utility and {:.{prec}%} uncertainty interval:".format(1 - data.ALPHA, prec=0),
          utility_mean_PI_text)
    print("")