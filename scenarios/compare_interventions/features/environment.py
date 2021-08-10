""" Set up the environment for compare vaccine features. """
import pandas as pd
from behave import fixture, use_fixture
import os
import re

obs_tag_re = re.compile('observational\(("|\')(.+)("|\')\)')

@fixture
def set_desired_outputs(context):
    """ Add a results dataframe which stores simulation outputs to context. """
    context.desired_outputs = []


@fixture
def set_parameters_dict(context):
    """ Add a parameters dictionary which stores simulation parameters to context."""
    context.params_dict = dict()
    context.types = {}

def before_feature(context, feature):
    print(f"Running Feature `{feature.name}`")
    use_fixture(set_parameters_dict, context)
    feature_name = context.feature.name.lower().replace(" ", "-")
    context.dag_path = f"dags/{feature_name}.dot"
    context.results_dir = f"results/{feature_name}"
    context.estimates_file = f"results/estimates/{feature_name}.csv"
    if not os.path.exists(context.results_dir):
        os.makedirs(context.results_dir, exist_ok=True)
    if not os.path.exists(f"results/estimates/"):
        os.makedirs(f"results/estimates/", exist_ok=True)
    with open(context.estimates_file, 'w') as f:
        print("treatment_var,outcome_var,control_val,treatment_val,estimate,ci_low,ci_high", file=f)

def after_feature(context, feature):
    print(f"Finished Feature `{feature.name}`")


def before_tag(context, tag):
    obs_match = obs_tag_re.match(tag)
    if obs_match:
        context.data = obs_match.group(2)
