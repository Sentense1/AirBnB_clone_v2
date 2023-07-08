#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["54.87.224.2", "54.89.109.20"]


def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    # Get the list of archives in the local 'versions' directory
    archives = sorted(os.listdir("versions"))

    # Delete out-of-date archives from the local directory
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Get the list of archives in the remote '/data/web_static/releases' directory
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]

        # Delete out-of-date archives from the remote directory
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
