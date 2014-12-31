# table-cleaner

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/akloster/table-cleaner?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

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

This software is very young, the APIs may change. If you'd like to make
suggestions, feel free to post them to the Issues in Github, or
join the chatroom at https://gitter.im/akloster/table-cleaner
