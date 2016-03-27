"""
Automatically generate the configuration files for the pods/replication
controllers/services/auto-scalers.

This script can be run in a sandboxed Docker container using the command `make
generate_k8s_config`.

Configuration values can be set in `config.json` - configurable parameters
include the auto-scaling types possible and the different values for pod
initialization time.
"""

import glob
import json
import shutil
import sys
import os

from jinja2 import Template

# CONFIG_JSON is the file containing the json configuration values.
CONFIG_JSON = "config.json"

# SECRET_CONFIG_JSON is the file containing json configuration values that
# should not be public.
SECRET_CONFIG_JSON = "secret-config.json"

# GENERATED_DIR is the directory in which we store the generated files.
GENERATED_DIR = "generated"

# COMMIT_HASH is the key for the commit hash of HEAD.
COMMIT_HASH = "head_commit_hash"

def _get_file_dir():
    """
    Return the directory containing this file. So that we can use it as a root
    for accessing other files and directories that are either in the same
    directory or subdirectories.

    Returns:
        string: The name of the directory containing this file.
    """

    return os.path.dirname(os.path.realpath(__file__))

def clean_generated_directory():
    """
    Delete all of the files in GENERATED_DIR before generating the new config
    files.
    """
    files_to_del = glob.glob("{0}/{1}/*".format(_get_file_dir(), GENERATED_DIR))

    for del_file in files_to_del:
        os.remove(del_file)

def load_json_config():
    """
    Read in the json configuration values from CONFIG_JSON and
    SECRET_CONFIG_JSON.

    Returns:
        (dict): Dict containing the key/values from CONFIG_JSON and
        SECRET_CONFIG_JSON.
    """
    json_file = "{0}/{1}".format(_get_file_dir(), CONFIG_JSON)
    secret_json_file = "{0}/{1}".format(_get_file_dir(), SECRET_CONFIG_JSON)

    configs = []

    for file_name in [json_file, secret_json_file]:
        with open(file_name, "r") as read_file:
            raw_data = read_file.read()
            json_config = json.loads(raw_data)
            configs.append(json_config)

    all_config = {}
    for config in configs:
        all_config.update(config)

    return all_config

def compute_additional_config():
    """
    Compute additional dynamic configuration that cannot be specified in
    CONFIG_JSON and instead must be dynamically generated each time.

    @TODO Currently we label Docker iamges with the commit hash of the HEAD at
    the time it is built and pushed to Docker Hub. Our k8s configuration files
    must include this label when referencing the image, but we don't want to
    have to update the files by hand each time. However, there is an issue
    because we run this function in a Docker container, but we do not upload our
    entire Git tree to the Docker container, nor can we be sure that Git is
    installed on the Docker container. Thus, we pass the HEAD commit hash as an
    argument to this program.

    Returns:
        (dict): A dictionary containing configuration files used to generate
        templates.
    """
    head_commit_hash = sys.argv[1]
    return {COMMIT_HASH: head_commit_hash}

def generate_unstable_files(config):
    """
    Generate the unstable configuration files. Right now the only unstable
    configuration file is the replication controller configuration file.

    We name the file according to the following scheme:
    - `test-server-controller-AUTOSCALING_METHOD-POD_INITIALIZATION_TIME.yaml`

    We expect the following configuration values:
    - `autoscaling_methods`: A list of auto-scaling method strings, each of
      which has an associated replication controller configuration file.
    - `pod_initialization_times`: A list of pod initialization times, each of
      which has an associated replication controller configuration file.
    - `head_commit_hash`: The label for the Docker image, based on the head
      commit hash for the latest git commit.
    - `database_[name|address|username|password]`: Strings representing the
      respective database configuration values for influxdb.
    """
    rc_config_file = "{0}/{1}".format(_get_file_dir(),
                                      "sample-test-server-controller.yaml.jinja")

    with open(rc_config_file, "r") as config_file:
        template_str = config_file.read()

    hch = config["head_commit_hash"]
    dbn = config["database_name"]
    dba = config["database_address"]
    dbu = config["database_username"]
    dbp = config["database_password"]

    for as_method in config["autoscaling_methods"]:
        for pit in config["pod_initialization_times"]:
            file_name = "{0}/{1}/test-server-controller-{2}-{3}.yaml".format(_get_file_dir(),
                                                                             GENERATED_DIR,
                                                                             as_method, pit)

            rendered_config_str = Template(template_str).render(autoscaling_method=as_method,
                                                                pod_initialization_time=pit,
                                                                head_commit_hash=hch,
                                                                database_name=dbn,
                                                                database_address=dba,
                                                                database_username=dbu,
                                                                database_password=dbp)

            with open(file_name, "w+") as new_config_file:
                new_config_file.write(rendered_config_str)


def generate_stable_files():
    """
    Generate the stable configuration files. Right now the stable configuration
    files are the service and horizontal pod auto-scaling configuration files.

    If any of these files start having files that are templated with jinja, then
    they should be moved into `generate_unstable_files`.
    """
    src_dst_hash = {
        "sample-hpa-test-server.yaml": "hpa-test-server.yaml",
        "sample-test-server-service.yaml": "test-server-service.yaml"}

    for src, dst in src_dst_hash.iteritems():
        src_file_name = "{0}/{1}".format(_get_file_dir(), src)
        dst_file_name = "{0}/{1}/{2}".format(_get_file_dir(), GENERATED_DIR, dst)

        shutil.copy(src_file_name, dst_file_name)

def generate_files(config):
    """
    Write the generated config files to `GENERATED_DIR` using the values
    specified in `config`.

    """
    generate_unstable_files(config)
    generate_stable_files()

def generate_k8s_config():
    """
    This function, called when the script executes, generates the k8s
    configurations files.
    """
    clean_generated_directory()

    json_config = load_json_config()
    additional_config = compute_additional_config()
    json_config.update(additional_config)

    generate_files(json_config)

if __name__ == "__main__":
    generate_k8s_config()
