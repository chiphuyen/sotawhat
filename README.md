# sotawhat

This script runs using Python 3.

First, install the project using pip3. This script only requires ``nltk`` and ``six``.
Optionally, you can install the `[full]` version, which includes PyEnchant for spelling checks.

There are two ways to install it :

```bash
$ pip3 install .
```

```bash
$ pip3 install .[full]
```

If you run the error that the package ``punkt`` doesn't exist, this script will automatically download it for you.

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
$ sotawhat "[keyword]"
```

It also supports choosing the number of returned samples via arguments :

```bash
$ sotawhat "[keyword]" -c 10
$ sotawhat "[keyword]" --count 10  # same as above
```

You can also force exact name matches (if you are sure about spelling) by using the `--exact` flag.

```bash
$ sotawhat "[keyword]" -e
$ sotawhat "[keyword]" --exact
```

For example:

```bash
$ sotawhat "perplexity" --count 10 --exact
```

If you don't specify the number of results, by default, the script returns 5 results and doesnt perform exact matching.
Each result contains the title of the paper with author and published date, a summary of the abstract, and link to the paper.

We've found that this script works well with keywords that are:
+ a model (e.g. transformer, wavenet, ...)
+ a dataset (e.g. wikitext, imagenet, ...)
+ a task (e.g. 'language model', 'machine translation', 'fuzzing', ...)
+ a metric (e.g. BLEU, perplexity, ...)
+ random stuff
