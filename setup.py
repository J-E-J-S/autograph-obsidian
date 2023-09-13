from setuptools import setup, find_packages
exec(open('autographObsidian/__init__.py').read())

DESCRIPTION = 'Automatic knowledge graph generation.'
LONG_DESCRIPTION = 'Make graphs for obsidian.md through mining scientific literature.'

# Setting up
setup(
        name="autograph-obsidian",
        version= __version__ ,
        author="James Sanders",
        author_email="james.sanders1711@gmail.com",
        url = 'https://github.com/J-E-J-S/autograph-obsidian',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'click==7.1.2', 
            'pygetpapers==1.2.5'
        ],
        entry_points = {
            'console_scripts':['autograph=autographObsidian.autograph:cli']
        }
)
