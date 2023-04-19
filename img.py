import requests
from time import time


def get_file(i, url):
    print(f"getting file number {i}")
    r = requests.get(url, allow_redirects=True)
    write_file(i, r)


def write_file(i, response):
    print(f"writing file number {i}")
    filename = response.url.split('/')[-1]
    with open(f'./img/{filename}', 'wb') as file:
        file.write(response.content)


def main():
    url = 'https://loremflickr.com/640/480'
    for i in range(30):
        get_file(i, url)


if __name__ == '__main__':
    t0 = time()
    main()
    print(f'{time() - t0} seconds')