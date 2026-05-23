#-------------------------------------------------------------------
# The objective is to decode the paragraphs and the tables in the
# order of the document
# APIs:
# - get_document_text
# - treat_text_with_contents
#-------------------------------------------------------------------

# Using extensively docx
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

import sys
sys.path.append('.')
from tools10 import myprint

# Constants
NUMS = ["0","1","2","3","4","5","6","7","8","9"]

#---------------------------------------------------------------------- iter_block_items
def iter_block_items(parent):
    """
    Generate a reference to each paragraph and table child within *parent*,
    in document order. Each returned value is an instance of either Table or
    Paragraph. *parent* would most commonly be a reference to a main
    Document object, but also works for a _Cell object, which itself can
    contain paragraphs and tables.
    """
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    elif isinstance(parent, _Row):
        parent_elm = parent._tr
    else:
        raise ValueError("something's not right")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

#---------------------------------------------------------------------- get_document_text
def get_document_text(source_file):
    '''
    The objective is to have a document in the right order, with paragraphs and tables.
    The chunking is prepared for paragraphs and tables.
    '''
    document = Document(source_file)
    text = ""
    for block in iter_block_items(document):
        # paragraphs should be separated by 2 \n: usefull for chunking
        if isinstance(block, Paragraph):
            text += block.text + "\n\n"
        # tables are formatted the md way
        elif isinstance(block, Table):
            text += "\n"
            for row in block.rows:
                row_data = []
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        row_data.append(paragraph.text)
                text += "| " + " | ".join(row_data) + " |\n"
            text += "\n"
        else:
            myprint(f"Found another type of content: {type(block)}")
    return text


#---------------------------------------------------------------------- analyze_contents_line
def analyze_contents_line(line):
    '''
    The objective of this function is to gather all the cases where we have a
    a table of contents in word documents
    '''
    if "TABLE OF CONTENTS" in line.upper():
        return True
    # Why 13? len("Contents") = 8, that let 4 char for other stuff like number
    # or even \t, but the objective is not to return True if "contents" is in
    # the middle of a phrase.
    if "CONTENTS" in line.upper() and len(line.strip()) < 13:
        return True
    return False


#---------------------------------------------------------------------- treat_text
def treat_text_with_contents(text, verbose=False):
    '''
    The idea is to enrich the original document with the numbers of the sections
    that we find in the table of contents.
    '''
    text2 = ""
    thetoc = {}
    toc = False
    nbtoc = 0
    corps = False
    count = 0
    lines = text.split('\n')
    # first scan to get the toc
    for line in lines:
        count += 1
        if analyze_contents_line(line):
            if verbose:
                myprint(f"| DOCX | Found 'CONTENTS' in line {count}")
            toc = True
            continue
        elif toc:
            for num in NUMS:
                if line == "":
                    continue
                if num == line[0]:
                    parts = line.split("\t") # 14.	Means provided by NHIndustries	128
                    if len(parts) == 3:
                        thetoc[parts[1]] = parts[0] #title first, index second
                        nbtoc += 1
                        break
        else:
            print(".",end='')
    print("")
    if toc and verbose:
        myprint(f"| DOCX| TOC found with {nbtoc} elements")
    if not toc:
        myprint("| DOCX | Info: TOC not found")
        return text
    # second scan to add numberings in titles
    for linebis in lines:
        found = False
        for elem in thetoc:
            if elem == linebis.strip():
                text2 += thetoc[linebis.strip()] + "\t" + linebis + "\n"
                if verbose:
                    myprint("| DOCX | " + thetoc[linebis.strip()] + "\t" + linebis)
                found = True
                break
        if not found:
            text2 += linebis + "\n"
    return text2


#---------------------------------------------------------------------- main
def main():
    test_doc = '.\\data\\source.docx'
    text = get_document_text(test_doc)
    with open(test_doc + ".txt", "w", encoding="utf-8") as out:
        out.write(text)
    myprint(f"| DOCX | {test_doc + '.txt'} created")

    text2 = treat_text_with_contents(text, True)
    with open(test_doc + "-contents.txt", "w", encoding="utf-8") as out:
        out.write(text2)
    myprint(f"| DOCX | {test_doc + '-contents.txt'} created")


#===================================================================== entry point
if __name__ == "__main__":
    main()
