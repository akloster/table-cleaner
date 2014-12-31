#!/bin/bash
docker run -p 8888:8888 -v /home/andi/oss/table-cleaner:/usr/src/app/table-cleaner -ti tabclean_notebook
