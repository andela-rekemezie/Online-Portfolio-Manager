from setuptools import setup

setup(name='Portfolio',
      version='1.0',
      description='Application to allow users to create their online CV',
      author='Rowland Ekemezie',
      author_email='rowland.ekemezie@andela.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=[
          'Flask==0.11.1',
          'MarkupSafe',
          'SQLAlchemy>=0.8.0',
          'Flask-SQLAlchemy==2.1',
          'Flask-Login==0.3.2',
          'Flask-WTF==0.12'
      ],
      )
