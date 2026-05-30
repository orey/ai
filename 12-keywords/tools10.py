'''

Various tools for multi-purpose programs

* O. Rey - rey.olivier@gmail.com
* Creation date: July 2024
* Last update: May 2026

In order to use in other files

import sys
sys.path.append('.')

from toolsX import

* string2md5 : returns a md5 of the string, can be used with other algorithms
* footprint_sha256
*  sha256_fingerprint, more elaborated version
* footprint_sha1
* myProgressBar: encapsulates the progress bar in a convenient class
* ErrorFile: encapsulate a file with a convenient name
* list_files_in_dir
* ensureFile
* ensureFolder
* myexit: exit with a message
* generateName: generate a timestamp before the filename
* myprint: logs in the console and in a file in the same move
* interrupt: my breakpoint
*  mybreakpoint: a more elaborated version of interrupt
* countLinesInCSVFile
* countLinesInFile
* Timer: encapsulate the timer in a class
* find_in_disk: finds with a pattern
* CounterDict: dict of key-value where value is the number of times key appear
* print_dict
* safe_copy: copy unless the target file exists
* imprint => immediate print to the console
* CSV_Trace => create a CSV trace file without the pain
* create_text_file => 
* is_zip
'''

import csv, time, os, os.path, sys
from datetime import datetime
import hashlib
import shutil, inspect
import zipfile


#================================================= is_zip
def is_zip(file_path):
    try:
        with zipfile.ZipFile(file_path) as zf:
            return True
    except zipfile.BadZipFile:
        return False

    
#================================================= create text file
def create_text_file(filename, text, enc = "utf8", verbose = False, prefix = ""):
    try:
        with open(filename, "w", encoding=enc) as f:
            f.write(text)
        if verbose:
            print(f"{prefix}File '{filename}' was created")
        return True
    except Exception as e:
        print(f"Creation Error for file '{filename}'\nInfo: File path length = {len(filename)}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e}")
        return False



#=================================================
class CSV_trace():
    def __init__(self, filename, mode="w", encode="utf8", sep = ";"):
        self.filename = filename
        self.csvfile = open(self.filename, mode, encoding = encode, newline='')
        self.writer = csv.writer(self.csvfile, quoting=csv.QUOTE_ALL, delimiter = sep)
    def add(self, array):
        self.writer.writerow(array)


#================================================= myProgressBar
class myProgressBar():
    length = 80
    def __init__(self,target, name = ""):
        self.target = target #int
        self.message = ""
        self.name = name
        self.exact = False
        print("Treatment " + ((self.name + " started") if self.name != "" else "started"))

    def set(self,current, message=""):
        if current <= 0:
            print("Progress:   0% [" + "-"*myProgressBar.length + "]", end = "\r", flush=True)
        elif current >= self.target:
            print("Progress: 100% [" + "#"*myProgressBar.length + "] - Job terminated.", flush=True)
            self.exact = True
        else:
            temp = int(current / self.target * myProgressBar.length)
            percent = int(current / self.target * 100)
            if message != "":
                self.message = message
                print("Progress: " + (str(percent)).rjust(3)
                      + "% [" + "#"*temp + "-"*(myProgressBar.length-temp)
                      + "] " + message, end = "\r", flush=True)
            else:
                if self.message != "":
                    #there was a message before and we must remove it
                    print("Progress: " + (str(percent)).rjust(3)
                      + "% [" + "#"*temp + "-"*(myProgressBar.length-temp)
                      + "] " + " "*len(self.message), end = "\r", flush=True)
                    self.message = ""
                else:
                    print("Progress: " + (str(percent)).rjust(3)
                      + "% [" + "#"*temp + "-"*(myProgressBar.length-temp)
                      + "] ", end = "\r", flush=True)

    def stop(self):
        print(("\n" if not self.exact else "") + "Treatment "
              + ((self.name + " terminated") if self.name != "" else "terminated"))
        

#======================== test_progress_bar
def test_progress_bar():
    pb1 = myProgressBar(149, "test1")
    for i in range(150):
        if i == 70:
            pb1.set(i, "Warning, this can be big")
            time.sleep(2)
        else:
            pb1.set(i)
            time.sleep(0.05)
    pb1.stop()
    # exact: i va à la borne max 39
    pb2 = myProgressBar(39)
    for i in range(40):
        pb2.set(i)
        time.sleep(0.1)
    pb2.stop()
    # non exact: i ne va pas à la borne max 70 mais va à 69
    pb3 = myProgressBar(70)
    for i in range(70):
        pb3.set(i)
        time.sleep(0.1)
    pb3.stop()
    

#================================================= imprint
def imprint(t, end="\n"):
    print(t, end=end)
    sys.stdout.flush()


#----------------------------------------------breakpoint
def mybreakpoint(obj=None):
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

def sha256_fingerprint(filepath: str) -> str:
    """Create SHA256 fingerprint of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


#-----------------------------sha1
def footprint_sha1(filename):
    with open(filename, 'rb') as doc:
        content = doc.read()
        return hashlib.sha1(content).hexdigest()


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


#============================================ generateName
def myexit(msg):
    myprint(msg)
    myprint("Exiting")
    exit()


#============================================ generateName
def generateName(name=None):
    if name:
        return datetime.now().strftime('%Y%m%d_%H%M%S-%f_') + name
    else:
        return datetime.now().strftime('%Y%m%d_%H%M%S-%f_')


#============================================ myprint
LOG = generateName("run.log")
FIRST = True
def myprint(obj, verbose=True, flush=True):
    '''
    print to console and into a log file
    '''
    global FIRST
    if FIRST:
        with open(LOG, "w",encoding='utf-8') as logfile:
            logfile.write(str(obj) + '\n')
        FIRST = False
    else:
        with open(LOG, "a",encoding='utf-8') as logfile:
            logfile.write(str(obj) + '\n')
    if verbose:
        print(str(obj), flush=flush)
        

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



def test():
    test_progress_bar()

        

if __name__ == "__main__":
    test()
