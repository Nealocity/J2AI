import os
import shutil
from PyPDF2 import PdfReader

source_pdf_path = 'D:\content\source\proj.pdf'
content_dir = 'D:\content'

# Function to copy and process PDF files
def process_folders(folder_path):
    for subdir, dirs, files in os.walk(folder_path):
        print(f"{subdir} , {dirs} , {files}")
        for dir in dirs:
            try:
                print(f"{dir}")
                # Construct paths
                subfolder_path = os.path.join(subdir, dir)
                pdf_dest_path = os.path.join(subfolder_path, 'source.pdf')
                output_txt_path = os.path.join(subfolder_path, 'output.txt')

                # Copy source.pdf to subfolder
                shutil.copy(source_pdf_path, pdf_dest_path)
                print("copying")

                # Read PDF and write contents to output.txt
                with open(output_txt_path, 'w') as output_file:
                    reader = PdfReader(pdf_dest_path)
                    for page in reader.pages:
                        output_file.write(page.extract_text())
                
                # Check if output.txt is created
                if not os.path.isfile(output_txt_path):
                    raise FileNotFoundError(f"Failed to create {output_txt_path}")

            except FileNotFoundError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

# Check if the source PDF exists
if not os.path.exists(source_pdf_path):
    print("The source PDF file was not found.")
else:
    # Process the folders
    process_folders(content_dir)