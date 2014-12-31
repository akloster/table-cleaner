#!/bin/bash
docker run -v /home/andi/oss/table-cleaner:/usr/src/app/table-cleaner tabclean_docs /bin/bash -c "make html"
