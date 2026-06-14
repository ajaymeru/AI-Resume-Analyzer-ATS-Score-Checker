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
    text_content = []
    
    try:
        # If input is a string path, open it; if it is a binary stream, use it directly
        if isinstance(file_input, str):
            reader = PyPDF2.PdfReader(file_input)
        else:
            # For BytesIO or file-like objects
            reader = PyPDF2.PdfReader(file_input)
            
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
                
    except Exception as e:
        raise ValueError(f"Failed to parse PDF file: {str(e)}")
        
    extracted_text = "\n".join(text_content)
    
    # Simple post-processing to normalize spaces and lines
    cleaned_lines = []
    for line in extracted_text.splitlines():
        trimmed = line.strip()
        if trimmed:
            cleaned_lines.append(trimmed)
            
    return "\n".join(cleaned_lines)
