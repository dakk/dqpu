# Contributing

## Bug report and feature suggestion

If you have found an issue with dqpu, first do a search in the [dqpu issue tracker](https://github.com/dakk/dqpu/issues) to ensure that there are no existing issues with
similar content. If you can't find another related issue, open a new one: please try to be as detailed as possible.


## Submit a pull request

If you want to contribute to dqpu, you have to follow this flow:

1. First fork the [dqpu repository](https://github.com/dakk/dqpu) so you can work on your copy of the code
2. Clone it locally by running ```git clone https://github.com/YOUR_USERNAME/dqpu.git```
3. Add the original repo as upstream ```git remote add upstream https://github.com/dakk/dqpu.git```

We also suggest to use `pyenv` to create an isolated pip environment:

- Create a new env: ```pyenv virtualenv dqpu-env```
- Activate it: ```pyenv activate dqpu-env```


### Working on the code

1. Now that you have your local copy of dqpu, you can start working on the code; first, search or create the issue you want to contribute to in the dqpu issue tracker, and ask
to be assigned to that issue in order to avoid duplicate work.

2. Create e new branch with a descriptibe name where you will do the changes; the starting point is always upstream/main:

```bash
git fetch upstream
git checkout -b your-branch-name upstream/master
```

3. Before each commit, use tox (```pip install tox```) in order to check that typechecker, linters and tests run fine:

```tox```

Use short and descriptive commit message, and remember to add tests to check new functionalities.


4. If your branch drifts out of sync from upstream/main, you can fetch and merge the updated version:

```git pull upstream main```

5. Finally push your code in your branch

```git push origin your-branch-name```

6. Once you're happy with your changes, visit [dqpu github](https://github.com/dakk/dqpu) and start a new pull request from `USERNAME:your-branch-name` to `dakk:main`. Maintainers will start reviewing your code and they may ask you to do some changes (in your branch): PR updates automatically every time you push to your working branch.


### Make docs

You can also create docs locally in order to check if everything is as expected:

```bash
pip install sphinx sphinx_rtd_theme sphinx_rtd_dark_mode myst_nb
cd docs
make html
```


## Publish a new release (maintainers only)

1. Update dqpu version in `dqpu/__init__.py`

2. Create a new tag and a new release on github

3. Submit the release on pypi using twine:


```bash
python setup.py sdist bdist
python -m twine upload dist/*
```