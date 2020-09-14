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
import subprocess
import time

def get_project_information():
    print("~~~ FLASK SERVER SETUP ~~~")
    
    print("\n\nYour project identifier should be an alphanumeric name for your project.")
    print("It will be used for:")
    print(" * the project folder name, eg /home/<user>/<project>")
    print(" * the name for the uwsgi ini and socket files")
    projectid = input("Project identifier:")

    print("\n\nWhat is the web domain name your project will be accessible from?")
    print("Note: Please setup your domain name to point to this server before proceeding")
    print("eg: myproject.mydomain.com")
    domain = input("Domain name: ")
    return projectid, domain

def is_root():
    return os.geteuid() == 0

if __name__=="__main__":
    userid = os.getlogin()
    if not is_root() and userid != "root":
        print("Run with sudo privileges while logged in as the user you want to own the files...")
        exit()
    projectid, domain = get_project_information()
    folder = os.path.join(os.path.expanduser("~"), projectid)
    current_working_directory = os.getcwd()

    # ****************************************************************************
    # CREATE FILE STRINGS
    # ****************************************************************************

    app_py = f"""
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello There!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
"""

    # ****************************************************************************

    wsgi_py = f"""
from app import app
if __name__ == "__main__":
   app.run()
"""

    # ****************************************************************************

    project_service = f"""
[Unit]
Description={projectid}
After=network.target

[Service]
User={userid}
Group=www-date
WorkingDirectory={folder}
Environment="PATH={folder}/venv/bin"
ExecStart={folder}/venv/bin/uwsgi --ini project.ini

[Install]
WantedBy=multi-user.target
"""

    # ****************************************************************************

    nginx_conf = f"""
server {{
	listen 443 ssl;
	listen [::]:443 ssl;
	server_name {domain};
	location / {{
		include uwsgi_params;
		uwsgi_pass unix:{folder}/project.sock;
		access_log on;
		error_log on;
	}}

}}
"""

    # ****************************************************************************

    project_ini = f"""[uwsgi]
module = wsgi:app
master = true
processes = 5
socket = project.sock
chmod-socket = 660
vacuum = true
die-on-term = true
"""

    # ****************************************************************************
    # PERFORM TASKS
    # ****************************************************************************

    # **** PROJECT FOLDERS AND FILES ****

    # create /home/<user>/<project>
    print("\n\nfolders: creating project folder...")
    if not os.path.exists(folder):
        print(f"{folder}... creating")
        try:
            os.mkdir(folder)
        except OSError:
            print("Could not create folder "+folder)
            exit(1)
    else:
        print(f"{folder}... already exists")
    print("\n\nfolders: changing into project folder...")
    os.chdir(folder)
    time.sleep(5)

    # **** VIRTUAL ENVIRONMENT ****

    # install venv ... apt install python3-venv
    print("\n\nvenv: installing...")
    response = subprocess.run(["apt", "install", "python3-venv"])
    if response.returncode != 0:
        print("Error occurred, terminating")
        exit(1)
    time.sleep(5)

    # virtualenv projectenv
    print("\n\nvenv: creating virtual envionment...")
    response = subprocess.run(["python3", "-m", "venv", "venv"])
    if response.returncode != 0:
        print("Error occurred, terminating")
        exit(1)
    time.sleep(5)

    # source projectenv/bin/activate
    print("\n\nvenv: activating virtual envionment...")
    commands = ["source venv/bin/activate"]
    # pip3 install uwsgi flask
    print("\n\nvenv: installing packages into virtual envionment...")
    commands.append("pip install uwsgi flask")
    # pip3 install -r requirements.txt
    if os.path.exists(folder+"/requirements.txt"):
        print("\n\nvenv: requirements.txt found and used...")
        commands.append("pip install -r requirements.txt")
    else:
        print("\n\nvenv: requirements.txt not found...")
    # deactivate
    print("\n\nvenv: deactivating virtual envionment...")
    commands.append("deactivate")
    subprocess.run(';'.join(commands), shell=True)
    time.sleep(5)

    # **** WSGI ****

    # create /home/<user>/<project>/app.py
    target = os.path.join(folder, "app.py")
    if not os.path.exists(target):
        print(f"\n\nwsgi: creating {target}...")
        with open(target, "w") as f:
            f.write(wsgi_py)
    else:
        print(f"\n\nwsgi: already exists {target}...")
    time.sleep(5)

    # create /home/<user>/<project>/wsgi.py
    target = os.path.join(folder, "wsgi.py")
    print(f"\n\nwsgi: creating {target}...")
    with open(target, "w") as f:
        f.write(wsgi_py)

    # create /home/<user>/<project>/project.ini
    target = os.path.join(folder, "project.ini")
    print(f"\n\nwsgi: creating {target}...")
    with open(target, "w") as f:
        f.write(project_ini)

    # create /etc/systemd/system/<project>.service
    target = f"/etc/systemd/system/{projectid}.service"
    print(f"\n\nsystemd: creating {target}...")
    with open(target, "w") as f:
        f.write(project_service)

    # execute systemctl enable <project>
    print(f"\n\nsystemd: enabling and starting {projectid}...")

    # execute systemctl start <project>
    print(f"\n\nsystemd: starting {projectid}...")
    commands = [
        f"systemctl enable {projectid}", 
        f"systemctl start {projectid}", 
        f"systemctl status {projectid}" 
        ]
    subprocess.run(';'.join(commands), shell=True)
    time.sleep(5)

    # **** NGINX ****
    target = f"/etc/nginx/sites-available/{projectid}"
    print(f"\n\nnginx: creating {target}...")
    with open(target, "w") as f:
        f.write(project_service)

    # ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
    print("\n\nnginx: linking sites-available to sites-enabled")
    response = subprocess.run(["ln", "-s", target, "/etc/nginx/sites-enabled"])
    time.sleep(5)

    # nginx -t
    print("\n\nnginx: config file check")
    response = subprocess.run(["nginx", "-t"])
    time.sleep(5)

    # systemctl restart nginx
    print("\n\nnginx: restarting nginx")
    response = subprocess.run(["systemctl", "restarts", "nginx"])
    time.sleep(5)

    # **** LETS ENCRYPT ****

    # apt install certbot python3-certbot-nginx
    print("\n\ncertbox: installing")
    response = subprocess.run(["apt", "install", "certbot", "python3-certbot-nginx"])
    time.sleep(5)

    # certbot --nginx -d your_domain
    print("\n\nnginx: certbox adding domain")
    response = subprocess.run(["certbot", "--nginx", "-d", domain])
    time.sleep(5)


