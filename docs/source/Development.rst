Development
===============

Currently, Table Cleaner is in a very early state of development. Python 3
support and documentation is marginal. Built-in validators are still very few.

For easier development a few Dockerfiles have been prepared and stored in the
docker/ subdirectory. Build these first. Then you can use "docker_test_py2.sh"
and "docker_test_py3.sh" in the top level directory to quickly and
reproducibly run the test suite.

This documentation can be generated with the "docker_make_html_docs.sh" script.

The directories with the Dockefiles each contain a build.sh script. These
scripts assign certain names to the containers, and these names are expected
by the other docker_* scripts to point to the respecting containers. In the
future this simple system may be refactored into a hierarchical container
structure, but for now, this is works quite well.

Feel free to send pull requests or discuss missing features in the Github
issue tracker for this project!


Future Plans
================

* Implement colored html table output to indicate errors
* Integrate Flanker email validation
* Add IP Address validators (as found in Django.core.validators)
* Elaborate Docker containers
* More Documentation

