.. Table-Cleaner documentation master file, created by
   sphinx-quickstart on Thu Dec 25 09:03:30 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Table-Cleaner
=========================================

Introduction
____________

Table-Cleaner is a validation framework for tabular data in the Pandas
ecosystem. It can be used to validate data inside DataFrames and returns the
cleaned data and information about errors as DataFrames for further processing.

Such data may come from CSV or Excel files. Using built-in and custom
validators Table-Cleaner can be used to ensure data integrity.

DataFrames with information about the errors in such a table can then be used in
documentation or web applications, or it can be further analyzed using the
usual Pandas and scientific Python tools.

Table-Cleaner is largely inspired by the Django validators, which are used in
forms, among other things.


Contents:

.. toctree::
   :maxdepth: 2

   Tutorial
   Development


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

