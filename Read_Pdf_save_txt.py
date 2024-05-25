import shutil
import os
import PyPDF2

# Define the source and destination paths
content = r'C:\content'
source_file = 'source\proj.pdf'
source_path = os.path.join(content, source_file)
destination_folder = content
pdf_file_path = os.path.join(destination_folder, 'proj.pdf')
output_text_file = os.path.join(destination_folder, 'proj.txt')

# Check if the content folder exists
if not os.path.isdir(content):
    print(f"The folder '{content}' does not exist.")
    exit(1)  # Exit the script if the folder doesn't exist

# Use shutil to copy the file
try:
    # Check if the source PDF file exists before copying
    if not os.path.isfile(source_path):
        print(f"The PDF file '{source_path}' does not exist.")
        exit(1)  # Exit the script if the PDF file doesn't exist

    shutil.copy(source_path, pdf_file_path)
    print(f"File '{source_path}' has been copied to '{pdf_file_path}'")
    
    # Open the PDF file and write its content to a text file
    with open(pdf_file_path, 'rb') as pdf_file, open(output_text_file, 'w') as text_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        # Read each page and write its content to the text file
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:  # Check if the page contains text
                text_file.write(f"Page {page_num + 1}:\n{page_text}\n\n")
            elif num_pages>1:
                text_file.write(f"Page {page_num + 1}:\nNo text on page\n\n")
                print(f"No text found on page {page_num + 1}")
            else:
                print(f"No text found on page {page_num + 1}")

    print(f"PDF content has been written to '{output_text_file}'")

except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")