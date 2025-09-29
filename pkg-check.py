# Package Update Checker
# Kaylee Hinton
# CS 310 Systems Administration
# Description: Checks for packages to update and lists them to a text file. Then creates a 
# cron job to run the update checks weekly. Finally checks if the cronjob was created correctly.

from crontab import CronTab
import subprocess
import os

# Gives the path for the script
script_path = os.path.abspath(__file__)

# Creates the sudo command for the script
sudo_command = f'sudo python3 {script_path}'

def check_updates():
    """ Checks for package updates and lists new updates in a text file. """

    # Updates the list of packages
    subprocess.run(['sudo', 'apt', 'update', '-qq'])

    # Creates a list of packages that can be updated
    result = subprocess.run(['apt', 'list', '--upgradable'], capture_output=True, text=True)

    # Writes all packages that can be updated to a text file
    with open('update-list.txt', 'w') as f:
        f.write(result.stdout)

def create_cron():
    """ Checks if a cron job exists and creates a new one if it does not exist. """
    
    # Points to the text file where the cronjobs are listed
    cron = CronTab(tabfile="local-crontab.txt") 

    # Checks if a cronjob has been created
    created_job = any(job.command == sudo_command for job in cron)

    # Creates a new cronjob if it does not exist
    if not created_job:
        job = cron.new(command=sudo_command)
        job.setall('0 0 * * 0')
        cron.write()
        print("New cronjob created")

    else:
        print("This job already exists")


def check_if_cron_exists():
    """ Checks if the cron job was created correctly. """

    # Points to the text file where the cronjobs are listed
    cron = CronTab(tabfile="local-crontab.txt") 
    
    # Looks to see if the job was created sucessfully
    for job in cron:
        if job.command == sudo_command:
            print("Cron job exists")
            break
    else:
        print("Cron job not found")


if __name__ == '__main__':
    check_updates()
    create_cron()
    check_if_cron_exists()


    