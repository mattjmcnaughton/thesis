"""
Automatically generates the configuration files to run the traffic generator on
Kubernetes.

This script can be run in a sandboxed Docker container using `make
generate_k8s_config`.

@TODO Right now there is a lot of code duplication between this file and the
instance of `generate_k8s_config.py` that's in the `test-server` dir. Maybe
there is a way to make this a `pip` package, or at least a more abstract script
that both can use? Also see that version for more intensive documentation.
"""

import glob
import os

from jinja2 import Template

GENERATED_DIR = "generated"
TEST_PLANS_DIR = "test-plans"

def _get_file_dir():
    """
    Return the directory containing this python script to use as root.

    Returns:
        string: The file dir.
    """
    return os.path.dirname(os.path.realpath(__file__))

def clean_generated_directory():
    """
    Delete all the files in the generated directory before creating the new
    one.
    """
    files_to_del = glob.glob("{0}/{1}/*".format(_get_file_dir(), GENERATED_DIR))

    for del_file in files_to_del:
        os.remove(del_file)

def get_all_test_plans():
    """
    Return a list of the names of all of the different test plans by reading all
    of the test plans in the directory.

    Returns:
        [string]: A list of the different test plans to generate config files
        for.
    """

    test_plans = []

    test_plan_files = glob.glob("{0}/../{1}/*".format(_get_file_dir(),
                                                      TEST_PLANS_DIR))

    for file_name in test_plan_files:
        name = os.path.splitext(file_name)[0].split("/")[-1]
        test_plans.append(name)

    return test_plans

def generate_files():
    """
    Write the generated files to `GENERATED_DIR`.

    We create a file for each of the following configuration values:
    - `test-plan`: The name (without jsx) of the `test-plan` we want to run on
      Kubernetes.
    """
    rc_config_file = "{0}/{1}".format(_get_file_dir(),
                                      "sample-traffic-generator-controller.yaml.jinja")

    with open(rc_config_file, "r") as config_file:
        template_str = config_file.read()

    test_plans = get_all_test_plans()

    for test_plan in test_plans:
        file_name = "{0}/{1}/traffic-generator-controller-{2}.yaml".format(_get_file_dir(),
                                                                           GENERATED_DIR,
                                                                           test_plan)
        rendered_config_str = Template(template_str).render(test_plan=test_plan)

        with open(file_name, "w+") as new_config_file:
            new_config_file.write(rendered_config_str)

def generate_k8s_config():
    """
    Generate the replication controller config file for the pod containing
    jmeter.
    """
    clean_generated_directory()

    generate_files()

if __name__ == "__main__":
    generate_k8s_config()
