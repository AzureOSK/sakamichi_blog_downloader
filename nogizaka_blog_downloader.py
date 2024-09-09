import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(
     prog='Nogizaka Blog Photos Downloader',
     description="This program downloads photos from Nogizaka blogs.")

parser.add_argument('-c', '--ct_number', type = int, help = "When you go to the page with all of the members' blogs as selected in the dropdown menu in https://www.nogizaka46.com/s/n46/diary/MEMBER, there will be a 'ct' number in the URL. E.g. for Sugawara Satsuki (https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=0520&ct=55391) the ct number is 55391")
parser.add_argument('-d', '--download_location', type = str, help = r"The download location for the downloaded messages; can be relative or absolute. E.g. 'C:\Users\<your username>\Downloads\satsuki_photos' or just 'satsuki_photos'")
args = parser.parse_args()
CT_NUMBER = args.ct_number
OUTPUT_FOLDER_PATH = args.download_location

def download_images(ct_number, output_folder_path):

    params = {
        'page': '0',
        'ct': ct_number, # 48009 etc
    }

    # response = requests.get('https://www.nogizaka46.com/s/n46/diary/MEMBER/list', params=params, cookies=cookies, headers=headers)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # blog_urls = soup.find_all('a', {'class': "bl--card js-pos a--op hv--thumb"})
    # blog_urls[0].get("href")

    # Get list of blog urls, list of datetimes
    blog_url_list = []
    datetime_list = []
    i = -1
    while True:
        i = i + 1
        params["page"] = i
        print(f"Parsing blog page: {i}")

        response = requests.get('https://www.nogizaka46.com/s/n46/diary/MEMBER/list', params=params)

        soup = BeautifulSoup(response.text, 'html.parser')

        blog_urls = soup.find_all('a', {'class': "bl--card js-pos a--op hv--thumb"})

        # End of pages
        if blog_urls[0].find('p', {'class': "bl--card__ttl"}).text == '該当するデータがございません':
            break

        href_list = [f"https://www.nogizaka46.com{x.get("href")}" for x in blog_urls]
        blog_url_list.extend(href_list)

        fix_datetimes = lambda x: datetime.strptime(x.replace("\n", "").strip(), '%Y.%m.%d %H:%M').strftime('%Y_%m_%d_-_%H_%M')
        datetimes = [fix_datetimes(x.find('p', {'class': "bl--card__date"}).text) for x in blog_urls]
        datetime_list.extend(datetimes)

    # For each blog url, get list of image urls in the form of tuple (image url, date_time_-_imagename.ext)
    img_url_list = []
    for i, blog_url in enumerate(blog_url_list):

        print(f"Getting image urls from {i}: {blog_url}")

        blog_id = blog_url.split("/")[-1].split("?")[0]

        response = requests.get(blog_url, params=params)

        soup = BeautifulSoup(response.text, 'html.parser')

        img_urls = soup.find_all('img')

        src_list = [(f"https://www.nogizaka46.com{x.get("src")}", 
                    f"{datetime_list[i]}_-_{blog_id}_-_{x.get("src").split("/")[-1]}") for x in img_urls if x.get("src") is not None]

        img_url_list.extend(src_list)

    # Create output folder if folder does not exist
    output_folder_path = Path(output_folder_path)
    output_folder_path.mkdir(parents=True, exist_ok=True)

    photos_downloaded = 0

    # For each img_url and filename combination, save 
    for (img_url, filename) in reversed(img_url_list):
        
        output_file_path = output_folder_path/filename

        # If file doesn't exist, downloadit, else print info and don't download
        if not output_file_path.is_file():
            image = requests.get(img_url)
            print(f"Downloading {img_url} to {output_file_path.resolve()}")
            with open(output_file_path, 'wb') as f:
                f.write(image.content)
            photos_downloaded += 1
        else:
            print(f"Not downloading {img_url} as {filename} already exists in {output_folder_path.resolve()}!")

    print(f"{photos_downloaded} photos downloaded to {output_folder_path.resolve()}!")

    return None

if __name__ == "__main__":
    download_images(CT_NUMBER, OUTPUT_FOLDER_PATH)
    # download_images(ct_number = 55391, output_folder_path = "satsuki_photos")