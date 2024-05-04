import deampy.econ_eval as econ
import deampy.plots.histogram as hist
import deampy.plots.sample_paths as path
import deampy.statistics as stat

import InputData as data


def print_outcomes(sim_outcomes, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param sim_outcomes: outcomes of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval of patient survival time
    survival_mean_CI_text = sim_outcomes.statSurvivalTimes.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    # mean and confidence interval text of time to severe state
    time_to_SEVERE_CI_text = sim_outcomes.statTimeToSEVERE.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = sim_outcomes.statCost.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=0, form=',')

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = sim_outcomes.statUtilities.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of mean time to severe state and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          time_to_SEVERE_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")


def plot_survival_curves_and_histograms(sim_outcomes_soc, sim_outcomes_dmt):
    """ draws the survival curves and the histograms of time until HIV deaths
    :param sim_outcomes_soc: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_dmt: outcomes of a cohort simulated under combination therapy
    """

    # get survival curves of both treatments
    survival_curves = [
        sim_outcomes_soc.nLivingPatients,
        sim_outcomes_dmt.nLivingPatients
    ]

    # plot survival curve
    path.plot_sample_paths(
        sample_paths=survival_curves,
        x_label='Simulation time step (year)',
        y_label='Number of alive patients',
        figure_size=(6,5),
        legends=['Donepezil', 'Disease Modifying Treatment at 30% effectiveness'],
        color_codes=['cornflowerblue', 'midnightblue'],
        file_name='figs/compare/survival_curves.png'
    )

    # histograms of survival times
    set_of_time_to_severe = [
        sim_outcomes_soc.survivalTimes,
        sim_outcomes_dmt.survivalTimes
    ]

    # graph histograms
    hist.plot_histograms(
        data_sets=set_of_time_to_severe,
        x_label='Survival time (year)',
        y_label='Counts',
        bin_width=1,
        legends=['Donepezil', 'Disease Modifying Treatment at 30% effectiveness'],
        color_codes=['cornflowerblue', 'midnightblue'],
        transparency=0.5,
        file_name='figs/compare/survival_times.png'
    )

    # histogram of time to reach SEVERE state
    set_of_time_to_severe = [
        sim_outcomes_soc.timeToSEVERE,
        sim_outcomes_dmt.timeToSEVERE
    ]

    # graph histograms
    hist.plot_histograms(
        data_sets=set_of_time_to_severe,
        x_label='Survival time (year)',
        y_label='Counts',
        bin_width=1,
        legends=['Donepezil', 'Disease Modifying Treatment at 30% effectiveness'],
        color_codes=['cornflowerblue', 'midnightblue'],
        transparency=0.5,
        file_name='figs/compare/times_severe_state.png'
    )


def plot_survival_curves_and_histograms_multi(multi_cohort_outcomes_soc, multi_cohort_outcomes_dmt30):
    """ plot the survival curves and the histograms of survival times
    :param multi_cohort_outcomes_soc: outcomes of a multi-cohort simulated under mono therapy
    :param multi_cohort_outcomes_dmt30: outcomes of a multi-cohort simulated under combination therapy
    """

    # get survival curves of both treatments
    sets_of_survival_curves = [
        multi_cohort_outcomes_soc.survivalCurves,
        multi_cohort_outcomes_dmt30.survivalCurves
    ]

    # graph survival curve
    path.plot_sets_of_sample_paths(
        sets_of_sample_paths=sets_of_survival_curves,
        x_label='Simulation Time Step (year)',
        y_label='Number of Patients Alive',
        legends=['Donepezil', 'Disease Modifying Treatment at 30% effectiveness'],
        transparency=0.4,
        color_codes=['cornflowerblue', 'midnightblue'],
        figure_size=(6, 5),
        file_name='figs/compare/multicohort/survival_curves_multicohort.png'
    )

    # histograms of survival times
    set_of_time_to_severe = [
        multi_cohort_outcomes_soc.meanSurvivalTimes,
        multi_cohort_outcomes_dmt30.meanSurvivalTimes
    ]

    # graph histograms
    hist.plot_histograms(
        data_sets=set_of_time_to_severe,
        x_label='Survival Time (year)',
        y_label='Counts',
        bin_width=0.1,
        x_range=[5, 15],
        legends=['Donepezil', 'Disease Modifying Treatment at 30% effectiveness'],
        color_codes=['cornflowerblue', 'midnightblue'],
        transparency=0.5,
        figure_size=(6, 5),
        file_name='figs/compare/multicohort/survival_times_multicohort.png'
    )

    # histograms of time to reach severe state
    set_of_time_to_severe = [
        multi_cohort_outcomes_soc.meanTimeToSEVERE,
        multi_cohort_outcomes_dmt30.meanTimeToSEVERE
    ]

    # graph histograms
    hist.plot_histograms(
        data_sets=set_of_time_to_severe,
        x_label='Survival Time (year)',
        y_label='Counts',
        bin_width=0.1,
        x_range=[5, 15],
        legends=['Donepezil', 'Disease Modifying Treatment at 30% effectiveness'],
        color_codes=['cornflowerblue', 'midnightblue'],
        transparency=0.5,
        figure_size=(6, 5),
        file_name='figs/compare/multicohort/times_multicohort_severe_state.png'
    )


def print_comparative_outcomes(sim_outcomes_soc, sim_outcomes_dmt):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under dmt compared to donepezil
    :param sim_outcomes_soc: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_dmt: outcomes of a cohort simulated under combination therapy
    """

    # increase in mean survival time under combination therapy with respect to mono therapy
    increase_survival_time = stat.DifferenceStatIndp(
        name='Increase in mean survival time',
        x=sim_outcomes_dmt.survivalTimes,
        y_ref=sim_outcomes_soc.survivalTimes)

    # estimate and CI
    estimate_CI = increase_survival_time.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)
    print("Increase in mean survival time and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0),  estimate_CI)

    # increase in mean time to severe under dmt with respect to donepezil
    increase_time_to_severe = stat.DifferenceStatIndp(
        name='Increase in mean time to severe state',
        x=sim_outcomes_dmt.timeToSEVERE,
        y_ref=sim_outcomes_soc.timeToSEVERE)

    # estimate and CI
    estimate_CI = increase_time_to_severe.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)
    print("Increase in mean time to severe state and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)

    # increase in mean discounted cost under dmt with respect to donepezil
    increase_discounted_cost = stat.DifferenceStatIndp(
        name='Increase in mean discounted cost',
        x=sim_outcomes_dmt.costs,
        y_ref=sim_outcomes_soc.costs)

    # estimate and CI
    estimate_CI = increase_discounted_cost.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2, form=',')
    print("Increase in mean discounted cost and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)

    # increase in mean discounted utility under dmt with respect to donepezil
    increase_discounted_utility = stat.DifferenceStatIndp(
        name='Increase in mean discounted utility',
        x=sim_outcomes_dmt.utilities,
        y_ref=sim_outcomes_soc.utilities)

    # estimate and CI
    estimate_CI = increase_discounted_utility.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)


def report_CEA_CBA(sim_outcomes_soc, sim_outcomes_dmt):
    """ performs cost-effectiveness and cost-benefit analyses
    :param sim_outcomes_soc: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_dmt: outcomes of a cohort simulated under combination therapy
    """

    # define two strategies
    soc_therapy_strategy = econ.Strategy(
        name='Donepezil',
        cost_obs=sim_outcomes_soc.costs,
        effect_obs=sim_outcomes_soc.utilities,
        color='cornflowerblue'
    )
    dmt_therapy_strategy = econ.Strategy(
        name='Disease Modifying Treatment at 30% effectiveness',
        cost_obs=sim_outcomes_dmt.costs,
        effect_obs=sim_outcomes_dmt.utilities,
        color='midnightblue'
    )

    # do CEA
    # (the first strategy in the list of strategies is assumed to be the 'Base' strategy)
    CEA = econ.CEA(
        strategies=[soc_therapy_strategy, dmt_therapy_strategy],
        if_paired=False
    )

    # plot cost-effectiveness figure
    CEA.plot_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional QALYs',
        y_label='Additional Cost',
        interval_type='c',  # to show confidence intervals for cost and effect of each strategy
        file_name='figs/cea/cea.png'
    )

    # report the CE table
    CEA.build_CE_table(
        interval_type='c',
        alpha=data.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='CETable.csv')

    # CBA
    CBA = econ.CBA(
        strategies=[soc_therapy_strategy, dmt_therapy_strategy],
        wtp_range=[0, 150000],
        if_paired=False
    )
    # show the net monetary benefit figure
    CBA.plot_marginal_nmb_lines(
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay per QALY ($)',
        y_label='Marginal Net Monetary Benefit ($)',
        interval_type='c',
        show_legend=True,
        figure_size=(6, 5),
        file_name='figs/cea/nmb.png'
    )
