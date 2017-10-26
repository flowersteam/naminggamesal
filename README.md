## Naming Games library in Python, for testing Active Learning strategies

branch master:
[![Build Status](https://travis-ci.org/flowersteam/naminggamesal.svg?branch=master)](https://travis-ci.org/flowersteam/naminggamesal)

branch develop:
[![Build Status](https://travis-ci.org/flowersteam/naminggamesal.svg?branch=develop)](https://travis-ci.org/flowersteam/naminggamesal)

Tests are done with both python 2 and 3.

#### This library is used in some scientific papers. 

The figures of the articles were this library is mentioned can be recomputed thanks to the jupyter notebooks that can be found also in this repository.

Because the structure of the library is continuously improved, those notebooks may not be compatible anymore with the current version of the code. However, they all correspond to a release version, and can be executed with the code version of the release.


#### You can install the library with the command:

`pip install -e git+https://github.com/flowersteam/naminggamesal.git@origin/develop#egg=naminggamesal`

You can change develop by master if you want the master branch, or any commit uuid.

Potential requirements (for debian like systems):
```
apt-get install python-dev liblzo2-dev liblzma-dev libsqlite3-dev python-tk
```

Other requirements may be necessary for scipy, numpy and matplotlib compilation:
```
apt-get install gcc gfortran python-dev libblas-dev liblapack-dev cython
```


