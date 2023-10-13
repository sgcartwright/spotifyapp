# Setup program to ensure all proper packages are installed


from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'html5lib',
    'requests',
    'requests_html',
    'beautifulsoup4',
    'youtube_dl',
    'pathlib',
    'pandas'
]

setup(
    name='PlaylistRadioGenerator',
    version='1.0',
    description='An application that creates Spotify Playlist Radios',
    author='Steven Cartwright',
    author_email='stevencartwright',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)