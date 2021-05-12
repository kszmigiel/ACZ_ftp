import os
from ftplib import FTP
from cmd import Cmd


class FtpInterpreter(Cmd):
    """pro
    FTP client command line utility.
    """
    def __init__(self):
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

    def do_open(self, host):
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

    def do_ls(self, *args):
        response = self._perform_ftp_command('dir')
        print(response)

    def do_mls(self, path):
        response = self._perform_ftp_command('mlsd', path)
        print(response)

    def do_nlist(self, path):
        response = self._perform_ftp_command('nlst', path)
        print(response)

    def do_cd(self, path):
        response = self._perform_ftp_command('cwd', path)
        print(response)

    def do_mkdir(self, dir_name):
        response = self._perform_ftp_command('mkd', dir_name)
        print(response)

    def do_rmdir(self, dir_name):
        response = self._perform_ftp_command('rmd', dir_name)
        print(response)

    def do_size(self, filename):
        response = self._perform_ftp_command('size', filename)
        print(response)

    def do_delete(self, filename):
        response = self._perform_ftp_command('delete', filename)
        print(response)

    def do_get(self, filename):
        with open(filename, 'wb') as fp:
            response = self._perform_ftp_command('retrbinary', 'RETR '+filename, fp.write)
        print(response)

    def do_put(self, filename):
        with open(filename, 'rb') as fp:
            response = self._perform_ftp_command('storbinary', 'STOR '+filename, fp)