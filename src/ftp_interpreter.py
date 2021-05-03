import os
from ftplib import FTP
from cmd import Cmd


class FtpInterpreter(Cmd):
    """pro
    FTP client command line utility.
    """
    def __init__(self, debug=False):
        Cmd.__init__(self)
        self.intro = ('xD')
        self.prompt = 'FTP > '
        self._ftp_client = FTP()

    def _update_prompt(self, user=None):
        prompt = 'FTP'
        if self._ftp_client.host is not None:
            prompt = '{} {}'.format(prompt, self._ftp_client.host)
            if user is not None:
                prompt = '{} ({})'.format(prompt, user)
        self.prompt = '{} > '.format(prompt)

    def _perform_ftp_command(self, command, *args):
        method = getattr(self._ftp_client, command)
        try:
            response = method(*args)
        except Exception as e:
            return e
        return response

    def do_connect(self, host):
        response = self._perform_ftp_command('connect', host)
        print(response)
        self._update_prompt()

    def do_login(self, *args):
        user = input('User: ')
        password = input('Password: ')
        response = self._perform_ftp_command('login', user, password)
        print(response)
        if user == '':
            user = 'Anonymous'
        self._update_prompt(user)

    def do_bye(self, *args):
        quit()

    def do_quit(self, *args):
        quit()

    def do_close(self, *args):
        response = self._perform_ftp_command('quit')
        print(response)
        self._ftp_client = FTP()

    def do_dir(self, *args):
        response = self._perform_ftp_command('dir')
        print(response)

    def do_mkdir(self, dir_name):
        response = self._perform_ftp_command('mkd', dir_name)
        print(response)


    def do_list(self, filename):
        """
        Command to perform LIST command on the connected FTP host.
        Args:
            filename (str): Name of file or directory to retrieve info for.
        """
        response = self._perform_ftp_command('list', filename)
        print(response)

