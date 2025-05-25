from setuptools import setup, find_packages
import re
import os

def derive_version() -> str:
    try:
        with open(os.path.join('discordself', '__init__.py'), 'r', encoding='utf-8') as f:
            version = re.search(
                r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                f.read(),
                re.MULTILINE
            ).group(1)
    except Exception as e:
        raise RuntimeError(f'Failed to get version: {e}')

    if not version:
        raise RuntimeError('Version is not set in __init__.py')

    if version.endswith(('a', 'b', 'rc')):
        try:
            import subprocess
            # Добавляем количество коммитов
            result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                capture_output=True,
                text=True
            )
            if result.stdout:
                version += result.stdout.strip()
            
            # Добавляем короткий хэш коммита
            result = subprocess.run(
                ['git', 'rev-parse', '--short', 'HEAD'],
                capture_output=True,
                text=True
            )
            if result.stdout:
                version += '+g' + result.stdout.strip()
        except Exception:
            pass

    return version

setup(
    name='discord.py-self',
    version=derive_version(),
    packages=['discordself'],
    package_dir={'discordself': 'discordself'},
    install_requires=[
        'aiohttp>=3.7.4',
        'typing-extensions>=4.3.0',
    ],
    python_requires='>=3.8',
    author='Petrix',
    description='Discord.py self-bot fork',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/petrixgxd/discord.py-self',
)
