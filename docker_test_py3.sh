#!/bin/bash
docker run -v ${PWD}:/usr/src/app/table-cleaner -ti tabclean_py3 nosetests

