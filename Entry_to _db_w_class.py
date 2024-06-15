import re
import psycopg2
from psycopg2 import OperationalError, DatabaseError
from PyPDF2 import PdfReader

# Base class for questions
class Question:
    def __init__(self, subj_name, prompt):
        self.subj_name = subj_name
        self.prompt = prompt

# Subclasses for different question types
class SubjectiveQuestion(Question):
    def __init__(self, subj_name, prompt):
        super().__init__(subj_name, prompt)

class ObjectiveQuestion(Question):
    def __init__(self, subj_name, prompt, answer):
        super().__init__(subj_name, prompt)
        self.answer = answer

class TrueFalseQuestion(ObjectiveQuestion):
    def __init__(self, subj_name, prompt, answer):
        super().__init__(subj_name, prompt, answer)

class MultipleChoiceQuestion(ObjectiveQuestion):
    def __init__(self, subj_name, prompt, choices, answer):
        super().__init__(subj_name,     prompt, answer)
        self.choices = choices

# Interface for storing questions in the database
class QuestionStorageInterface:
    def store_question(self, question):
        raise NotImplementedError("Subclasses should implement this method")

# Implementation of the interface for PostgreSQL database
class QuestionStorage(QuestionStorageInterface):
    def __init__(self, conn):
        self.conn = conn

    def store_question(self, question):
        if not isinstance(question, Question):
            raise ValueError("Can only store instances of Question or its subclasses")
        
        # Determine the type of question and prepare data accordingly
        if isinstance(question, SubjectiveQuestion):
            que_type = 'Subjective'
            ans_opt = None  # No answer options for subjective questions
        elif isinstance(question, TrueFalseQuestion):
            que_type = 'True/False'
            ans_opt = question.answer
        elif isinstance(question, MultipleChoiceQuestion):
            que_type = 'Multiple Choice'
            ans_opt = ', '.join(question.choices) + f"; Correct: {question.answer}"
        else:
            raise ValueError("Unsupported question type")

        # Insert data into the database
        insert_data(self.conn, question.subj_name, que_type, question.prompt, ans_opt)

# Existing functions from project 5 with minor modifications
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

def insert_data(conn, subj_name, que_type, que_text, ans_opt=None, chap_name=None):
    try:
        with conn.cursor() as curs:
            curs.execute("""
                INSERT INTO proj_eight(subj_name, que_type, que_text, ans_opt, chap_name)
                VALUES (%s, %s, %s, %s, %s)
            """, (subj_name, que_type, que_text, ans_opt, chap_name))
        conn.commit()
    except DatabaseError as e:
        print(f"Database operation failed: {e}")
        conn.rollback()

def load_data_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        full_text = ""
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
    qt_pattern = r'qt:\s*(.+)'
    q_pattern = r'q:\s*(.+)'
    a_pattern = r'a:\s*(\".+\"|.+)'
    chap_pattern = r'chap:\s*(.+)'
    roll_pattern = r'roll_no:\s*(.+)'

    for page in reader.pages:
        #print(f"page: '{page}'")
        text = page.extract_text()
        if text:
            full_text += text + '\n'
        else:
            print("No text found on this page.")
        #print(f"text: '{full_text}'\n")

    # Find each section of text that starts with 'ques>'
    sections = full_text.split('ques>')
    #print(f"sections: '{sections}'")
    for section in sections[1:]:  # Skip the first split as it's before the first 'ques>'
        #print(f"section: '{section}'")
        subj_match = re.search(subj_pattern, section)
        qt_match = re.search(qt_pattern, section)
        q_match = re.search(q_pattern, section)
        a_match = re.search(a_pattern, section, re.DOTALL)
        chap_match = re.search(chap_pattern, section)
        roll_match = re.search(roll_pattern, section)

        if subj_match and qt_match and q_match and a_match and chap_match:
            subj_name = subj_match.group(1).strip()
            que_type = qt_match.group(1).strip()
            que_text = q_match.group(1).strip()
            #ans_opt = a_match.group(1).strip()
            ans_opt = a_match.group(1).strip('\n')
            chap_name = chap_match.group(1).strip()
            roll_no = roll_match.group(1).strip()
            # print(f"{que_type}, \nfinal subject: {subj_name}, \nquestion: {que_text}, \nans: {ans_opt}, \nchapter: {chap_name}, \nroll_no: {roll_no}")
            # print("done")
            # input("press enter")
            insert_data(conn, subj_name, que_type, que_text, ans_opt, chap_name)

    conn.close()

# Example usage:
conn = connect_to_db()
storage = QuestionStorage(conn)

subj_question = SubjectiveQuestion("Programming", "Describe OOP concepts.")
storage.store_question(subj_question)

tf_question = TrueFalseQuestion("Programming", "Python supports multiple inheritance.", True)
storage.store_question(tf_question)

mc_question = MultipleChoiceQuestion("Geo", "What is the capital of France?", ["A) London", "B) Paris", "C) Rome"], "B")
storage.store_question(mc_question)

conn.close()
 
# Call the function with the path to your PDF
#load_data_from_pdf('D:\\content\\source\\ans_sheet2.pdf')