'''
This module extracts text from PDF.
'''





#---------------------------------------------------------- analyze_pdf
def get_text_from_standard_pdf(source_file, verbose=False) -> str:
    """
    Analyze a PDF to determine if it has extractable text or is image-only.
    Returns True if the PDF has extractable text, False otherwise.
    """
    try:
        reader = PdfReader(source_file)

        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]        
            text += page.extract_text()
    except Exception as e:
        myprint(f"| PDF  | Error | Error for file '{source_file}'")
        myprint(f"| PDF  | Exception type: {type(e).__name__}")
        myprint(f"| PDF  | Exception message: {e}")
        return False

    # If any non-whitespace text is found, consider it a standard PDF
    if len(text.strip())<2:
        myprint(f"| PDF  | No text found (image PDF?) | {source_file}", verbose)
        return False
    else:
        myprint(f"| PDF  | Standard PDF | {source_file} ", verbose)
    #creating output file
    return create_text_file(target_file + ".txt", text, prefix="| PDF  | ")





if __name__ = "__main__":
    
