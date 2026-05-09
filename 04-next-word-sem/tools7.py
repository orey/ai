########################################################
# Tools for the Finance data processing
# O. Rey - July 2025
########################################################
import csv, time, os, os.path, sys
from datetime import datetime
from difflib import SequenceMatcher
import progressbar2, unidecode
import hashlib
import shutil, inspect
from rdflib import Graph


#---------------- In order to use in other files
#
#import sys
#sys.path.append('.')
#
#from toolsX import
#- string2md5 : returns a md5 of the string, can be used with other algorithms
#- footprint_sha256
#- footprint_sha1
#- ProgressBar: encapsulates the progress bar in a convenient class
#- ErrorFile: encapsulate a file with a convenient name
#- list_files_in_dir
#- ensureFile
#- ensureFolder
#- similar: finds a similarity between 2 strings
#- myexit: exit with a message
#- generateName: generate a timestamp before the filename
#- myprint: logs in the console and in a file in the same move
#- interrupt: my breakpoint
#-> breakpoint: a more elaborated version of interrupt
#- countLinesInCSVFile
#- countLinesInFile
#- Timer: encapsulate the timer in a class
#- find_in_disk: finds with a pattern
#- CounterDict: dict of key-value where value is the number of times key appear
#- print_dict
#- safe_copy: copy unless the target file exists
#- my_tokenizer: personal tokenizer
#- file_tokenizer
#- RDF store
#- imprint => immediate print to the console


#================================================= imprint
def imprint(t, end="\n"):
    print(t, end=end)
    sys.stdout.flush()


#================================================= RDFStore
class RDFStore():
    '''
    This class wraps the RDF store proposed by rdflib
    TODO Add more output formats in dump_store
    '''
    def __init__(self, name):
        # Expecting name to be something like "toto"
        self.name = name
        self.store = Graph()
    def get_store(self):
        return self.store
    def add(self, triple):
        self.store.add(triple)
    def remove(self, triple):
        self.store.remove(triple)
    def dump(self):
        myprint("Dumping store")
        tim = Timer("Store dump")
        filename = self.name if self.name.endswith(".ttl") else self.name + ".ttl"
        self.store.serialize(filename,
                             format='turtle')
        tim.stop()
        myprint("Store dumped")


#================================================= format_predicate
SYMBOLS_TO_REPLACE = [' ', '-', '/', '\\', '(',')',',',
                      '"', "'", "<", ">", "|", "{", "}",
                      "^", "#", "$", "*", ".", "`", "+",
                      "=", "%"]
REPLACEMENT = '_'

def format_URI(pred):
    new = ''
    for i, c in enumerate(pred):
        if c in SYMBOLS_TO_REPLACE:
            new += REPLACEMENT
        else:
            new += pred[i]
    return new


#-----------------------------------------------------------------------file_tokenizer
def file_tokenizer(f, keep_accents=False, verbose = False, removeFirstChar=True):
    '''
    More basic stuff but working quite well
    '''
    with open(f) as g:
        text = g.read()[(1 if removeFirstChar else 0):] #removing first char \ufeff
        if verbose: print("Text read")
        return my_tokenizer(text, keep_accents, verbose)

        
#-----------------------------------------------------------------------my_tokenizer
REPLACE = [
    ("\n", " "),
    ("_" , " "),
    ("”" , '"'),
    ("‘" , "'"),
    ("“" , '"'),
    ("[" , "" ),
    ("]" , "" )
]

ADD_SPACE_AROUND = [".",",",";",":","!","?","'",'"',"-","(",")","—"]

def my_tokenizer(text, keep_accents = False, verbose = False):
    '''
    This tokenizer was tested for English and French. It is simple and is quite robust.
    (benchmarks made on the Bible). It preserves accents and is word based.
    Returns an array of tokens in the order of the text.
    '''
    if not keep_accents:
        text = unidecode(text)
        if verbose: print("Accents removed")
    text = text.lower()
    if verbose: print("Text in lower case")
    for before, after in REPLACE:
        text = text.replace(before, after)
        if verbose: print(f"{before} was replaced by {after}")
    for char in ADD_SPACE_AROUND:
        text = text.replace(char," " + char + " ")
        if verbose: print("Created spaces around << " + char + " >>")
    return [x for x in text.split(" ") if x] #removing empty strings


#----------------------------------------------breakpoint
def breakpoint(obj=None):
    prefix = "Breakpoint"
    #print(inspect.stack()[0][3]) => breakpoint
    print(f"{prefix} in {inspect.stack()[1][3]}")
    if obj: print(f"{prefix}: {obj}")
    a = input(f"{prefix}: Do you want to continue? ('n' will stop) ")
    if a == "n":
        print(f"{prefix}:Goodbye")
        sys.exit()


#--------------------------------------------safe_copy
def safe_copy(source, target, verbose = False):
    if ensureFile(source):
        if ensureFile(target):
            #the target file exists
            if verbose: print(f"The file '{target}' already exists. Doing nothing.")
            return False
        else:
            shutil.copyfile(source,target)
            if verbose: print(f"File '{source}' copied to '{target}'")
            return True
    else:
        if verbose: print(f"The file '{source}' was not found. Doing nothing.")
        return False



#--------------------------------------------md5
def string2md5(mystr, algo='md5'):
    h = hashlib.new(algo)
    h.update(mystr.encode())
    return h.hexdigest()


#-----------------------------sha256sum
def footprint_sha256(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()

#-----------------------------sha1
def footprint_sha1(filename):
    with open(filename, 'rb') as doc:
        content = doc.read()
        return hashlib.sha1(content).hexdigest()



#---------------------------------------------ProgressBar
class ProgressBar():
    def __init__(self,mini,maxi):
        self.nb = maxi
        self.bar = progressbar2.ProgressBar(mini,maxi)
        self.count = 0
    def set(self, count):
        if count > self.nb:
            self.bar.update(self.nb)
            self.count = self.nb
        else:
            self.count = count
            self.bar.update(count)
        


#---------------------------------------------ErrorFile
class ErrorFile():
    def __init__(self,name,encoding="latin_1"):
        self.name = name
        self.thefile = open(generateName(name),
                            "w",
                            encoding=encoding)
    def write(self,line):
        self.thefile.write(line)
    def close(self):
        self.thefile.close()
    

#---------------------------------------------list_files_in_dir
def list_files_in_dir(mypath):
    return [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]


#--------------------------------ensure folders
def ensureFile(f):
    if os.path.isfile(f):
        return True
    else:
        return False    

#--------------------------------ensure folders
def ensureFolder(dire):
    if not os.path.isdir(dire): 
        os.makedirs(dire)


#--------------------------------------------Similiar
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


#============================================ generateName
def myexit(msg):
    myprint(msg)
    myprint("Exiting")
    exit()


#============================================ generateName
def generateName(name):
    return datetime.now().strftime('%Y%m%d_%H%M%S-%f_') + name


#============================================ myprint
LOG = generateName("run.log")
FIRST = True
def myprint(str):
    '''
    print to console and into a log file
    '''
    global FIRST
    if FIRST:
        with open(LOG, "w",encoding='utf-8') as logfile:
            logfile.write(str + '\n')
        FIRST = False
    else:
        with open(LOG, "a",encoding='utf-8') as logfile:
            logfile.write(str + '\n')
    print(str)
        

#============================================ interrupt
def interrupt(obj=None):
    '''
    Manual breakpoint
    '''
    if obj != None:
        print(obj)
    resp = input("Continue? [n/no] ")
    if resp.upper() in ["N","NO"]:
        print("Goodbye!")
        exit(0)


#=========================================== count lines in csv file
def countLinesInCSVFile(file):
    newreader = csv.reader(open(file, "r", encoding='utf-8', errors='ignore'))
    nblines = 0
    for i, row in enumerate(newreader):
        nblines += 1
    return nblines

#=========================================== count lines in csv file
def countLinesInFile(file):
    f = open(file, "r", errors='ignore')
    nblines = 0
    for line in f:
        nblines += 1
    return nblines

#============================================ Timer
class Timer():
    def __init__(self, name=""):
        self.start = time.time()
        self.name = name
    def stop(self):
        self.stop = time.time()
        print("~~~ Treatment '" + self.name + "' duration: "
              + str((round(self.stop-self.start))//60)
              + " minutes and "
              + str((round(self.stop-self.start))%60)
              + " seconds")

#-------------------------------find_in_disk
def find_in_disk(pattern, path):
    result = []
    pattern2 = "*" + pattern + "*" + SUFFIX #The pattern is really built here
    for root, dirs, files in os.walk(path, topdown=True):
        #print("Directory path: " + root)
        for name in files:
            if fnmatch.fnmatch(name, pattern2):
                found = os.path.join(root, name)
                result.append(found)
                print("In: " + root)
                print("Found: " + found)
    return result


#-------------------------------CounterDict
class CounterDict():
    def __init__(self):
        self.dic = {}
    def append(self, key):
        if key in self.dic.keys():
            self.dic[key] = self.dic[key] + 1
        else:
            self.dic[key] = 1

#-------------------------------print_dict
def print_dict(dic, separator=" | "):
    for key,value in dic.items():
        print(str(key) + separator + str(value))

