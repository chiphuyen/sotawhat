# sotawhat

This script runs using Python 3.

First, install the required packages. This script only requires ``nltk`` and ``PyEnchant``.

```bash
$ pip3 install -r requirements.txt
```

If you run the error that the package ``punkt`` doesn't exist, download it by going into your Python environment and running:

```bash
$ python3

>>> import nltk
>>> nltk.download('punkt')
```

To query for a certain keyword, run:

```bash
$ python3 sotawhat.py "[keyword]" [number of results]
```

For example:

```bash
$ python3 sotawhat.py "perplexity" 10
```

If you don't specify the number of results, by default, the script returns 5 results. Each result contains the title of the paper with author and published date, a summary of the abstract, and link to the paper.

We've found that this script works well with keywords that are:
+ a model (e.g. transformer, wavenet, ...)
+ a dataset (e.g. wikitext, imagenet, ...)
+ a task (e.g. 'language model', 'machine translation', 'fuzzing', ...)
+ a metric (e.g. BLEU, perplexity, ...)
+ random stuff
