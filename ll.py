str="""
{'ok': {'10.0.0.143': {'command': {'changed': True, 
'end': '2019-03-27 05:17:22.770787', 'stdout': '/root', 
'cmd': 'pwd', 'rc': 0, 'start': '2019-03-27 05:17:22.767627', 
'stderr': '', 'delta': '0:00:00.003160', 
'invocation': {'module_args': 
{'creates': None, 'executable': None, '_uses_shell': True, '_raw_params': 'pwd', 
'removes': None, 'argv': None, 'warn': True, 'chdir': None, 'stdin': None}}, 
'_ansible_parsed': True, 'stdout_lines': ['/root'], 'stderr_lines': [], '_ansible_no_log': False}},
 '10.0.0.142': {'command': {'changed': True, 'end': '2019-03-27 05:17:22.793513', 'stdout': '/root', 'cmd': 'pwd', 'rc': 0, 'start': '2019-03-27 05:17:22.790558', 'stderr': '', 'delta': '0:00:00.002955', 'invocation': {'module_args': {'creates': None, 'executable': None, '_uses_shell': True, '_raw_params': 'pwd', 'removes': None, 'argv': None, 'warn': True, 'chdir': None, 'stdin': None}}, '_ansible_parsed': True, 'stdout_lines': ['/root'], 'stderr_lines': [], '_ansible_no_log': False}}}, 'failed': {}, 'unreachable': {}, 'skipped': {}}

"""
import pprint
pprint.pprint(str)