from setuptools import setup, find_packages
import sotawhat

setup(
    name='sotawhat',
    version=str(sotawhat.__VERSION__),
    packages=find_packages(),
    description='arxiv-sanity query script',
    long_description=str('SOTAwhat is a script to query Arxiv for the latest '
                         'abstracts and extract summaries from them. '),
    url='https://huyenchip.com/2018/10/04/sotawhat.html',
    license="",
    install_requires=['six', 'nltk', 'pyspellchecker', 'PyPDF2', 'openai'],
    entry_points={
        'console_scripts': ['sotawhat=sotawhat.sotawhat:main'],
    }
)
