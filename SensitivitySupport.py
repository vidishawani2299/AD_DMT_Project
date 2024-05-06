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

    # mean and prediction interval text of time to severe stage
    time_to_severe_PI_text = multi_cohort_outcomes.statMeanTimeToSEVERE.get_formatted_mean_and_interval(
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
    print("  Estimate of mean time to severe stage and {:.{prec}%} uncertainty interval:".format(1 - data.ALPHA, prec=0),
          time_to_severe_PI_text)
    print("  Estimate of mean discounted cost and {:.{prec}%} uncertainty interval:".format(1 - data.ALPHA, prec=0),
          cost_mean_PI_text)
    print("  Estimate of mean discounted utility and {:.{prec}%} uncertainty interval:".format(1 - data.ALPHA, prec=0),
          utility_mean_PI_text)
    print("")


def plot_survival_curves_and_histograms(multi_cohort_outcomes_soc, multi_cohort_outcomes_dmt30):
    """ plot the survival curves and the histograms of survival times
    :param multi_cohort_outcomes_soc: outcomes of a multi-cohort simulated under SOC Donepezil treatment
    :param multi_cohort_outcomes_dmt30: outcomes of a multi-cohort simulated under DMT treatment
    """

    # get survival curves of both treatments
    sets_of_survival_curves = [
        multi_cohort_outcomes_soc.survivalCurves,
        multi_cohort_outcomes_dmt30.survivalCurves
    ]

    # graph survival curve
    path.plot_sets_of_sample_paths(
        sets_of_sample_paths=sets_of_survival_curves,
        title='Survival Curves',
        x_label='Simulation Time Step (year)',
        y_label='Number of Patients Alive',
        legends=['Donepezil Treatment', 'Disease-modifying Treatment at 30% effectiveness'],
        transparency=0.4,
        color_codes=['cornflowerblue', 'midnightblue'],
        figure_size=(6, 5),
        file_name='figs/survival_curves_sensitivity.png'
    )
    # histograms of survival times
    set_of_time_to_severe = [
        multi_cohort_outcomes_soc.meanTimeToSEVERE,
        multi_cohort_outcomes_dmt30.meanTimeToSEVERE
    ]
    # graph histograms
    hist.plot_histograms(
        data_sets=set_of_time_to_severe,
        title='Histograms of mean time until SEVERE',
        x_label='Time to Severe (year)',
        y_label='Counts',
        bin_width=0.5,
        x_range=[5, 20],
        legends=['Donepezil Treatment', 'Disease-modifying Treatment at 30% effectiveness'],
        color_codes=['cornflowerblue', 'midnightblue'],
        transparency=0.5,
        figure_size=(6, 5),
        file_name='figs/time_to_severe_sensitivity.png'
    )
    # histograms of survival times
    set_of_survival_times = [
        multi_cohort_outcomes_soc.meanSurvivalTimes,
        multi_cohort_outcomes_dmt30.meanSurvivalTimes
    ]

    # graph histograms
    hist.plot_histograms(
        data_sets=set_of_survival_times,
        title='Histograms of Mean Survival Time',
        x_label='Survival Time (year)',
        y_label='Counts',
        bin_width=0.5,
        x_range=[5, 20],
        legends=['Donepezil Treatment', 'Disease-modifying Treatment at 30% effectiveness'],
        color_codes=['cornflowerblue', 'midnightblue'],
        transparency=0.5,
        figure_size=(6, 5),
        file_name='figs/survival_times_sensitivity.png'
    )

def print_comparative_outcomes(multi_cohort_outcomes_soc, multi_cohort_outcomes_dmt30):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param multi_cohort_outcomes_soc: outcomes of a multi-cohort simulated under SOC Donepezil treatment
    :param multi_cohort_outcomes_dmt30: outcomes of a multi-cohort simulated under DMT treatment
    """

    # increase in mean survival time under DMT treatment with respect to Donepezil
    increase_mean_survival_time = stat.DifferenceStatPaired(
        name='Increase in mean survival time',
        x=multi_cohort_outcomes_dmt30.meanSurvivalTimes,
        y_ref=multi_cohort_outcomes_soc.meanSurvivalTimes)

    # estimate and PI
    estimate_PI = increase_mean_survival_time.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2)
    print("Increase in mean survival time and {:.{prec}%} uncertainty interval:"
          .format(1 - data.ALPHA, prec=0), estimate_PI)

    # increase in mean time to severe stage under DMT treatment with respect to Donepezil
    increase_mean_time_to_SEVERE = stat.DifferenceStatPaired(
        name='Increase in mean time to severe stage',
        x=multi_cohort_outcomes_dmt30.meanTimeToSEVERE,
        y_ref=multi_cohort_outcomes_soc.meanTimeToSEVERE)

    # estimate and PI
    estimate_PI = increase_mean_time_to_SEVERE.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2)
    print("Increase in mean time to severe stage and {:.{prec}%} uncertainty interval:"
          .format(1 - data.ALPHA, prec=0), estimate_PI)

    # increase in mean discounted cost under DMT treatment with respect to Donepezil
    increase_mean_discounted_cost = stat.DifferenceStatPaired(
        name='Increase in mean discounted cost',
        x=multi_cohort_outcomes_dmt30.meanCosts,
        y_ref=multi_cohort_outcomes_soc.meanCosts)

    # estimate and PI
    estimate_PI = increase_mean_discounted_cost.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2, form=',')
    print("Increase in mean discounted cost and {:.{prec}%} uncertainty interval:"
          .format(1 - data.ALPHA, prec=0), estimate_PI)

    # increase in mean discounted QALY under DMT treatment with respect to Donepezil
    increase_mean_discounted_qaly = stat.DifferenceStatPaired(
        name='Increase in mean discounted QALY',
        x=multi_cohort_outcomes_dmt30.meanQALYs,
        y_ref=multi_cohort_outcomes_soc.meanQALYs)

    # estimate and PI
    estimate_PI = increase_mean_discounted_qaly.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} uncertainty interval:"
          .format(1 - data.ALPHA, prec=0), estimate_PI)


def report_CEA_CBA(multi_cohort_outcomes_soc, multi_cohort_outcomes_dmt30):
    """ performs cost-effectiveness and cost-benefit analyses
    :param multi_cohort_outcomes_soc: outcomes of a multi-cohort simulated under SOC Donepezil treatment
    :param multi_cohort_outcomes_dmt30: outcomes of a multi-cohort simulated under DMT treatment
    """

    # define two strategies
    soc_therapy_strategy = econ.Strategy(
        name='Donepezil',
        cost_obs=multi_cohort_outcomes_soc.meanCosts,
        effect_obs=multi_cohort_outcomes_soc.meanQALYs,
        color='cornflowerblue'
    )
    dmt30_therapy_strategy = econ.Strategy(
        name='Disease Modifying Treatment at 30% effectiveness',
        cost_obs=multi_cohort_outcomes_dmt30.meanCosts,
        effect_obs=multi_cohort_outcomes_dmt30.meanQALYs,
        color='midnightblue'
    )

    # do CEA
    CEA = econ.CEA(
        strategies=[soc_therapy_strategy, dmt30_therapy_strategy],
        if_paired=True
    )

    # show the cost-effectiveness plane
    CEA.plot_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional Discounted QALY',
        y_label='Additional Discounted Cost',
        fig_size=(6, 5),
        add_clouds=True,
        transparency=0.2,
        file_name='figs/cea_sensitivity.png')

    # report the CE table
    CEA.build_CE_table(
        interval_type='p',  # uncertainty (projection) interval for cost and effect estimates but
                            # for ICER, confidence interval will be reported.
        alpha=data.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='CETable_sensitivity.csv')

    # CBA
    NBA = econ.CBA(
        strategies=[soc_therapy_strategy, dmt30_therapy_strategy],
        wtp_range=(0, 150000),
        if_paired=True
    )
    # show the net monetary benefit figure
    NBA.plot_marginal_nmb_lines(
        title='Cost-Benefit Analysis',
        x_label='Willingness-To-Pay per Additional QALY($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='c', # show confidence interval
        show_legend=True,
        figure_size=(6, 5),
        file_name='figs/nmb_sensitivity.png'
    )