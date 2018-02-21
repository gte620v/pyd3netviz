"""pyd3netviz"""

from setuptools import setup

setup(
    name='pyd3netviz',
    packages=['pyd3netviz'],
    package_data={
        'pyd3netviz': ['js/*.js'],
    },
    version='0.1.2',
    description='Simple wrapper around d3 force graph for python and Jupyter Notebooks',
    author='Bob Baxley',
    author_email='bob.baxley@gmail.com',
    license='MIT',
    url='https://github.com/gte620v/pyd3netviz',
    keywords=['network graph', 'd3js', 'visualization',
              'force layout', 'Jupyter Notebook'],
    classifiers=[],
    install_requires=['pyperclip==1.5.27', 'networkx==2.1', ],
)
