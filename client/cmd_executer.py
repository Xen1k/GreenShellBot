import os
import subprocess

def execute_shell_command(command):
    def get_current_path():
        return 'Path: {}'.format(os.path.abspath(os.getcwd()))
        
    # Change the directory
    if(command.split()[0].lower() == 'cd'):
        try:
            abs_path = os.path.join(os.path.abspath(os.getcwd()), command[3:])
            os.chdir(abs_path)
            return get_current_path()
        except:
            return 'Problem to get to the path!'
    # Change the drive
    if(len(command) == 2 and command[1] == ':'):
        try:
            os.chdir(command)
            return get_current_path()
        except:
            return 'Problem to change the drive!'
    
    return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('cp866')