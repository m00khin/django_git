import requests
from bs4 import BeautifulSoup
import data_client


class Parser:
    links_to_parse = [
        'https://www.kufar.by/l/mebel',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6Mn0%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6NH0%3D'
    ]
    # SQLite3
    # data_client_imp = data_client.Sqlite3Client()

    # Postres SQL
    data_client_imp = data_client.PostgresClient()

    # CSV file
    # data_client_imp = data_client.CsvClient()

    @staticmethod
    def get_mebel_by_link(link):
        response = requests.get(link)
        mebel_data = response.text

        mebel_items = []
        to_parse = BeautifulSoup(mebel_data, 'html.parser')
        for elem in to_parse.find_all('a', class_='styles_wrapper__yaLfq'):
            try:
                price, decription = elem.text.split('р.')
                mebel_items.append((
                    elem['href'],
                    int(price.replace(' ', '')),
                    decription
                ))
            except:
                print(f'Цена не была указана. {elem.text}')

        return mebel_items

    def save_to_db(self, mebel_items):
        connection = self.data_client_imp.get_connection()
        self.data_client_imp.create_mebel_table(connection)
        [self.data_client_imp.insert(connection, item[0], item[1], item[2]) for item in mebel_items]

    def run(self):
        mebel_items = []
        [mebel_items.extend(self.get_mebel_by_link(link)) for link in Parser.links_to_parse]
        self.save_to_db(mebel_items)


Parser().run()
