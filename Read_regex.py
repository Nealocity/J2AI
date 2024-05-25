import os
import re
import PyPDF2
import csv


def process_pdf(source_path, output_text_file, regex_pattern):
    # Function to process PDF files and extract text matching the regex
    try:
        with open(source_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)

            with open(output_text_file, 'w') as text_file:
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    matches = re.findall(r'^.*' + regex_pattern + r'.*$', page_text, re.MULTILINE)

                    for match in matches:
                        text_file.write(f"{match}\n")

            print(f"Extracted content from all pages has been written to '{output_text_file}'")

    except Exception as e:
        print(f"An error occurred: {e}")

def process_text_file(source_path, output_text_file, regex_pattern):
    # Function to process text files and extract text matching the regex
    try:
        with open(source_path, 'r') as file:
            content = file.read()
            matches = re.findall(r'^.*' + regex_pattern + r'.*$', content, re.MULTILINE)

        with open(output_text_file, 'w') as file:
            for match in matches:
                file.write(f"{match}\n")
        print(f"Extracted content has been written to '{output_text_file}'")

    except Exception as e:
        print(f"An error occurred: {e}")

def process_cfg_file(source_path, output_text_file, regex_pattern):
    # Function to process .cfg files and extract text matching the regex
    try:
        with open(source_path, 'r') as file:
            content = file.read()
            matches = re.findall(r'^.*' + regex_pattern + r'.*$', content, re.MULTILINE)

        with open(output_text_file, 'w') as file:
            for match in matches:
                file.write(f"{match}\n")
        print(f"Extracted content has been written to '{output_text_file}'")

    except Exception as e:
        print(f"An error occurred: {e}")

def process_csv_file(source_path, output_text_file, regex_pattern):
    # Function to process .csv files and extract text matching the regex
    try:
        with open(source_path, 'r') as file:
            reader = csv.reader(file)
            matches = []
            for row in reader:
                row_text = ','.join(row)
                # Modify the regex pattern to capture the entire line
                match = re.search(r'^.*' + regex_pattern + r'.*$', row_text)

#                for cell in row:
#                    match = re.search(regex_pattern, cell)
                if match:
                    matches.append(match.group())

#        with open(output_text_file, 'w') as file:
        with open(output_text_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for match in matches:
                writer.writerow([match])
#               file.write(f"{match}\n")
        print(f"Extracted content from CSV file has been written to '{output_text_file}'")

    except Exception as e:
        print(f"An error occurred: {e}")

# Define the destination path
content = r'D:\content'
destination_folder = content

# Check if the content folder exists
if not os.path.isdir(content):
    print(f"The folder '{content}' does not exist.")
    exit(1)  # Exit the script if the folder doesn't exist

# Ask the user for the file name, extension, and the regex pattern
file_name = input("Enter the file name with extension (e.g., proj.pdf): ")
regex_pattern = input("Enter the regular expression pattern to match: ")
source_path = os.path.join(content, file_name)
output_text_file = os.path.join(destination_folder, os.path.splitext(file_name)[0] + '_extracted.txt')

# Determine the file extension and call the appropriate function
file_extension = os.path.splitext(file_name)[1].lower()

if file_extension == '.pdf':
#    page_to_read = int(input("Enter the page number you want to read: "))
#    process_pdf(source_path, output_text_file, page_to_read, regex_pattern)
    process_pdf(source_path, output_text_file, regex_pattern)
elif file_extension in ['.cfg','.txt']:
    process_text_file(source_path, output_text_file, regex_pattern)
elif file_extension == '.csv':
    process_csv_file(source_path, output_text_file, regex_pattern)
else:
    print(f"The file extension '{file_extension}' is not supported for regex extraction.")