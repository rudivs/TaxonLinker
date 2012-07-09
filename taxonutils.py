#!/usr/bin/env python

import csv
import difflib


class TaxonIndex():
    """
    TaxonIndex is a class for reading a taxon dictionary file (which must be
    in the form of a tab-separated CSV text file), and matching genera and taxa
    against that dictionary using a fuzzy-matching algorithm to deal with
    spelling errors.
    """
    # Todo: handle if taxonID in fieldnames but not provided for a row
    # Todo: does this work with Unicode files?
    # Todo: sort the genus lists

    def __init__(self,csvfile,delimiter='\t'):
        self.taxonindex = dict()
        self.genusindex = dict()
        self.idindex = dict()
        self._taxontest = dict()
        validheaders = set(['scientificName','taxonID','taxonomicStatus',
                   'relatedResourceID'])
        
        with open(csvfile,'rb') as f:
            try:
                dialect = csv.Sniffer().sniff(f.read(2048),delimiters=delimiter)
                f.seek(0)
                self.reader = csv.DictReader(f, dialect=dialect)
            except csv.Error:
                f.seek(0)
                self.reader = csv.DictReader(f)
            self.fieldnames = self.reader.fieldnames
            if 'scientificName' in self.fieldnames:
                for r in self.reader:
                    if len(r) != len(self.fieldnames):
                        raise csv.Error("Number of fields should be "
                                    "%s: %s" % (len(self.fieldnames),str(r)))
                    self.taxonindex[r['scientificName']] = {k:v for k,v in \
                        r.items() if k in validheaders-set(['scientificName'])}
                    if 'taxonID' not in self.fieldnames :
                        self.taxonindex[r['scientificName']]['taxonID'] = \
                            r['scientificName']
                    else:
                        self.idindex[r['taxonID']] = \
                            {k:v for k,v in r.items() if k in validheaders-
                             set(['taxonID'])}                         
                    try:
                        self.genusindex[r['scientificName'].split(' ')[0].\
                            strip().capitalize()] += [r['scientificName']]
                    except KeyError:
                        self.genusindex[r['scientificName'].split(' ')[0].\
                            strip().capitalize()] = [r['scientificName']]
            else:
                raise csv.Error("CSV Error: headers must include at least "
                 "'scientificName'. Current headers: %s" % str(self.fieldnames))
        self._taxontest = {n.strip().lower():n for n in self.taxonindex}
            

    def matchgenera(self,genus,n=1,sensitivity=0.85):
        """Returns up to n genera which are similar to the genus of the name 
        provided.
        """
        #Assumes first word is genus
        test = genus.strip().split(' ')[0].capitalize()
        return difflib.get_close_matches(test,self.genusindex.keys()
            ,n,sensitivity)
        
    def matchtaxa(self,t,genus=None,n=1,sensitivity=0.65):
        """Returns up to n taxa which have a similar name to the one
        provided. If genus is provided, limits search to that genus.
        """
        test = t.strip().lower()
        if genus == None:
            results = difflib.get_close_matches(test,self._taxontest,n,
                                                sensitivity)
        else:
            glist = [t.lower() for t in self.genusindex[genus]]
            results = difflib.get_close_matches(test,glist,n,sensitivity)
        return [self._taxontest[r] for r in results]
        
def ratio(t1,t2):
    """Returns the closeness of the match between two taxon names, with 1 being
    exact.
    """
    t1 = t1.strip().lower()
    t2 = t2.strip().lower()
    return difflib.SequenceMatcher(None,t1,t2).ratio()


if __name__=='__main__':

    dict1 = TaxonIndex('test/sn_dict')
    dict2 = TaxonIndex('test/id_sn_dict')
    print("sn_dict:")
    for k,v in dict1.taxonindex.items():
        print(k + ": " + str(v))
    print("\nid_sn_dict:")
    for k,v in dict2.taxonindex.items():
        print(k + ": " + str(v))
    print
    print dict1.matchtaxa('THALASSARCH CHLORORYNCHOS',1,0.9)
