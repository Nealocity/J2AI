import shutil
import os
import PyPDF2

def copy_and_read_pdf(source_path, pdf_file_path, output_text_file, page_to_read):
    try:
        # Check if the source PDF file exists before copying
        if not os.path.isfile(source_path):
            print(f"The PDF file '{source_path}' does not exist.")
            return False

        shutil.copy(source_path, pdf_file_path)
        print(f"File '{source_path}' has been copied to '{pdf_file_path}'")

        # Open the PDF file
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)

            if 1 <= page_to_read <= num_pages:
                # Extract text from the specified page
                page = pdf_reader.pages[page_to_read - 1]
                page_text = page.extract_text()

                # Write the content of the specified page to a text file
                with open(output_text_file, 'w') as text_file:
                    if page_text:  # Check if the page contains text
                        text_file.write(f"Page {page_to_read}:\n{page_text}\n")
                        print(f"Content from page {page_to_read} has been written to '{output_text_file}'")
                    else:
                        print(f"No text found on page {page_to_read}")
                return True
            else:
                print(f"Invalid page number. Please enter a number between 1 and {num_pages}.")
                return False

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def process_user_input(user_input):
    if user_input.lower() == 'exit':
        print("Exiting the script.")
        return False

    try:
        if ',' in user_input:
            # Handle comma-separated input
            pages = [int(page.strip()) for page in user_input.split(',')]
        elif '-' in user_input:
            # Handle range input
            start, end = map(int, user_input.split('-'))
            pages = list(range(start, end + 1))
        else:
            # Single page input
            pages = [int(user_input)]

        return pages
    except ValueError:
        print("Invalid input. Please enter a valid page number or range (e.g., 1, 3-5) or type 'exit'.")
        return None

# Define the source and destination paths
content = r'D:\content'
source_file = 'source\proj.pdf'
source_path = os.path.join(content, source_file)
destination_folder = content
pdf_file_path = os.path.join(destination_folder, 'proj.pdf')
output_text_file = os.path.join(destination_folder, 'proj.txt')

# Check if the content folder exists
if not os.path.isdir(content):
    print(f"The folder '{content}' does not exist.")
    exit(1)  # Exit the script if the folder doesn't exist

while True:
    user_input = input("Enter the page number(s) you want to read (e.g., 1, 3-5) or type 'exit' to quit: ")
    pages = process_user_input(user_input)
    if pages is None:
        continue

    for page_to_read in pages:
        success = copy_and_read_pdf(source_path, pdf_file_path, output_text_file, page_to_read)
        if not success:
            break
    else:
        # All pages processed successfully
        break
