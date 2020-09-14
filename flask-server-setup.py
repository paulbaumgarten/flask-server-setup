"""
A script to automate the setup of a Python3 Flask webserver on an Debian + Nginx environment. 

Will perform the following tasks:

FOLDERS + FILES
 * Will create a dedicated project folder at /home/<user>/<project>
 * Will create a uwsgi.py file
 * Will create a placeholder app.py if one does not already exist

VIRTUALENV
 * Create a virtual environment for the project
 * Install packages based on a requirements.txt file if present

UWSGI
 * Create a project.ini
 * /home/<user>/<project>/<project>.ini

SYSTEMD
 * Set the uwsgi application as a system service to start on boot
 * /etc/systemd/system/<project>.service

NGINX
 * Create a server for the domain name provided
 * /etc/nginx/sites-available/<project>

LETSENCRYPT
 * Run let's encrypt for the given domain name

"""

import os

def get_project_information():
    print("~~~ FLASK SERVER SETUP ~~~")
    
    print("\n\nExisting user that should own all the project files")
    print("(to create a user, the name for the uwsgi ini and socket files")
    user = input("User to own the project files:")

    print("\n\nYour project identifier should be an alphanumeric name for your project.")
    print("It will be used for:
    print(" * the project folder name, eg /home/<user>/<project>")
    print(" * the name for the uwsgi ini and socket files")
    project_id = input("Project identifier:")

    print("\n\nWhat is the web domain name your project will be accessible from?")
    print("Note: Please setup your domain name to point to this server before proceeding")
    print("eg: myproject.mydomain.com")
    domain_name = input("Domain name: ")
    return { "id" : project_id, "domain": domain_name }

def is_root():
    return os.geteuid() == 0

def do_folders_and_files():
    # create /home/<user>/<project>
    pass

def do_virtualenv():
    # pip3 install virtualenv
    # virtualenv projectenv
    # source projectenv/bin/activate
    # pip3 install uwsgi flask
    # pip3 install -r requirements.txt
    # deactivate
    pass

def do_uwsgi():
    # wsgi.py
    content = f"""
from main import app
if __name__ == "__main__":
   app.run()
"""
    # project.ini
    content = f"""[uwsgi]
module = wsgi:app
master = true
processes = 5
socket = project.sock
chmod-socket = 666
vacuum = true
die-on-term = true
"""

def do_systemd():
    # /etc/systemd/system/<project>.service
    # systemctl enable <project>
    # systemctl start <project>
    content = f"""
[Unit]
Description=My great flask project
After=network.target

[Service]
User=userid
Group=groupid
WorkingDirectory=</path/to/project>
Environment="PATH=</path/to/project>/projectenv/bin"
Environment="CLIENT_SECRETS=/folder/folder/client_secrets.json"
ExecStart=</path/to/project>/projectenv/bin/uwsgi --ini project.ini

[Install]
WantedBy=multi-user.target
"""
    pass

def do_nginx():
    pass

def do_letsencrypt():
    pass

if __name__=="__main__":
    if not is_root():
        print("Requires root privileges. Exiting...")
        exit()
    info = get_project_information()


"""
Resources during writing this:

https://janakiev.com/blog/python-shell-commands/
"""

