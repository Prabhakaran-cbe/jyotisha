JyotiSha tools
==============
# For users
For detailed examples and help, please see individual module files in this package.

## Installation or upgrade:
* `sudo pip install jyotisha -U`
* `sudo pip install git+https://github.com/sanskrit-coders/jyotisha/@master -U`
* [Web](https://pypi.python.org/pypi/jyotisha).

## Usage
- Please see the generated python sphynx docs in one of the following places:
    - http://jyotisha.readthedocs.io [Broken as of 20170828.]
    - [project page](https://sanskrit-coders.github.io/jyotisha/build/html/jyotisha.html).
    - under docs/_build/html/index.html

# For contributors
## Contact
Have a problem or question? Please head to [github](https://github.com/sanskrit-coders/jyotisha).

## Packaging
* ~/.pypirc should have your pypi login credentials.
```
python setup.py bdist_wheel
twine upload dist/* --skip-existing
```

## Document generation
- Sphynx html docs can be generated with `cd docs; make html` Current errors:
  - Can't find xsanscript. indic_transliteration package must be updated.
- http://jyotisha.readthedocs.io/en/latest/jyotisha.html should automatically have good updated documentation - unless there are build errors. Current build errors:
  - indic_transliteration cannot be installed. [Stackexchange question](https://stackoverflow.com/questions/45929148/read-the-docs-pip-pypi-dependency-installation-error).
