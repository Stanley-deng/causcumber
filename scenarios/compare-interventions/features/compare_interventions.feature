# This file MUST be run from inside ../compare_interventions, otherwise it won't
# be able to find the causal DAG. Run as `behave features/compare_interventions.feature`
Feature: Compare interventions
  Background:
    Given a simulation with parameters
      | parameter    | value  | type |
      | quar_period  | 14     | int  |
      | n_days       | 84     | int  |
      | pop_type     | hybrid | str  |
      | pop_size     | 50000  | int  |
      | pop_infected | 100    | int  |
      | location     | UK     | str  |
    And the following variables are recorded weekly
      | variable          | type |
      | cum_tests         | int  |
      | n_quarantined     | int  |
      | n_exposed         | int  |
      | cum_infections    | int  |
      | cum_symptomatic   | int  |
      | cum_severe        | int  |
      | cum_critical      | int  |
      | cum_deaths        | int  |

  @current
  Scenario: Baseline
    Given we run the model with an intervention baseline
    Then all weekly variables are recorded

  # TODO: this is a bit clunky. It might not be  reasonable to assume that a
  # domain expert would be able to list all edges that wouldn’t be present
  # before seeing the connected graph
  Scenario: Draw DAG
    Given a connected repeating unit
    When we prune the following edges
      | s1                | s2                 |
      | quar_period       | n_exposed_n        |
      | quar_period       | cum_infections_n   |
      | quar_period       | cum_symptomatic_n  |
      | quar_period       | cum_severe_n       |
      | quar_period       | cum_critical_n     |
      | quar_period       | cum_deaths_n       |
      | quar_period       | cum_tests_n        |
      | intervention      | cum_infections_n   |
      | intervention      | cum_symptomatic_n  |
      | intervention      | cum_severe_n       |
      | intervention      | cum_critical_n     |
      | intervention      | cum_deaths_n       |
      | pop_type          | cum_deaths_n       |
      | pop_type          | cum_tests_n        |
      | pop_size          | cum_deaths_n       |
      | pop_size          | cum_tests_n        |
      | location          | cum_deaths_n       |
      | location          | cum_tests_n        |
      | pop_infected      | n_quarantined_n    |
      | pop_infected      | n_exposed_n        |
      | pop_infected      | cum_deaths_n       |
      | pop_infected      | cum_tests_n        |
      | n_days            | n_quarantined_n    |
      | n_days            | n_exposed_n        |
      | n_days            | cum_infections_n   |
      | n_days            | cum_symptomatic_n  |
      | n_days            | cum_severe_n       |
      | n_days            | cum_critical_n     |
      | n_days            | cum_deaths_n       |
      | n_days            | cum_tests_n        |
      | n_quarantined_n   | cum_infections_n1  |
      | n_quarantined_n   | cum_symptomatic_n1 |
      | n_quarantined_n   | cum_severe_n1      |
      | n_quarantined_n   | cum_critical_n1    |
      | n_quarantined_n   | cum_tests_n1       |
      | n_quarantined_n   | cum_deaths_n1      |
      | n_exposed_n       | n_quarantined_n1   |
      | n_exposed_n       | cum_symptomatic_n1 |
      | n_exposed_n       | cum_severe_n1      |
      | n_exposed_n       | cum_critical_n1    |
      | n_exposed_n       | cum_deaths_n1      |
      | n_exposed_n       | cum_tests_n1       |
      | cum_infections_n  | cum_severe_n1      |
      | cum_infections_n  | cum_critical_n1    |
      | cum_infections_n  | cum_deaths_n1      |
      | cum_infections_n  | cum_tests_n1       |
      | cum_symptomatic_n | n_exposed_n1       |
      | cum_symptomatic_n | cum_critical_n1    |
      | cum_symptomatic_n | cum_deaths_n1      |
      | cum_symptomatic_n | cum_tests_n1       |
      | cum_severe_n      | n_quarantined_n1   |
      | cum_severe_n      | n_exposed_n1       |
      | cum_severe_n      | cum_infections_n1  |
      | cum_severe_n      | cum_symptomatic_n1 |
      | cum_severe_n      | cum_tests_n1       |
      | cum_severe_n      | cum_deaths_n1      |
      | cum_critical_n    | n_quarantined_n1   |
      | cum_critical_n    | n_exposed_n1       |
      | cum_critical_n    | cum_infections_n1  |
      | cum_critical_n    | cum_symptomatic_n1 |
      | cum_critical_n    | cum_severe_n1      |
      | cum_critical_n    | cum_tests_n1       |
      | cum_tests_n       | n_exposed_n1       |
      | cum_tests_n       | cum_infections_n1  |
      | cum_tests_n       | cum_symptomatic_n1 |
      | cum_tests_n       | cum_severe_n1      |
      | cum_tests_n       | cum_critical_n1    |
      | cum_tests_n       | cum_deaths_n1      |
      | cum_deaths_n      | n_quarantined_n1   |
      | cum_deaths_n      | cum_infections_n1  |
      | cum_deaths_n      | cum_symptomatic_n1 |
      | cum_deaths_n      | cum_severe_n1      |
      | cum_deaths_n      | cum_critical_n1    |
    Then we obtain the causal DAG for 12 weeks

  Scenario Outline: Testing
    Given we run the model with an intervention <control>
    When we run the model with an intervention <treatment>
    Then the "cum_deaths" should be <relationship> <control>
    Examples:
      | control       | treatment     | relationship |
      | baseline      | standardTest  | <            |
      | baseline      | noTest        | =            |
      | standardTest  | optimalTest   | <            |
      | baseline      | standardTrace | <            |
      | standardTest  | standardTrace | <            |
      | standardTest  | noTrace       | =            |
      | standardTrace | optimalTrace  | <            |
      | baseline      | traceNoTest   | =            |

  # This depends on the existence of observational data. We need lots of runs to
  # get a reliable estimate. Essentially, we need to just run the model with
  # some different starting parameters. We can reuse data from prior test runs
  # by just pulling it all in. This works under the assumption that all the
  # CSV files have the same columns.

  Scenario: Subsequent mortality (has confounding)
    Given a control scenario where cum_infections_7=4000
    When cum_infections_7=5000
    Then the "cum_deaths" should be "more than" control
