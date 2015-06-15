from rpg.command import Command
from os.path import expanduser
import configparser

class CoprUploader:
    
    def setup_config(self, username, login, token):
        config = configparser.ConfigParser()
        config['copr-cli'] = { 'username': username,
                              'login': login,
                              'token': token,
                              'copr_url': 'http://copr.fedoraproject.org'}
        config_path = expanduser('~') + '/.config/copr'
        with open(config_path, 'w') as config_file:
            config.write(config_file)
                
    
    def create_copr(self, name, chroots, description='', instructions=''):
        command = 'copr-cli create'
        parameters = ''
        for chroot in chroots:
            parameters = parameters + ' --chroot ' + str(chroot)
        if description:
            parameters = parameters + ' --description \'' + description + '\''
        if instructions:
            parameters = parameters + ' --instructions \'' + instructions + '\''
        parameters = parameters + ' ' + name
        Command(command + parameters).execute()
        
    def build_copr(self, name, srpm_url):
        command = 'copr-cli build '
        parameters = name + ' ' + srpm_url
        Command(command + parameters).execute()
