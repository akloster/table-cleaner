FROM tabclean_docs
WORKDIR /usr/src/app/table-cleaner/docs
EXPOSE 8888
CMD bash -c "PYTHONPATH=/usr/src/app/table-cleaner:$PYTHONPATH ipython3 notebook --ip 0.0.0.0 --no-browser --log-level=DEBUG"
