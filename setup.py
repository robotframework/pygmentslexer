from setuptools import setup


entry_points = '''
[pygments.lexers]
robotframework = robotframeworklexer:RobotFrameworkLexer
'''

setup(
    name         = 'robotframeworklexer',
    version      = '0.0.1',
    description  = __doc__,
    py_modules   = ['robotframeworklexer'],
    entry_points = entry_points

)
