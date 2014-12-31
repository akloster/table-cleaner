FROM python:3-onbuild
ENV SPHINXBUILD sphinx-build
RUN apt-get update
RUN apt-get install -y pandoc 
WORKDIR /usr/src/app/table-cleaner/docs
