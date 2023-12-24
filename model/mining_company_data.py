import requests
from bs4 import BeautifulSoup
import pandas as pd

class company:
    def get_data():
        def get_table_from_wikipedia(url):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'wikitable'})
            if table is not None:
                rows = table.find_all('tr')
                header_row = rows[0]  # Assuming the first row contains the table headers
                headers = header_row.find_all('th')
                column_names = [header.text.strip() for header in headers]
                
                data = []
                for row in rows[1:]:  # Skip the header row
                    cells = row.find_all('td')
                    row_data = []
                    for cell in cells:
                        row_data.append(cell.text.strip())
                    if row_data:
                        data.append(row_data)
                return column_names, data
            else:
                return None

        def convert_table_to_csv(column_names, table_data, file_name):
            df = pd.DataFrame(table_data, columns=column_names)
            df['Symbol'] = df['Symbol'].replace('\.', '-', regex=True)
            df.to_csv(file_name, index=False, encoding='utf-8')
    
        wikipedia_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

        column_names, table_data = get_table_from_wikipedia(wikipedia_url)

        if table_data is not None:
            convert_table_to_csv(column_names, table_data, 'Data/company_data.csv')

