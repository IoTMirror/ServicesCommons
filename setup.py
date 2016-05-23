from setuptools import setup

setup(name='iotmirror_commons',
      version='0.3',
      description='Common files for IoTMirror Web Services',
      url='https://github.com/IoTMirror/ServicesCommons',
      packages=['iotmirror_commons'],
      install_requires=['psycopg2', 'oauth2client', 'Flask']
     )
