TaxonLinker
===========

TaxonLinker is a simple tool that addresses the problem of integrating biological information from different sources using the scientific name as the linking code. It has been implemented in Python, using Tkinter for the interface, and will therefore work on any computer with a standard Python installation.

TaxonLinker addresses two common problems associated with biological data integration. Firstly, data has often been entered by hand, and many records will not match because of spelling or formatting differences. By making use of Python's difflib library, TaxonLinker can match taxa despite differences in spelling. In the case of very minor differences, the match is automatic. If the difference is more substantial, the user is provided with a list of most likely matches to choose from.

Secondly, the imported data might make use of a different taxonomy. To deal with this, the dictionary can optionally include information on synonomy. This enables TaxonLinker to automatically link the data to the current name rather than the synonym.

TaxonLinker works with csv text files, and the output file is simply a match between the taxon name in the input file, and the taxon name or taxon identifier in your database. The process of linking the related data is up to the user.

Installation
------------

As mentioned, TaxonLinker needs a working Python installation to run. If you do not have Python on your system already, you can download it from http://www.python.org/download/releases/. If there are no other compelling reasons for choosing a particular version, the highest 2.7.x version is recommended. TaxonLinker should work in Python 2.7 and 2.6 (though it hasn't been tested in the latter). It will not work on 3.x without some simple modification.

TaxonLinker does not need to be installed anywhere in particular, and will run quite happily from your Desktop, a USB drive or any other folder on your hard drive. Simply copy or unzip the files to a place of your liking, e.g. a `TaxonLinker` folder on your Desktop.

The basic configuration should be fine for most uses, but you can edit the options in settings.py file to better suit your requirements.

Setting up your taxon dictionary
--------------------------------

TaxonLinker requires a taxon dictionary to match input names against. At a minimum this requires the set of names that your database knows about, or that you are interested in importing data for. The names should ideally be in the same format as those in the data that you are importing. For example, if the names in the imported data use the format *Genus species subsp. subspecies*, the matches will be more accurate if your data also includes '*subsp.*'.

Your dictionary file must be a text file in `csv format`_, preferably using tabs as field separators (although you can change this in `settings.py`). If the file is saved as `TaxonIndex.txt` in the `var` directory under `TaxonLinker`, it will be loaded automatically at startup. You can also load a dictionary using the `Load Dictionary` button while the program is running.

TaxonLinker uses the column headers to process the information in your dictionary file, so these need to be included as the first line of the file. TaxonLinker can handle `scientificName`, `taxonID`, `taxonomicStatus`, and `relatedResourceID` as field names, though only `scientificName` is required. These names are taken from the `Darwin Core`_ vocabulary for the purpose of interoperability.

The following table shows a dictionary containing only `scientificName`:

+-----------------------------+
|       scientificName        |
+=============================+
| Thalassarche chlororhynchos |
+-----------------------------+
| Thalassarche melanophrys    |
+-----------------------------+
| Thalassarche bulleri        |
+-----------------------------+
| Thalassarche eremita        |
+-----------------------------+
| ...                         |
+-----------------------------+

You can also add identifiers, so that the output file links directly to your data rather than having to match the names first:

+-----------------------------+-----------+
|       scientificName        |  taxonID  |
+=============================+===========+
| Thalassarche chlororhynchos |  14       |
+-----------------------------+-----------+
| Thalassarche melanophrys    |  12       |
+-----------------------------+-----------+
| Thalassarche bulleri        |  14.2     |
+-----------------------------+-----------+
| Thalassarche eremita        |  11.2     |
+-----------------------------+-----------+
| ...                         |  ...      |
+-----------------------------+-----------+

Note that you can have multiple forms of a taxon name in your dictionary, if you are not sure of the input data and want to match all possibilities. You would need to use the same taxonID for this to work:

+-----------------------------------------------------+-----------+
|       scientificName                                |  taxonID  |
+=====================================================+===========+
| Acacia koa A.Gray var. latifolia (Benth.) H.St.John |  123-4    |
+-----------------------------------------------------+-----------+
| Acacia koa var. latifolia                           |  123-4    |
+-----------------------------------------------------+-----------+
| Anas undulata subsp. undulata                       |  151a     |
+-----------------------------------------------------+-----------+
| Anas undulata                                       |  151a     |
+-----------------------------------------------------+-----------+
| ...                                                 |  ...      |
+-----------------------------------------------------+-----------+

If you have information on the synonomy of your names, TaxonLinker can help you to link to the current name rather than a synonym. In order to achieve this, you need to use the `taxonomicStatus` and `relatedResourceID` fields. The `taxonID` field has been omitted in this example, but it will work just as well with it included. You would then have a `taxonID` entry in the `relatedResourceID` column instead of a `scientificName` as it is here. The `taxonomicStatus` field can contain entries of `valid`, `accepted` or `synonym`. Anything else (including blank entries) are assumed to be not current.

+-----------------------------+-------------------+----------------------+
|       scientificName        |  taxonomicStatus  |  relatedResourceID   |
+=============================+===================+======================+
| Thalassarche chlororhynchos | valid             |                      |
+-----------------------------+-------------------+----------------------+
| Thalassarche melanophrys    | synonym           | Thalassarche eremita |
+-----------------------------+-------------------+----------------------+
| Thalassarche bulleri        |                   |                      |
+-----------------------------+-------------------+----------------------+
| Thalassarche eremita        | valid             |                      |
+-----------------------------+-------------------+----------------------+
| ...                         | ...               | ...                  |
+-----------------------------+-------------------+----------------------+

It's easiest to set up your dictionary in a spreadsheet (such as Microsoft Excel) and save it in csv format. Be sure to specify that it should use tab as a field separator, and should not use any text delimiters. There are some small example files in the `test` directory that you can edit to create your own dictionary.

.. _csv format: http://en.wikipedia.org/wiki/Comma-separated_values
.. _Darwin Core: http://rs.tdwg.org/dwc/terms/index.htm

Using TaxonLinker
-----------------

To run TaxonLinker, you should be able to double-click the taxonlinker.py file in the `TaxonLinker` folder [1]_. This will load the program interface.

Load Dictionary: 
    Use this button to load a different dictionary from the 
    default one. If there is no file called TaxonDictionary.txt
    in the `var` directry of `TaxonLinker`, you will have to load
    a dictionary before you can process any names. You can also
    change your dictionary while processing a batch of names. Any
    names processed subsequently will use the new dictionary.

Load Names: 
    Use this button to load a text file containing the names of the
    taxa you are interested in importing. It should contain names only,
    and should not have any headers. It is not modified in any way by
    Taxon Linker.

Select correct taxon: 
    If Taxon Linker is not sure of the match for a 
    particular name, it will populate this window with a list
    of possible matches. Within this list, synonyms will be
    indicated with '=', and names which are not current will
    be indicated by a '*' before the taxon name. If no
    synonomy information is available, the taxon name will
    be shown without any embellishments.
                       
Check Updated Name: 
    If the select options shown are not correct, you can edit
    the name directly, and refresh the options using this
    button. This can be useful for gross misspellings or when
    the synonomy is not loaded or not up to date.

Save: 
    If the correct matching taxon is listed in the select window, you can
    choose it by clicking on it, and then save it by pressing this button.
    If the first option is the correct one, you can simply click the `Save`
    button. This button will only be enabled when there is both a dictionary
    and a list of names loaded.

Skip: 
    If there is no similar record in your database to the one being checked,
    it will not show up in the list of options. You can then move on to the
    next record using the `Skip` button. This button will only be enabled
    when there is both a dictionary and list of names loaded.

If you close the program before finishing the batch of names, it will save your current batch to a temporary file, and will automatically load it when Taxon Linker starts again.

.. [1] On Windows, if this doesn't work, you may need to set up your environment variables. See The Python_ documentation for additional instructions.
.. _Python: http://docs.python.org/using/windows.html#excursus-setting-environment-variables for instructions.

Output files
------------

MatchedNames.txt:
    This is the main output file that Taxon Linker produces, and
    is saved in the same directory as the program executable. It
    contains a tab-separated list of the taxon names in the
    input file and either the matching names or related id in the
    dictionary.

NotValid.txt:
    This file contains names which have been saved but which are not 
    current, and do not have synonyms indicated. It is provided as a
    convenience as these may need individual processing to integrate.
    It is also saved in the base directory.

skipped.txt:
    This file, saved in the `log` directory, serves as a record of
    names that have been skipped, either because the user pressed the
    `Skip` button, or because the algorithm could not find a genus
    that was a likely match. The skipped files are logged so that the
    user can pick up any anomalies, or reprocess the list after making
    some edits.

automatch.txt: 
    This file contains a log of names that were matched
    automatically by the system without user intervention. It is
    provided for the user to pick up any false matches (although
    this would happen rarely, if at all). It is saved in the `log`
    directory.

Changes and license
-------------------
TaxonLinker is free software released under the terms of the MIT license available in the accompanying LICENSE file. The current version is 0.8.0. You can find a more detailed list of changes in the CHANGES file.

