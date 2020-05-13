import sqlite3,json,os,sys
import requests

class ServerDataHandler:

    url = "http://127.0.0.1:8000/submit"
    catagories = ['unique_id', 'search_term', 'job_title', 'description', 'label', 'link', 'location',
                  'company', 'date_posted']

    def __init__(self,file_term):
        self.database = sqlite3.connect(os.path.join(os.getcwd(), file_term, f'{file_term}.db'))
        self.file_term = file_term

    def get_training_data(self):
        response = requests.get(ServerDataHandler.url, params={"search_term":str(self.file_term)})

        json_content = json.loads(response.content)
        tabulated_data = list(json_content.values())
        training_data = [tabulated_data[0],tabulated_data[4],tabulated_data[2],tabulated_data[3]]
        train = list(zip(*training_data))
        with self.database as db:
            cursor = db.cursor()
            cursor.executemany("INSERT OR REPLACE INTO training VALUES (?,?,?,?)",zip(*training_data))

    def send_training_data(self):
        with self.database as db:
            cursor = db.cursor()
            data = cursor.execute(
                """SELECT training.unique_id,metadata.search_term,training.job_title,training.description,
                training.label,metadata.link,metadata.location 
                FROM training LEFT JOIN  metadata ON training.unique_id = metadata.unique_id""").fetchall()
        data = list(zip(*data))

        json_formatted_data = {cat: (data if cat != 'search_term' else [self.file_term]*len(data)) for
                cat, data in zip(ServerDataHandler.catagories, data)}
        post_data = json.dumps(json_formatted_data)
        requests.post(ServerDataHandler.url, json=post_data)


if __name__ == '__main__':
    handler = ServerDataHandler("Entry Level Computer Programmer")
    handler.send_training_data()
    handler.get_training_data()