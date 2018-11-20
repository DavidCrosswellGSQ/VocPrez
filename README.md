# SKOS Styler
Simple Knowledge Organization System (SKOS) read-only web delivery system.

This tool is a SKOS-specific, specialised, implementation of the [pyLDAPI](https://github.com/rdflib/pyLDAPI). pyLDAPI is a generic tool for the deliver of [RDF](https://www.w3.org/RDF/) data online in both human- and machine-readable formats. pyLDAPI needs deployment-specific templates for registers & classes that present the data of interest in that deployment. SKOS Styler is pre-configured with templates for SKOS' core data classes - `ConceptScheme`, `Collection` & `Concept` - and registers of them.

Since this tool is preconfigured for SKOS data, it is ready for use with SKSO-only vocabularies. Forks of this codebase can be made to enhance it for SKOS+ features. SKOS+ is a general term for SKOS data *plus some other bits*.


## API & Templates
As per other pyLDAPI deployments, this tool uses the [Jinja2 Python templating engine](http://jinja.pocoo.org/) to generate HTML and other files which are called fro use through Python's [Flask](http://flask.pocoo.org/), a small HTTP framework.

Standard templates for `ConceptScheme`, `Collection`, `Concept` & `Register` are contained within this repository, as is a Model-View-Controller-style depolyment of Flask, pre-configures for SKOS.


## Installation
* follow the instructions as per pyLDAPI (see [its documentation]())
* ensure your config file is correct
    * you need to copy the file `_config/template.py` to `_config/__init__.py` and configure carables within it. See the template.py` file for examples
* configure your data source
    * you will need to supply this tool with SKOS data from any sort of data source: a triplestore, a relational database or even a test file
    * see the [DATA_SOURCES.md](https://github.com/CSIRO-enviro-informatics/skos-styler/examples/DATA_SOURCES.md) file for examples


## Dependencies
See the [requirements.txt](https://github.com/CSIRO-enviro-informatics/skos-styler/requirements.txt) standard Python dependency listing file.


## License
The content of this API is licensed for use under the [Creative Commons 4.0 License](https://creativecommons.org/licenses/by/4.0/). See the [license deed](LICENSE) all details.


## Contacts
*Author*:<br />
**Nicholas Car**<br />
*Senior Experimental Scientist*<br />
CSIRO Land & Water, Environmental Informatics Group<br />
<nicholas.car@csiro.au>