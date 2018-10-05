from setuptools import setup, find_packages
import sotawhat

setup(
    name='sotawhat',
    version=str(sotawhat.__VERSION__),
    packages=find_packages(),
    description='arxiv-sanity query script',
    long_description=str('I often get frustrated searching for the latest '
                         'research results on Google and Arxiv so I wrote '
                         'SOTAwhat, a script to query Arxiv for the latest '
                         'abstracts and extract summaries from them. '),
    url='https://huyenchip.com/2018/10/04/sotawhat.html',
    license="",
    install_requires=['six', 'nltk'],
    extras_require={
        'full': ['PyEnchant'],
    },
    entry_points={
        'console_scripts': ['sotawhat=sotawhat.cmd_line:main'],
    }
)
