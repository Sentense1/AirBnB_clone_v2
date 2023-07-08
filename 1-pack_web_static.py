#!/usr/bin/python3
# Fabfile to generate a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local


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
    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None

    # Create the archive using tar command
    if local("tar -cvzf {} web_static".format(file)).failed:
        return None

    # Return the file path of the generated archive
    return file
