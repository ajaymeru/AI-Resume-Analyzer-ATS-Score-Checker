import io
from typing import Union, BinaryIO
import PyPDF2


def extract_text_from_pdf(file_input: Union[str, BinaryIO]) -> str:
    """
    Extracts plain text from a PDF file input.
    
    Args:
        file_input: A file path string or a file-like binary object (e.g., BytesIO from Streamlit).
        
    Returns:
        The extracted and cleaned text content as a string.
        
    Raises:
        ValueError: If the file is not a valid PDF or is corrupted.
    """
    # Initialize a list to hold text extracted from each page
    text_content = []
    
    try:
        # Determine the input type. If it is a string path, open the file.
        # If it is a binary stream (like Streamlit's UploadedFile / BytesIO), read it directly.
        if isinstance(file_input, str):
            reader = PyPDF2.PdfReader(file_input)
        else:
            # Handle in-memory file-like binary streams (BytesIO)
            reader = PyPDF2.PdfReader(file_input)
            
        # Loop through each page in the PDF document and extract its text content
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            # If text is successfully extracted from the page, append it to the content list
            if page_text:
                text_content.append(page_text)
                
    except Exception as e:
        # Raise an error detailing that PDF parsing failed, passing the underlying exception message
        raise ValueError(f"Failed to parse PDF file: {str(e)}")
        
    # Join all pages with a newline character
    extracted_text = "\n".join(text_content)
    
    # Post-processing: clean and split the text into lines, stripping whitespace
    # and ignoring empty lines to return a clean, normalized string
    cleaned_lines = []
    for line in extracted_text.splitlines():
        trimmed = line.strip()
        if trimmed:
            cleaned_lines.append(trimmed)
            
    # Re-join clean non-empty lines with single newline character
    return "\n".join(cleaned_lines)

