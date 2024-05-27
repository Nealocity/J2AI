import sys
import psycopg2

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        return psycopg2.connect(
            dbname="project",
            user="proj_user",
            password="proj_user",
            host="localhost"
        )
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)


# Function to load and print questions from the database
def load_and_print_questions(chap_name):
    if not chap_name:
        print("No chapter name provided. Please provide a valid chapter name.")
        sys.exit(1)

    desired_chap_name = f'%{chap_name}%' 
    conn = connect_to_db()
    with conn.cursor() as curs:
        curs.execute("""
            SELECT que_text, chap_name FROM class_one WHERE chap_name like %s;
        """, (desired_chap_name,))
        questions = curs.fetchall()

        if not questions:
            print(f"No questions found for the chapter '{chap_name}'.")
        else:
            print(f"Questions for chapter matching '{chap_name}':")
            for question in questions:
                print(question[0], question[1])

    conn.close()

chapter_name = input("Enter the chapter name: ")
load_and_print_questions(chapter_name)