import os

PERFECT_CUTOFF = 0.95  # confidence requred to match automatically
GENUS_CUTOFF = 0.85    # confidence below which genus is skipped
FUZZY_CUTOFF = 0.5     # minimum confidence required to list taxon as a select option
FIELD_SEP = '\t'       # field separator for output file: default is Tab
DICTIONARY_FILE = 'var' + os.sep + 'TaxonDictionary.txt'  # taxon dictionarary to match against
OUTPUT_FILE = 'MatchedNames.txt'   # output file name and location
NOTVALID_FILE = 'NotValid.txt'     # logs taxa which are not current and without synonym
CURRENT_BATCH = 'var' + os.sep + '~CurrentBatch.txt' # working batch of names

LOGFILE = 'log' + os.sep +'skipped.txt'                   # log of names that were skipped
AUTOLOG = 'log' + os.sep + 'automatch.txt'                # log of names that were matched automatically
