#!/usr/bin/env python

from settings import *
import os.path, Tkinter, tkFont, tkFileDialog
import taxonutils


class TaxonLinker():

  def __init__(self,root):
  
    self.taxondict = DICTIONARY_FILE
    self.nameslist = []
    self.results = []
    self.dictload = False
    self.nmload = False
    
    # options and format definitions
    sans10px = tkFont.Font(family='Arial',size=-15)
    button_opt = {'padx': 5, 'pady': 5, 'side': Tkinter.LEFT}
    entry_opt = {'padx': 5, 'pady': 5, 'side': Tkinter.LEFT, 'fill': Tkinter.X, 
                 'expand': 1}
    self.ftypes=(('Text files', '*.txt'),('CSV files', '*.csv'),
                 ('All files','*.*'))
    
    # loading buttons frame
    buttonframe = Tkinter.Frame(root)
    Tkinter.Button(buttonframe,text='Load Dictionary',
                   command=self.load_dict).pack(**button_opt)
    Tkinter.Button(buttonframe,text='Load Names', 
                   command=self.load_names).pack(**button_opt)
    buttonframe.pack(fill=Tkinter.X,expand=1)
    
    # current taxon frame
    taxonframe = Tkinter.Frame(root)
    self.taxonentry = Tkinter.Text(taxonframe,width='110',height='2',
                                   wrap='word',font=sans10px)
    self.taxonentry.pack(**entry_opt)
    Tkinter.Button(taxonframe,text='Check Updated Name',
                   command=self.check_updated).pack(**button_opt)
    taxonframe.pack(fill=Tkinter.X,expand=1)
    
    # select frame with buttons on the right
    Tkinter.Label(root,text='Select correct taxon:').pack(side=Tkinter.TOP,
            anchor=Tkinter.W,padx=5)
    selectframe = Tkinter.Frame(root)
    self.select = Tkinter.Listbox(selectframe,width=100,height=8,font=sans10px)
    self.select.bind('<<ListboxSelect>>')
    self.select.pack(side=Tkinter.LEFT,fill=Tkinter.BOTH,expand=1,
                     anchor=Tkinter.W,padx=5,pady=5)
    buttonframe = Tkinter.Frame(selectframe)
    self.savebtn = Tkinter.Button(buttonframe,text='Save',
            state=Tkinter.DISABLED, command=self.save)
    self.savebtn.pack(fill=Tkinter.BOTH,padx=5,pady=5)
    self.skipbtn = Tkinter.Button(buttonframe,text='Skip',
            state=Tkinter.DISABLED, command=self.skip)
    self.skipbtn.pack(fill=Tkinter.BOTH,padx=5,pady=5)
    buttonframe.pack(side=Tkinter.LEFT,padx=5,pady=5,anchor=Tkinter.W)
    selectframe.pack(anchor=Tkinter.NW,fill=Tkinter.BOTH,expand=1)

    # status bar at the bottom
    self.status = Tkinter.Label(root,text='')
    self.status.pack(side=Tkinter.LEFT,anchor=Tkinter.W,padx=5,pady=5)
    
    # check if dictionary file exists, and if so, load it
    if os.path.isfile(self.taxondict):
      self.dictionary = taxonutils.TaxonIndex(self.taxondict)
      self.dictload = True
      
    # check if there's a current batch of names, and if so, load it
    if os.path.isfile(CURRENT_BATCH):
      with open(CURRENT_BATCH,'r') as f: 
        for line in f:
            self.nameslist.append(line.strip())
      self.nmload = True
      self.readnext()
    
    self.update_status()
  

  def load_dict(self):
    self.taxondict = tkFileDialog.askopenfilename(filetypes=self.ftypes,
        title="Please select dictionary file")
    if self.taxondict:
      self.dictionary = taxonutils.TaxonIndex(self.taxondict)
      self.dictload = True
      self.update_status()

  
  def load_names(self):
    fn = tkFileDialog.askopenfilename(filetypes=self.ftypes,
        title="Please select input names file")
    if fn:
      self.nameslist = []
      with open(fn,'r') as f: 
        for line in f:
            self.nameslist.append(line.rstrip('\n'))
      self.nmload = True
      self.readnext()

  
  def check_updated(self):
    self.process_taxon()
    

  def save(self,taxon=''):
    """log current taxon to output file"""
    # Todo: handle case when relatedResourceID field is not in the dictionary
    if taxon == '':
        taxon = self.results[int(self.select.curselection()[0])]
    if 'taxonomicStatus' in self.dictionary.taxonindex[taxon].keys():
      if self.dictionary.taxonindex[taxon]['taxonomicStatus'].lower() == \
            'synonym' and self.dictionary.taxonindex[taxon]\
            ['relatedResourceID'] != '':
        # if it's a synonym, save the linked ID for the synonym
        self.log(self.nameslist[0].strip()+FIELD_SEP+self.dictionary.\
                taxonindex[taxon]['relatedResourceID'],OUTPUT_FILE)
        if self.dictionary.taxonindex[taxon]['taxonomicStatus'].lower() not in \
                ['accepted','valid','synonym']:
          # if the status is not valid or synonym, save it to work on separately
          self.log(self.nameslist[0].strip()+FIELD_SEP+self.dictionary.\
                taxonindex[taxon]['taxonID'],NOTVALID_FILE)
      else:
        # if it's not a synonym save the ID
        self.log(self.nameslist[0].strip()+FIELD_SEP+self.dictionary.\
                 taxonindex[taxon]['taxonID'],OUTPUT_FILE)
    else:
      # if there's no taxonomicStatus field, just save the taxonID
      self.log(self.nameslist[0].strip()+FIELD_SEP+self.dictionary.\
               taxonindex[taxon]['taxonID'],OUTPUT_FILE)
            
    self.skip('save')
    
  
  def skip(self,reason='button'):
    """Log skipped name with reason, and move to the next record."""
    if reason == 'genus':
      self.log(self.nameslist[0].strip()+" (couldn't find genus)",LOGFILE)
    elif reason == 'button':
      self.log(self.nameslist[0].strip()+" (skip button)",LOGFILE)
    if len(self.nameslist) > 1:
      self.nameslist = self.nameslist[1:]
      self.taxonentry.delete('1.0','end')
      self.taxonentry.insert('1.0',self.nameslist[0].strip())
      self.readnext()
    else:
      self.nameslist = []
      self.taxonentry.delete('1.0','end')
      self.taxonentry.insert('1.0','No more unmatched names.')
      self.savebtn.configure(state=Tkinter.DISABLED)
      self.skipbtn.configure(state=Tkinter.DISABLED)
      self.nmload = False
    

  def update_status(self):
    """Update the status bar."""
    if not self.dictload and not self.nmload:
      self.status.configure(text="Dictionary not loaded; Names not loaded.")
    elif self.dictload and not self.nmload:
      s = '{:,}'.format(len(self.dictionary.taxonindex))
      self.status.configure(text="Dictionary loaded with %s taxa; Names not "
          "loaded." % s)
    elif not self.dictload and self.nmload:
      s = '{:,}'.format(len(self.nameslist))
      self.status.configure(text="Dictionary not loaded; %s names remaining to "
          "process." % s)
    elif self.dictload and self.nmload:
      self.savebtn.configure(state=Tkinter.NORMAL)
      self.skipbtn.configure(state=Tkinter.NORMAL)
      s = ('{:,}'.format(len(self.dictionary.taxonindex)),
           '{:,}'.format(len(self.nameslist)))
      self.status.configure(text="Dictionary loaded with %s taxa; %s names "
          "remaining to process." % s)
    else:
      self.status.configure(text="Error updating status.")


  def log(self,s,f):
    """Driver for writing text to a specified log file."""
    d = os.path.dirname(f)
    if not os.path.exists(d) and not d=='':
      os.makedirs(d)
    open(f, 'a+').writelines(s.strip() + '\n')
    

  def process_taxon(self):
    """Uses certainty cutoff levels to automatically skip or match taxa, and 
    ask the user if uncertain.
    """
    self.select.delete(0,'end')
    #First look for genus match to speed up performance
    genus = self.dictionary.matchgenera(self.taxonentry.get('1.0','end'),
        1,GENUS_CUTOFF)
    if len(genus) > 0:
      self.results = self.dictionary.matchtaxa(self.taxonentry.get('1.0','end'),
                                               genus[0],8,FUZZY_CUTOFF)
      if len(self.results) > 0:
        # if first match is good enough, save automatically, else wait for user 
        # to skip or select and save.
        if taxonutils.ratio(self.taxonentry.get('1.0','end'),
                            self.results[0]) >= PERFECT_CUTOFF:
          self.select.select_set(0)
          self.log(self.nameslist[0].strip() + " -> " + self.results[0],AUTOLOG)
          self.save(self.results[0])
        else:
          for taxon in self.results:
            if 'taxonomicStatus' in self.dictionary.taxonindex[taxon].keys():
              if self.dictionary.taxonindex[taxon]['taxonomicStatus'].lower()\
                  in ['current', 'valid']:
                self.select.insert('end',taxon)
              elif self.dictionary.taxonindex[taxon]['taxonomicStatus'].lower()\
                  == 'synonym' and self.dictionary.taxonindex[taxon]\
                  ['relatedResourceID'] != '':
                synonym = self.dictionary.idindex[self.dictionary.\
                    taxonindex[taxon]['relatedResourceID']]['scientificName']
                self.select.insert('end',"*" + taxon + " = " + synonym)
              else:
                self.select.insert('end',"*" + taxon + " (not current)")
            else:
              self.select.insert('end',taxon)
          self.select.select_set(0) 
    else:
      self.skip('genus')  
          

  def readnext(self):
    """Load the next name to be processed."""
    if self.nameslist is not None and len(self.nameslist) > 0:
      self.taxonentry.delete('1.0','end')
      self.taxonentry.insert('1.0',self.nameslist[0])
      self.process_taxon()
      self.update_status()
    else:
      raise TypeError("No names to process.")


  def on_exit(self):
    """Write current file on exit."""
    if len(self.nameslist)>0:
      with open(CURRENT_BATCH,'w+') as f:
        for n in self.nameslist:
          f.write(n+'\n')
      root.destroy()
    else:
      try:
        os.remove(CURRENT_BATCH)
      except OSError:
        pass
      root.destroy()

if __name__=='__main__':
  root = Tkinter.Tk()
  root.wm_title("Taxon Linker")
  myapp = TaxonLinker(root)
  root.protocol("WM_DELETE_WINDOW", myapp.on_exit)
  root.mainloop()
