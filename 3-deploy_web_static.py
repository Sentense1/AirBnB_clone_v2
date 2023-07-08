#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["54.87.224.2", "54.89.109.20"]


def do_pack():
    """
    Create a tar gzipped archive of the directory web_static.
    Returns:
        str: The file path of the generated archive, or None if the archive creation failed.
    """
    # Get the current UTC datetime
    dt = datetime.utcnow()

    # Create the file name for the archive using the date and time
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)

    # Create the 'versions' directory if it doesn't exist
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None

    # Create the archive using tar command
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None

    # Return the file path of the generated archive
    return file


def do_deploy(archive_path):
    """
    Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        bool: True if the distribution is successful, False otherwise.
    """
    # Check if the file exists at the specified path
    if os.path.isfile(archive_path) is False:
        return False

    # Extract the file name and name of the release directory
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Upload the archive to the remote server
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False

    # Remove existing release directory
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False

    # Create the release directory
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed is True:
        return False

    # Extract the archive into the release directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed is True:
        return False

    # Remove the temporary archive
    if run("rm /tmp/{}".format(file)).failed is True:
        return False

    # Move the contents of the web_static folder to the release directory
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed is True:
        return False

    # Remove the now empty web_static folder
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed is True:
        return False

    # Update the symbolic link to the new release directory
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed is True:
        return False

    # Print a success message
    print("New version deployed!")

    return True


def deploy():
    """
    Create and distribute an archive to a web server.
    Returns:
        bool: True if the deployment is successful, False otherwise.
    """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
