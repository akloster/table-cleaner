
Tutorial
========

This tutorial will show you how to use the Table-Cleaner validation
framework.

First, let's import the necessary modules. My personal style is to
abbreviate the scientific python libraries with two letters. This avoids
namespace cluttering on the one hand, and is still reasonably short.

.. code:: python

    import numpy as np
    import pandas as pd
    from IPython import display
    import table_cleaner as tc
IPython.display provides us with the means to display Python objects in
a "rich" way, especially useful for tables.

Introduction
------------

Validating tabular data, especially from CSV or Excel files is a very
common task in data science and even generic programming. Many times
this data isn't "clean" enough for further processing. Writing custom
code to transform or clean up this kind of data quickly gets out of
hand.

Table-Cleaner is a framework to generalize this cleaning process.

Basic Example
-------------

First, let's create a DataFrame with messy data.

.. code:: python

    initial_df = pd.DataFrame(dict(name=["Alice", "Bob", "Wilhelm Alexander", 1, "Mary", "Andy"],
                                email=["alice@example.com", "bob@example.com", "blub", 4, "mary@example.com",
                                "andy k@example .com"],
                                x=[0,3.2,"5","hello", -3,11,],
                                y=[0.2,3.2,1.3,"hello",-3.0,11.0],
                                active=["Y", None, "T", "false", "no", "T"]
                                ))
    
    display.display(initial_df)


.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>active</th>
          <th>email</th>
          <th>name</th>
          <th>x</th>
          <th>y</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>     Y</td>
          <td>   alice@example.com</td>
          <td>             Alice</td>
          <td>     0</td>
          <td>   0.2</td>
        </tr>
        <tr>
          <th>1</th>
          <td>  None</td>
          <td>     bob@example.com</td>
          <td>               Bob</td>
          <td>   3.2</td>
          <td>   3.2</td>
        </tr>
        <tr>
          <th>2</th>
          <td>     T</td>
          <td>                blub</td>
          <td> Wilhelm Alexander</td>
          <td>     5</td>
          <td>   1.3</td>
        </tr>
        <tr>
          <th>3</th>
          <td> false</td>
          <td>                   4</td>
          <td>                 1</td>
          <td> hello</td>
          <td> hello</td>
        </tr>
        <tr>
          <th>4</th>
          <td>    no</td>
          <td>    mary@example.com</td>
          <td>              Mary</td>
          <td>    -3</td>
          <td>    -3</td>
        </tr>
        <tr>
          <th>5</th>
          <td>     T</td>
          <td> andy k@example .com</td>
          <td>              Andy</td>
          <td>    11</td>
          <td>    11</td>
        </tr>
      </tbody>
    </table>
    </div>


This dataframe contains several columns. Some of the cells don't look
much like the other cells in the same column. For Example we have
numbers in the email and name columns and strings in the number columns.

Looking at the dtypes assigned to the dataframe columns reveals a
further issue with this mess:

.. code:: python

    initial_df.dtypes



.. parsed-literal::

    active    object
    email     object
    name      object
    x         object
    y         object
    dtype: object



All columns are referred to as "object", which means they are saved as
individual Python objects, rather than strings, integers or floats. This
can make further processing inefficient, but also error prone, because
different Python objects may not work with certain dataframe
functionality.

Let's define a cleaner:

.. code:: python

    class MyCleaner(tc.Cleaner):
        name = tc.String(min_length=2, max_length=10)
        email = tc.Email()
        x = tc.Int(min_value=0, max_value=10)
        y = tc.Float64(min_value=0, max_value=10)
        active = tc.Bool()

Cleaner classes contain fields with validators.

The tc.String validator validates every input to a string. Because most
Python objects have some way of being represented as a string, this will
more often work than not. Pretty much the only failure reason is if the
string is encoded wrongly. Additionally, it can impose restrictions on
minimum and maximum string length.

The tc.Int instance tries to turn the input into integer objects. This
usually only works with numbers, or strings which look like integers.
Here, also, minimum and maximum values can be optionally specified.

The cleaner object can now validate the input dataframe like this:

.. code:: python

    cleaner = MyCleaner(initial_df)
Instantiating the cleaner class with an input dataframe creates a
cleaner instance with data and verdicts. The validation happens inside
the constructor.

.. code:: python

    cleaner.cleaned



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>active</th>
          <th>email</th>
          <th>name</th>
          <th>x</th>
          <th>y</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td> True</td>
          <td> alice@example.com</td>
          <td> Alice</td>
          <td> 0</td>
          <td> 0.2</td>
        </tr>
        <tr>
          <th>1</th>
          <td>  NaN</td>
          <td>   bob@example.com</td>
          <td>   Bob</td>
          <td> 3</td>
          <td> 3.2</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    cleaner.cleaned.dtypes



.. parsed-literal::

    active     object
    email      object
    name       object
    x           int64
    y         float64
    dtype: object



The DataFrame only contains completely valid rows, because the default
behavior is to delete any rows containing an error. See below on how to
use missing values instead.

The datatypes for the "x" column is now int64 instead of object. "y" is
now float64. Pandas uses the dtype system specified in numpy, and numpy
references strings as "object". The main reason for this is that numeric
data is usually stored in a contiguous way, meaning every value has the
same "width" of bytes in memory. Strings, not so much. Their size
varies. So arrays containing strings have to reference a string object
with a pointer. Then the array of pointers is contiguous with a fixed
number of bytes per pointer.

The "active" column is validated as a boolean field. There is a dtype
called bool, but it only allows True and False. If there are missing
values, the column reverts to "object". To force the bool dtype, read
the section about booleans below.

So far, we have ensured only valid data is in the output table. But
Table Cleaner can do more: The errors themselves can be treated as data:

.. code:: python

    cleaner.verdicts



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>column</th>
          <th>counter</th>
          <th>description</th>
          <th>reason</th>
          <th>valid</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td> active</td>
          <td>  0</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>0</th>
          <td>   name</td>
          <td>  1</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>0</th>
          <td>  email</td>
          <td>  2</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>0</th>
          <td>      x</td>
          <td>  3</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>0</th>
          <td>      y</td>
          <td>  4</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>1</th>
          <td> active</td>
          <td>  5</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>1</th>
          <td>   name</td>
          <td>  6</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>1</th>
          <td>  email</td>
          <td>  7</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>1</th>
          <td>      x</td>
          <td>  8</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>1</th>
          <td>      y</td>
          <td>  9</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>2</th>
          <td> active</td>
          <td> 10</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>2</th>
          <td>   name</td>
          <td> 11</td>
          <td> 'Wilhelm Alexander' has more than 10 characters</td>
          <td>                  too long</td>
          <td> False</td>
        </tr>
        <tr>
          <th>2</th>
          <td>  email</td>
          <td> 12</td>
          <td>  E-Mail addresses must contain one @ character.</td>
          <td>          email_without_at</td>
          <td> False</td>
        </tr>
        <tr>
          <th>2</th>
          <td>      x</td>
          <td> 13</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>2</th>
          <td>      y</td>
          <td> 14</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>3</th>
          <td> active</td>
          <td> 15</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>3</th>
          <td>   name</td>
          <td> 16</td>
          <td>                 '1' has fewer than 2 characters</td>
          <td>                 too short</td>
          <td> False</td>
        </tr>
        <tr>
          <th>3</th>
          <td>  email</td>
          <td> 17</td>
          <td>  E-Mail addresses must contain one @ character.</td>
          <td>          email_without_at</td>
          <td> False</td>
        </tr>
        <tr>
          <th>3</th>
          <td>      x</td>
          <td> 18</td>
          <td>            'hello' cannot be converted to int32</td>
          <td>             invalid int32</td>
          <td> False</td>
        </tr>
        <tr>
          <th>3</th>
          <td>      y</td>
          <td> 19</td>
          <td>          'hello' cannot be converted to float64</td>
          <td>           invalid float64</td>
          <td> False</td>
        </tr>
        <tr>
          <th>4</th>
          <td> active</td>
          <td> 20</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>4</th>
          <td>   name</td>
          <td> 21</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>4</th>
          <td>  email</td>
          <td> 22</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>4</th>
          <td>      x</td>
          <td> 23</td>
          <td>                              -3 is lower than 0</td>
          <td>             value too low</td>
          <td> False</td>
        </tr>
        <tr>
          <th>4</th>
          <td>      y</td>
          <td> 24</td>
          <td>                              -3 is lower than 0</td>
          <td>             value too low</td>
          <td> False</td>
        </tr>
        <tr>
          <th>5</th>
          <td> active</td>
          <td> 25</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>5</th>
          <td>   name</td>
          <td> 26</td>
          <td>                               undefined verdict</td>
          <td>                 undefined</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>5</th>
          <td>  email</td>
          <td> 27</td>
          <td> 'example .com' is not a valid email domain name</td>
          <td> email_domain_name_invalid</td>
          <td> False</td>
        </tr>
        <tr>
          <th>5</th>
          <td>  email</td>
          <td> 28</td>
          <td>         'andy k' is not a valid email user name</td>
          <td>   email_user_name_invalid</td>
          <td> False</td>
        </tr>
        <tr>
          <th>5</th>
          <td>      x</td>
          <td> 29</td>
          <td>                            11 is higher than 10</td>
          <td>            value too high</td>
          <td> False</td>
        </tr>
        <tr>
          <th>5</th>
          <td>      y</td>
          <td> 30</td>
          <td>                            11 is higher than 10</td>
          <td>            value too high</td>
          <td> False</td>
        </tr>
      </tbody>
    </table>
    </div>



In this case there is only one row per cell, or one per row and column.
Except for the last row, where there are two warnings/errors for the
Email column. In the current set of built-in validators this arises very
rarely. Just keep in mind not to sum the errors up naively and call it
the "number of invalid data points".

Let's filter the verdicts by validity:

.. code:: python

    errors = cleaner.verdicts[~cleaner.verdicts.valid]
    display.display(errors)


.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>column</th>
          <th>counter</th>
          <th>description</th>
          <th>reason</th>
          <th>valid</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2</th>
          <td>  name</td>
          <td> 11</td>
          <td> 'Wilhelm Alexander' has more than 10 characters</td>
          <td>                  too long</td>
          <td> False</td>
        </tr>
        <tr>
          <th>2</th>
          <td> email</td>
          <td> 12</td>
          <td>  E-Mail addresses must contain one @ character.</td>
          <td>          email_without_at</td>
          <td> False</td>
        </tr>
        <tr>
          <th>3</th>
          <td>  name</td>
          <td> 16</td>
          <td>                 '1' has fewer than 2 characters</td>
          <td>                 too short</td>
          <td> False</td>
        </tr>
        <tr>
          <th>3</th>
          <td> email</td>
          <td> 17</td>
          <td>  E-Mail addresses must contain one @ character.</td>
          <td>          email_without_at</td>
          <td> False</td>
        </tr>
        <tr>
          <th>3</th>
          <td>     x</td>
          <td> 18</td>
          <td>            'hello' cannot be converted to int32</td>
          <td>             invalid int32</td>
          <td> False</td>
        </tr>
        <tr>
          <th>3</th>
          <td>     y</td>
          <td> 19</td>
          <td>          'hello' cannot be converted to float64</td>
          <td>           invalid float64</td>
          <td> False</td>
        </tr>
        <tr>
          <th>4</th>
          <td>     x</td>
          <td> 23</td>
          <td>                              -3 is lower than 0</td>
          <td>             value too low</td>
          <td> False</td>
        </tr>
        <tr>
          <th>4</th>
          <td>     y</td>
          <td> 24</td>
          <td>                              -3 is lower than 0</td>
          <td>             value too low</td>
          <td> False</td>
        </tr>
        <tr>
          <th>5</th>
          <td> email</td>
          <td> 27</td>
          <td> 'example .com' is not a valid email domain name</td>
          <td> email_domain_name_invalid</td>
          <td> False</td>
        </tr>
        <tr>
          <th>5</th>
          <td> email</td>
          <td> 28</td>
          <td>         'andy k' is not a valid email user name</td>
          <td>   email_user_name_invalid</td>
          <td> False</td>
        </tr>
        <tr>
          <th>5</th>
          <td>     x</td>
          <td> 29</td>
          <td>                            11 is higher than 10</td>
          <td>            value too high</td>
          <td> False</td>
        </tr>
        <tr>
          <th>5</th>
          <td>     y</td>
          <td> 30</td>
          <td>                            11 is higher than 10</td>
          <td>            value too high</td>
          <td> False</td>
        </tr>
      </tbody>
    </table>
    </div>


As this is an ordinary DataFrame, we can do all the known shenanigans to
it, for example:

.. code:: python

    errors.groupby(["column", "reason"])["counter",].count()



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>counter</th>
        </tr>
        <tr>
          <th>column</th>
          <th>reason</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="3" valign="top">email</th>
          <th>email_domain_name_invalid</th>
          <td> 1</td>
        </tr>
        <tr>
          <th>email_user_name_invalid</th>
          <td> 1</td>
        </tr>
        <tr>
          <th>email_without_at</th>
          <td> 2</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">name</th>
          <th>too long</th>
          <td> 1</td>
        </tr>
        <tr>
          <th>too short</th>
          <td> 1</td>
        </tr>
        <tr>
          <th rowspan="3" valign="top">x</th>
          <th>invalid int32</th>
          <td> 1</td>
        </tr>
        <tr>
          <th>value too high</th>
          <td> 1</td>
        </tr>
        <tr>
          <th>value too low</th>
          <td> 1</td>
        </tr>
        <tr>
          <th rowspan="3" valign="top">y</th>
          <th>invalid float64</th>
          <td> 1</td>
        </tr>
        <tr>
          <th>value too high</th>
          <td> 1</td>
        </tr>
        <tr>
          <th>value too low</th>
          <td> 1</td>
        </tr>
      </tbody>
    </table>
    </div>



This functionality is the main reason why Table Cleaner was initially
written. In reproducible data science, it is important not only to
validate input data, but also be aware of, analyze and present the
errors present in the data.

Markup Frames
-------------

Let's bring some color into our tables. First, define some CSS styles
for the notebook, like so:

.. code:: python

    %%html
    <style>
    .tc-cell-invalid {
        background-color: #ff8080
    }
    .tc-highlight {
        color: red;
        font-weight: bold;
        margin: 3px solid black;
        background-color: #b0b0b0;
    }
    
    .tc-green {
        background-color: #80ff80
    }
    .tc-blue {
        background-color: #8080ff;
    }
    </style>


.. raw:: html

    <style>
    .tc-cell-invalid {
        background-color: #ff8080
    }
    .tc-highlight {
        color: red;
        font-weight: bold;
        margin: 3px solid black;
        background-color: #b0b0b0;
    }
    
    .tc-green {
        background-color: #80ff80
    }
    .tc-blue {
        background-color: #8080ff;
    }
    </style>


The MarkupFrame class is subclassed from Pandas' DataFrame class and is
used to manipulate and render cell-specific markup. It behaves almost
exactly the same as a DataFrame.

**Caution: This functionality will soon be completely rewritten to have
a simpler and cleaner API.**

It can be created from a validation like this:

.. code:: python

    mdf = tc.MarkupFrame.from_validation(initial_df, cleaner.verdicts)
    mdf



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table class="markup-table"><thead><th></th><th>active</th><th>email</th><th>name</th><th>x</th><th>y</th></thead><tbody><tr><th>0</th><td>Y</td><td>alice@example.com</td><td>Alice</td><td>0</td><td>0.2</td></tr><tr><th>1</th><td>None</td><td>bob@example.com</td><td>Bob</td><td>3.2</td><td>3.2</td></tr><tr><th>2</th><td>T</td><td class="tc-cell-invalid">blub</td><td class="tc-cell-invalid">Wilhelm Alexander</td><td>5</td><td>1.3</td></tr><tr><th>3</th><td>false</td><td class="tc-cell-invalid">4</td><td class="tc-cell-invalid">1</td><td class="tc-cell-invalid">hello</td><td class="tc-cell-invalid">hello</td></tr><tr><th>4</th><td>no</td><td>mary@example.com</td><td>Mary</td><td class="tc-cell-invalid">-3</td><td class="tc-cell-invalid">-3.0</td></tr><tr><th>5</th><td>T</td><td class="tc-cell-invalid tc-cell-invalid">andy k@example .com</td><td>Andy</td><td class="tc-cell-invalid">11</td><td class="tc-cell-invalid">11.0</td></tr></tbody></table>
    </div>



Note that we put in the initial\_df table, because the verdicts always
relate to the original dataframe, not the output, which has possibly
been altered and shortened during the validation process.

Now watch this:

.. code:: python

    mdf.x[1] += "tc-highlight"
    mdf.y += "tc-green"
    mdf.ix[0, :] += "tc-blue"
    mdf




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table class="markup-table"><thead><th></th><th>active</th><th>email</th><th>name</th><th>x</th><th>y</th></thead><tbody><tr><th>0</th><td class="tc-blue">Y</td><td class="tc-blue">alice@example.com</td><td class="tc-blue">Alice</td><td class="tc-blue">0</td><td class="tc-green tc-blue">0.2</td></tr><tr><th>1</th><td>None</td><td>bob@example.com</td><td>Bob</td><td class="tc-highlight">3.2</td><td class="tc-green">3.2</td></tr><tr><th>2</th><td>T</td><td class="tc-cell-invalid">blub</td><td class="tc-cell-invalid">Wilhelm Alexander</td><td>5</td><td class="tc-green">1.3</td></tr><tr><th>3</th><td>false</td><td class="tc-cell-invalid">4</td><td class="tc-cell-invalid">1</td><td class="tc-cell-invalid">hello</td><td class="tc-cell-invalid tc-green">hello</td></tr><tr><th>4</th><td>no</td><td>mary@example.com</td><td>Mary</td><td class="tc-cell-invalid">-3</td><td class="tc-cell-invalid tc-green">-3.0</td></tr><tr><th>5</th><td>T</td><td class="tc-cell-invalid tc-cell-invalid">andy k@example .com</td><td>Andy</td><td class="tc-cell-invalid">11</td><td class="tc-cell-invalid tc-green">11.0</td></tr></tbody></table>
    </div>



Booleans
--------

**The trouble with Booleans**

Boolean values are either True or False. In Pandas, and data science in
general, things are a bit more tricky. There is a third state, which
Pandas would refer to as a missing value. Numpy's Bool dtype does not
support missing values though.

.. code:: python

    np.bool(None)



.. parsed-literal::

    False



What's happening there is that many Python objects have a way of being
interpreted as either True or False. An empty list, empty strings, and
None, are all considered false, for example.

Now, let's try that in Pandas:

.. code:: python

    bools = pd.Series([True, False, None, np.NaN])
    bools



.. parsed-literal::

    0     True
    1    False
    2     None
    3      NaN
    dtype: object



The dtype is not "bool". Instead Pandas refers to the individual Python
object, and thus dtype must be "object". We can make it bool, though:

.. code:: python

    bools.astype(bool)



.. parsed-literal::

    0     True
    1    False
    2    False
    3     True
    dtype: bool



Notice how np.NaN, which is normally interpreted as a missing value, has
been converted to True?

If you try to index something with this sequence, this is what happens:

.. code:: python

    original = pd.Series(range(3))
    original[bools]

::


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-17-3d0782e602c7> in <module>()
          1 original = pd.Series(range(3))
    ----> 2 original[bools]
    

    /usr/local/lib/python3.4/site-packages/pandas/core/series.py in __getitem__(self, key)
        544             key = list(key)
        545 
    --> 546         if _is_bool_indexer(key):
        547             key = _check_bool_indexer(self.index, key)
        548 


    /usr/local/lib/python3.4/site-packages/pandas/core/common.py in _is_bool_indexer(key)
       2058             if not lib.is_bool_array(key):
       2059                 if isnull(key).any():
    -> 2060                     raise ValueError('cannot index with vector containing '
       2061                                      'NA / NaN values')
       2062                 return False


    ValueError: cannot index with vector containing NA / NaN values


Let's take a look at how to bring some sanity into this issue with Table
Cleaner. First, define a messy DataFrame, with columns that are
identical:

.. code:: python

    bools = [True, False, None, np.NaN]
    
    bool_df = pd.DataFrame(dict(a=bools, b=bools, c=bools, d=bools))
    bool_df



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>a</th>
          <th>b</th>
          <th>c</th>
          <th>d</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>  True</td>
          <td>  True</td>
          <td>  True</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>1</th>
          <td> False</td>
          <td> False</td>
          <td> False</td>
          <td> False</td>
        </tr>
        <tr>
          <th>2</th>
          <td>  None</td>
          <td>  None</td>
          <td>  None</td>
          <td>  None</td>
        </tr>
        <tr>
          <th>3</th>
          <td>   NaN</td>
          <td>   NaN</td>
          <td>   NaN</td>
          <td>   NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



Now create a cleaner which validates each column differently:

.. code:: python

    class BoolCleaner(tc.Cleaner):
        a = tc.Bool()
        b = tc.Bool(true_values=[True], false_values=[False], allow_nan=False)
        c = tc.Bool(true_values=[True], false_values=[False, None], allow_nan=False)
        d = tc.Bool(true_values=[True], false_values=[False, np.nan], nan_values=[None], allow_nan=False)
    
    bool_cleaner = BoolCleaner(bool_df)
    tc.MarkupFrame.from_validation(bool_df, bool_cleaner.verdicts)



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table class="markup-table"><thead><th></th><th>a</th><th>b</th><th>c</th><th>d</th></thead><tbody><tr><th>0</th><td>True</td><td>True</td><td>True</td><td>True</td></tr><tr><th>1</th><td>False</td><td>False</td><td>False</td><td>False</td></tr><tr><th>2</th><td>None</td><td class="tc-cell-invalid">None</td><td>None</td><td class="tc-cell-invalid">None</td></tr><tr><th>3</th><td>nan</td><td class="tc-cell-invalid">nan</td><td class="tc-cell-invalid">nan</td><td>nan</td></tr></tbody></table>
    </div>



Note that I used "delete=False" to keep rows with invalid data, while
still converting available values. Then this dataframe has the same
shape as MarkupFrame.from\_validation expects. "allow\_nan" defaults to
True and controls whether or not missing values are considered an error.

.. code:: python

    bool_cleaner.verdicts[~bool_cleaner.verdicts.valid]



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>column</th>
          <th>counter</th>
          <th>description</th>
          <th>reason</th>
          <th>valid</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2</th>
          <td> d</td>
          <td>  9</td>
          <td> None cannot be converted to True or False.</td>
          <td> bool_nan_not_allowed</td>
          <td> False</td>
        </tr>
        <tr>
          <th>2</th>
          <td> b</td>
          <td> 10</td>
          <td> None cannot be converted to True or False.</td>
          <td> bool_nan_not_allowed</td>
          <td> False</td>
        </tr>
        <tr>
          <th>3</th>
          <td> b</td>
          <td> 14</td>
          <td>  nan cannot be converted to True or False.</td>
          <td> bool_nan_not_allowed</td>
          <td> False</td>
        </tr>
        <tr>
          <th>3</th>
          <td> c</td>
          <td> 15</td>
          <td>  nan cannot be converted to True or False.</td>
          <td> bool_nan_not_allowed</td>
          <td> False</td>
        </tr>
      </tbody>
    </table>
    </div>



Tables coming from external sources, especially spreadsheet data is
notorious for having all sorts of ways to indicate booleans or missing
values. The Bool validator takes three arguments to handle these cases:
true\_values, false\_values and nan\_values.

.. code:: python

    messy_bools_column =["T","t","on","yes", "No", "F"]
    messy_bools = pd.DataFrame(dict(a=messy_bools_column, b=messy_bools_column))
.. code:: python

    class BoolCleaner2(tc.Cleaner):
        a=tc.Bool()
        b=tc.Bool(true_values=["T"], false_values=["F"], allow_nan=False)
    
    bool_cleaner2 = BoolCleaner2(messy_bools)
    tc.MarkupFrame.from_validation(messy_bools, bool_cleaner2.verdicts)



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table class="markup-table"><thead><th></th><th>a</th><th>b</th></thead><tbody><tr><th>0</th><td>T</td><td>T</td></tr><tr><th>1</th><td>t</td><td class="tc-cell-invalid">t</td></tr><tr><th>2</th><td>on</td><td class="tc-cell-invalid">on</td></tr><tr><th>3</th><td>yes</td><td class="tc-cell-invalid">yes</td></tr><tr><th>4</th><td>No</td><td class="tc-cell-invalid">No</td></tr><tr><th>5</th><td>F</td><td>F</td></tr></tbody></table>
    </div>



Email validation
================

Email validation is a subject onto its own. Some frameworks offer
validation by simple regular expressions, which sometimes isn't enough.
Other libraries or programs go so far as to ask the corresponding mail
server if it knows a particular address.

In almost all generic usecases, you expect email names to adhere to a
very specific form, meaning a username "at" a particular globally
identifiable domain name. It is assumed that every computer in the world
can resolve this domain name to the same physical server. Email
standards and most eail servers however, don't require "fully qualified
domain names" or even globally resolvable domains. "root@localhost" is a
perfectly valid email address, but completely useless in most
circumstances where you want to collect or use email addresses.

TableCleaner's Email validator class is based on Django's validation
method.

.. code:: python

    messy_emails =["alice@example.com", "bob@bob.com", "chris", "delta@localhost", "ernest@hemmingway@ernest.org", "fridolin@dev_server"]
    email_df = pd.DataFrame(dict(email=messy_emails))
    class EmailCleaner(tc.Cleaner):
        email = tc.Email()
        
    email_cleaner = EmailCleaner(email_df)
    tc.MarkupFrame.from_validation(email_df, email_cleaner.verdicts)



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table class="markup-table"><thead><th></th><th>email</th></thead><tbody><tr><th>0</th><td>alice@example.com</td></tr><tr><th>1</th><td>bob@bob.com</td></tr><tr><th>2</th><td class="tc-cell-invalid">chris</td></tr><tr><th>3</th><td>delta@localhost</td></tr><tr><th>4</th><td class="tc-cell-invalid tc-cell-invalid">ernest@hemmingway@ernest.org</td></tr><tr><th>5</th><td class="tc-cell-invalid">fridolin@dev_server</td></tr></tbody></table>
    </div>


