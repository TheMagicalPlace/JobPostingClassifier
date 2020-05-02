import os

import sqlite3,json

def file_setup(file_term):
    """Sets up the file structure used by the program for each search term"""
    try:
        os.mkdir(os.path.join(os.getcwd(),file_term))
    except FileExistsError:
        pass
    try:
        os.mkdir(os.path.join(os.getcwd(), 'webdrivers'))
    except FileExistsError:
        pass
    else:
        os.mkdir(os.path.join(os.getcwd(),'webdrivers','chromedriver'))
        os.mkdir(os.path.join(os.getcwd(),'webdrivers','geckodriver'))

    try:
        os.mkdir(os.path.join(os.getcwd(), 'user_information'))
    except FileExistsError:
        pass
    else:
        with open(os.path.join(os.getcwd(), 'user_information','settings.json'),'w') as st:
            st.write(json.dumps({}))
    try:
        open(os.path.join(os.getcwd(), file_term, f'{file_term}.db'))
    except FileNotFoundError:
        open(os.path.join(os.getcwd(), file_term, f'{file_term}.db'), 'w')
    finally:
        with sqlite3.connect(os.path.join(os.getcwd(), file_term, f'{file_term}.db')) as connection:
            cursor = connection.cursor()
            for table in ['training','results','unsorted','metadata','model_performance_results']:
                try:
                    if table == 'unsorted':
                        cursor.execute("""CREATE TABLE unsorted 
                        (unique_id TEXT PRIMARY KEY,          
                        job_title text,
                        description text)""")

                    if table == 'training':
                        cursor.execute("""CREATE TABLE training 
                        (unique_id TEXT PRIMARY KEY,          
                        label text,
                        job_title text,
                        description text)""")

                    elif table == 'metadata':
                        cursor.execute("""CREATE TABLE metadata 
                        (unique_id TEXT PRIMARY KEY,
                        search_term TEXT,
                        link TEXT, 
                        location TEXT, 
                        company TEXT, 
                        date_posted TEXT)""")

                    if table == 'results':
                        cursor.execute("""CREATE TABLE results 
                        (unique_id TEXT PRIMARY KEY,         
                        label text,
                        job_title text,
                        description text)""")
                    if table == 'model_performance_results':
                        cursor.execute("""CREATE TABLE model_performance_results 
                        (unique_id TEXT PRIMARY KEY,         
                        stemmer text,
                        vectorizer text,
                        transformer text,
                        model text,
                        f1_score REAL,
                        accuracy REAL,
                        classification_labels INT)""")
                except sqlite3.OperationalError:
                    pass

        try:
            os.mkdir(os.path.join(os.getcwd(),file_term,'models'))
        except FileExistsError:
            pass





if __name__ == '__main__':
    file_setup('Chemical Engineer')