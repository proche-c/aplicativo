from setuptools import setup, find_packages

setup(
    name='claimer',
    version='1.0',
    description="""Claimer is a programm that processes the information of the 
    receipts from an excel file genarated by the program Elevia and generated an 
    excel file with statistical information as well as desviations between agreed 
    and paid commissions.""",
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    scripts=['claim.py'],
    install_requires=[paquete.strip()
                      for paquete in open("requirements.txt").readlines()]
)