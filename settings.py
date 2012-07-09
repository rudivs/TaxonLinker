# name matching parameters
PERFECT_CUTOFF = 0.95  # automatch confidence
GENUS_CUTOFF = 0.85    # confidence below which genus is skipped
FUZZY_CUTOFF = 0.5     # confidence for select list options

# csv settings
FIELD_SEP = '\t'       # field separator for output file: default is Tab

# file locations
DICTIONARY_FILE = 'var/TaxonDictionary.txt'
OUTPUT_FILE = 'MatchedNames.txt' # output file name and location
NOTVALID_FILE = 'NotValid.txt'   # taxa which are not current and without synonym
CURRENT_BATCH = 'var/~CurrentBatch.txt'  # temp file forworking batch of names
LOGFILE = 'log/skipped.txt'      # log of names that were skipped
AUTOLOG = 'log/automatch.txt'    # log of names that were matched automatically
