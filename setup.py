from setuptools import setup

setup(name='Portfolio',
      version='1.0',
      description='Application to allow users to create their online CV',
      author='Rowland Ekemezie',
      author_email='rowland.ekemezie@andela.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=[
          'Flask',
          'Flask-SQLAlchemy',
          'Flask-Login',
          'Flask-WTF'
      ],
      )
