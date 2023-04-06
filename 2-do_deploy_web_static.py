#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers, using the
function do_deploy.
"""

import os.path
from fabric.api import *
from fabric.operations import run, put, sudo

env.hosts = ['52.55.249.21', '54.157.32.137']

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.isfile(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension>
        archive_filename = os.path.basename(archive_path)
        archive_basename = os.path.splitext(archive_filename)[0]
        remote_path = "/data/web_static/releases/{}".format(archive_basename)
        run("sudo mkdir -p {}".format(remote_path))
        run("sudo tar -xzf /tmp/{} -C {}".
            format(archive_filename, remote_path))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(archive_filename))

        # Move contents of web_static to /data/web_static/releases/
        run("sudo mv {}/web_static/* {}/".format(remote_path, remote_path))
        run("sudo rm -rf {}/web_static".format(remote_path))

        # Delete the symbolic link /data/web_static/current from the web server
        run("sudo rm -rf /data/web_static/current")

        # Create a new the symbolic link /data/web_static/current on the web server
        # linked to the new version of your code
        run("sudo ln -s {} /data/web_static/current".format(remote_path))

        print("New version deployed!")
        return True

    except Exception:
        return False
 
