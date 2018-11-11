# sotawhat

Read more about SOTAWHAT [here](https://huyenchip.com/2018/10/04/sotawhat.html).

You can use sotawhat through a web interface [here](https://sotawhat.herokuapp.com/#/). Thanks hmchuong!

This script runs using Python 3. It requires ``nltk``, ``six``, and ``pyspellchecker``. To install it as a Python package, follow the following steps:


Step 1: clone this repo, and go inside that repo:
```bash
$ git clone [HTTPS or SSH linnk to this repo]
$ cd sotawhat
```
Step 2: install using pip

```bash
$ pip3 install .
```

On Windows, due to encoding errors, the script may cause issues when run on the command line. It is
recommended to use `pip install win-unicode-console --upgrade` prior to launching the script. If you get
UnicodeEncodingError, you *must* install the above.

In MacOS, you can get the SSL error

```
[nltk_data] Error loading punkt: <urlopen error [SSL:
[nltk_data]     CERTIFICATE_VERIFY_FAILED] certificate verify failed:
[nltk_data]     unable to get local issuer certificate (_ssl.c:1045)>
```

this will be fixed by reinstalling certificates
```shell
$ /Applications/Python\ 3.x/Install\ Certificates.command
```

# Usage
This project adds the `sotawhat` script for you to run globally on Terminal or commandline.

To query for a certain keyword, run:

```bash
$ sotawhat [keyword] [number of results]
```

For example:

```bash
$ sotawhat perplexity 10
```

or 

```bash
$ sotawhat language model 10
```

If you don't specify the number of results, by default, the script returns 5 results. Each result contains the title of the paper with author and published date, a summary of the abstract, and link to the paper.

We've found that this script works well with keywords that are:
+ a model (e.g. transformer, wavenet, ...)
+ a dataset (e.g. wikitext, imagenet, ...)
+ a task (e.g. language model, machine translation, fuzzing, ...)
+ a metric (e.g. BLEU, perplexity, ...)
+ random stuff
