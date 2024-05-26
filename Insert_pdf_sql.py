import re
import psycopg2
from psycopg2 import OperationalError, DatabaseError
from PyPDF2 import PdfReader

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        return psycopg2.connect(
            dbname="project",
            user="proj_user",
            password="proj_user",
            host="localhost"
        )
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to insert data into the database
def insert_data(conn, subj_name, que_text, ans_opt, chap_name):
    try:
        with conn.cursor() as curs:
            curs.execute("""
                INSERT INTO class_one(subj_name, que_text, ans_opt, chap_name)
                VALUES (%s, %s, %s, %s)
            """, (subj_name, que_text, ans_opt, chap_name))
        conn.commit()
    except DatabaseError as e:
        print(f"Database operation failed: {e}")
        conn.rollback()

# Function to extract and load data from PDF
def load_data_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
    except (FileNotFoundError) as e:
        print(f"Error reading the PDF file: {e}")
        return

    conn = connect_to_db()
    if conn is None:
        return

    # Define your regex pattern for the 'ques>' marker
    ques_marker_pattern = r'ques>'

    # Define your regex patterns for the fields
    subj_pattern = r'subj:\s*(.+)'
    q_pattern = r'q:\s*(.+)'
    a_pattern = r'a:\s*(.+)'
    chap_pattern = r'chap:\s*(.+)'
    roll_pattern = r'roll_no:\s*(.+)'

    for page in reader.pages:
        #print(f"page: '{page}'")
        text = page.extract_text()
        #print(f"text: '{text}'")

        # Find each section of text that starts with 'ques>'
        sections = text.split('ques>')
        #print(f"sections: '{sections}'")
        for section in sections[1:]:  # Skip the first split as it's before the first 'ques>'
            #print(f"section: '{section}'")
            subj_match = re.search(subj_pattern, section)
            q_match = re.search(q_pattern, section)
            a_match = re.search(a_pattern, section)
            chap_match = re.search(chap_pattern, section)
            roll_match = re.search(roll_pattern, section)

            if subj_match and q_match and a_match and chap_match:
                subj_name = subj_match.group(1).strip()
                que_text = q_match.group(1).strip()
                ans_opt = a_match.group(1).strip()
                chap_name = chap_match.group(1).strip()
                roll_no = roll_match.group(1).strip()
                #print(f"final subject: '{subj_name}', \nquestion: '{que_text}',\nans: '{ans_opt}', \nchapter: '{chap_name}', \nroll_no: '{roll_no}")
                insert_data(conn, subj_name, que_text, ans_opt, chap_name)

    conn.close()

# Call the function with the path to your PDF
load_data_from_pdf('D:\\content\\source\\ans_sheet.pdf')