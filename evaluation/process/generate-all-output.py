#!/usr/bin/env python
#
# A hacky python script to generate all of the relevant graphs and statistics.

import subprocess

if __name__ == "__main__":
    pits = ["135s"]
    flags = ["--only-eru", "--only-qos", ""]

    version_lists = {
        "v1": ["increase-decrease", "flash-crowd"],
        "v2": ["increase-decrease", "step-ladder", "flash-crowd-short", "jagged-edge"]
    }

    for version, version_list in version_lists.iteritems():
        for pit in pits:
            for tp in version_list:
                for flag in flags:
                    command = ("export PIT={0}; export TP={1}; export VERSION={2}; "
                               "export OUT=/code/output; export FLAG={3}; "
                               "make process").format(pit, tp, version, flag)

                    subprocess.call(["bash", "-c", command])
