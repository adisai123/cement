"""Tests for cement.utils.shell"""

from cement.utils import shell, test

class ShellUtilsTestCase(test.CementTestCase):
    def test_exec_cmd(self):
        out, err, ret = shell.exec_cmd(['echo', 'KAPLA!'])
        self.eq(ret, 0)
        self.eq(out, b'KAPLA!\n')
        
    def test_exec_cmd_shell_true(self):
        out, err, ret = shell.exec_cmd(['echo KAPLA!'], shell=True)
        self.eq(ret, 0)
        self.eq(out, b'KAPLA!\n')
        
    def test_exec_cmd2(self):
        ret = shell.exec_cmd2(['echo'])
        self.eq(ret, 0)
        
    def test_exec_cmd2_shell_true(self):
        ret = shell.exec_cmd2(['echo johnny'], shell=True)
        self.eq(ret, 0)
    
    def test_exec_cmd_bad_command(self):
        out, err, ret = shell.exec_cmd(['false'])
        self.eq(ret, 1)
    
    def test_exec_cmd2_bad_command(self):
        ret = shell.exec_cmd2(['false'])
        self.eq(ret, 1)