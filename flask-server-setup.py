"""
A script to automate the setup of a Python3 Flask webserver on an Debian + Nginx environment. 

Will perform the following tasks:

SYSTEM USER
 * Create a dedicated system user to own the files for this project

FOLDERS + FILES
 * Will create a dedicated project folder
 * Will create a uwsgi.py file
 * Will create a placeholder app.py if one does not already exist

VIRTUALENV
 * Create a virtual environment for the project
 * Install packages based on a requirements.txt file if present

UWSGI
 * Create a project.ini
 * /home/<project>/<project>/<project>.ini

SYSTEMD
 * Set the uwsgi application as a system service to start on boot
 * /etc/systemd/system/<project>.service

NGINX
 * Create a server for the domain name provided
 * /etc/nginx/sites-available/<project>

LETSENCRYPT
 * Run let's encrypt for the given domain name

"""

def get_project_information():
    print("~~~ FLASK SERVER SETUP ~~~")
    
    print("\n\nYour project identifier should be an alphanumeric name for your project.")
    print("It will be used for:
    print(" * the username created on the system")
    print(" * the project folder name")
    print(" * the name for the uwsgi ini and socket files")
    project_id = input("Project identifier:")

    print("\n\nWhat is the web domain name your project will be accessible from?")
    print("Note: Please setup your domain name to point to this server before proceeding")
    print("eg: myproject.mydomain.com")
    domain_name = input("Domain name: ")
    return { "id" : project_id, "domain": domain_name }

def is_root():
    return os.geteuid() == 0

def do_user():
    pass

def do_folders_and_files():
    pass

def do_virtualenv():
    pass

def do_uwsgi():
    pass

def do_systemd():
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
