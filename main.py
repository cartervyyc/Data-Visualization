import concurrent.futures
import matplotlib
# Important to disable the GUI before importing pyplot
matplotlib.use('Agg') # Disables the GUI from matplotlib, which creates a limitation to using multiple threads and using matplotlib
from matplotlib import pyplot as plt
import csv
import time
from collections import defaultdict, Counter

prices = []
dates = []

city_price_map = defaultdict(list) # Generate a dictonary
city_date_map = defaultdict(list)

city_counter = Counter()

def read_data():
    global city_price_map, city_date_map, unique_cities

    t1 = time.perf_counter()
    with open('202304.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        print(csv_reader.fieldnames)

        for line in csv_reader:
            city = line[" 'Town/City'"]

            if city:
                city_counter[city] += 1

            try:
                price = float(line[" 'price'"])
                city_price_map[city].append(price)
            except ValueError:
                pass # Skips any poor data

            try:
                date = line[" 'Date_of_Transfer'"]
                year = int(date[:4])
                city_date_map[city].append(year)
            except ValueError:
                pass  # Skips any poor data


    # List comprehension for 2- most common cities
    # Lists over each tuple and unpacks the city name and count into variables city, and count
    unique_cities = [city for city, count in city_counter.most_common(20)]

    print(city_price_map)
    print(city_date_map)

    t2 = time.perf_counter()
    print(f"Completed in {t2-t1} seconds")

def visualize_data(city):
    plt_years = city_date_map[city]
    plt_prices = city_price_map[city]

    if not plt_years or not plt_prices:
        # Missing data
        print(f"Skipping {city}, missing data")
        return

    if len(plt_years) != len(plt_prices):
        # Incorrect amounts of data
        print(f"Skipping {city}, data mismatch")
        return

    print(f"Generating plot for {city}")

    fig = plt.figure()
    plt.scatter(plt_years, plt_prices, s=10, alpha=0.5)
    plt.title(city)
    plt.xlabel("Year")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.savefig(f"{city}.png")
    plt.close(fig) # Important - close the figure for thread safety and memory issues

if __name__ == "__main__":
    read_data()

    print(unique_cities)
    process_graphs = input("Enter any key to continue: ")

    t1 = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("Processing Graphs...")
        executor.map(visualize_data, unique_cities)

    t2 = time.perf_counter()

    print(f"Finished in {t2-t1} seconds")


