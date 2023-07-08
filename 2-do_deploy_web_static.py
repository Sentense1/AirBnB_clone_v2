#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["54.87.224.2", "54.89.109.20"]


def do_deploy(archive_path):
    """
    Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        bool: True if the distribution is successful, False otherwise.
    """
    # Check if the file exists at the specified path
    if not os.path.isfile(archive_path):
        return False

    # Extract the file name and name of the release directory
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Upload the archive to the remote server
    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False

    # Remove existing release directory
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False

    # Create the release directory
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    # Extract the archive into the release directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(file, name)).failed:
        return False

    # Remove the temporary archive
    if run("rm /tmp/{}".format(file)).failed:
        return False

    # Move the contents of the web_static folder to the release directory
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False

    # Remove the now empty web_static folder
    if run("rm -rf /data/web_static/releases/{}/web_static"
            .format(name)).failed:
        return False

    # Update the symbolic link to the new release directory
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(name)).failed:
        return False
    
    print("New version deployed!")

    return True
