import matplotlib.pyplot as plt
import sys
import os

sys.path.append('src/data')

import dataset

def graph_stock_over_time(data):
    plt.figure(figsize=(16, 8))

    date_points = [dat['date'] for dat in data]
    adj_close_prices = [dat['adj_close'] * 1.44 for dat in data]

    plt.plot(date_points, adj_close_prices, label='Prix', color='red')

    plt.title('Prix des actions Tesla (de 2021 à 2024)')
    plt.xlabel('Date')
    plt.ylabel('Prix (en dollars canadien)')

    plt.legend()
    plt.tight_layout()

    path = 'outputs/prix_des_actions_tesla.png'
    plt.savefig(path)
    plt.close()

    print(f'Saved line graph to path: {path}')



if __name__ == '__main__':
    os.makedirs('outputs', exist_ok=True)

    data = dataset.get_data()

    graph_stock_over_time(data)