import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import argparse
import os

parser = argparse.ArgumentParser(
     prog='Sakurazaka Blog Photos Downloader',
     description="This program downloads photos from Sakurazaka blogs.")

parser.add_argument('-c', '--ct_number', type = int, help = "When you go to the page with all of the members' blogs as selected in the dropdown menu in https://sakurazaka46.com/s/s46/diary/blog/list?ima=0000, there will be a 'ct' number in the URL. E.g. for Moriya Rena (https://sakurazaka46.com/s/s46/diary/blog/list?ima=0000&ct=58) the ct number is 58")
parser.add_argument('-d', '--download_location', type = str, help = r"The download location for the downloaded messages; can be relative or absolute. E.g. 'C:\Users\<your username>\Downloads\rena_photos' or just 'rena_photos'")
args = parser.parse_args()
CT_NUMBER = args.ct_number
OUTPUT_FOLDER_PATH = args.download_location

def download_images(ct_number, output_folder_path):

    params = {
        'page': '5',
        'ct': ct_number, # 48009 etc
    }

    # If output_folder_path is None, set current working directory as output path
    if output_folder_path is None:
        output_folder_path = Path(os.getcwd())

    # If ct_number is None, download all available member blogs
    if ct_number is None:
        response = requests.get('https://sakurazaka46.com/s/s46/diary/blog/list')
        soup = BeautifulSoup(response.text, 'html.parser')
        member_blog_list = [
            (
                x.text.split("(")[0], 
                x.get("value").split("ct=")[-1]
            ) for x in soup.find('select', {'name': "member_select"}).find_all('option')
            if x.get("value").split("ct=")[-1] != ""
            ]
        
        for member_name, ct_number in member_blog_list:
            print(f"Downloading {member_name}")
            download_images(ct_number, output_folder_path)

    # Else, if ct_number is not None, download only photos from one member
    else:
        # Get list of blog urls, list of datetimes
        blog_url_list = []
        datetime_list = []
        i = -1
        while True:
            i = i + 1
            params["page"] = i
            print(f"Parsing blog page: {i}")

            response = requests.get('https://sakurazaka46.com/s/s46/diary/blog/list', params=params)

            soup = BeautifulSoup(response.text, 'html.parser')

            # Get member name for use in folder name
            if i == 0:
                member_name = soup.find('dt', {'class': "name"})
                member_name.span.decompose()
                member_name = member_name.get_text(strip=True)
            
            # End of pages
            if soup.find('ul', {'class': "com-blog-part box3 fxpc"}) == None:
                break

            blog_urls = soup.find('ul', {'class': "com-blog-part box3 fxpc"}).find_all('a')

            href_list = [f"https://www.hinatazaka46.com{x.get("href")}" for x in blog_urls]
            blog_url_list.extend(href_list)

            # blog_dates = soup.find_all('div', {'class': "blog-foot"})
            # fix_datetimes = lambda x: datetime.strptime(x.replace("\n", "").strip(), '%Y.%m.%d %H:%M').strftime('%Y_%m_%d_-_%H_%M')
            # datetimes = [fix_datetimes(x.text) for x in blog_dates]
            # datetime_list.extend(datetimes)

        # For each blog url, get list of image urls in the form of tuple (image url, date_time_-_imagename.ext)
        img_url_list = []
        for i, blog_url in enumerate(blog_url_list):

            print(f"Getting image urls from {i}: {blog_url}")

            blog_id = blog_url.split("/")[-1].split("?")[0]

            response = requests.get(blog_url)

            soup = BeautifulSoup(response.text, 'html.parser')

            img_urls = soup.find("div", {'class':"box-article"}).find_all('img')

            img_urls = [x for x in img_urls if x.has_attr("src")]

            fix_datetimes = lambda x: datetime.strptime(x.replace("\n", "").strip(), '%Y/%m/%d %H:%M').strftime('%Y_%m_%d_-_%H_%M')
            blog_datetime = fix_datetimes(soup.find("div", {"class":"blog-foot"}).find("p", {"class": "date wf-a"}).text)

            src_list = [(f"https://sakurazaka46.com/{x.get("src")}", 
                        f"{blog_datetime}_-_{blog_id}_-_{x.get("src").split("/")[-1]}") for x in img_urls]

            img_url_list.extend(src_list)

        # Create output folder if folder does not exist
        output_folder_path = Path(output_folder_path)/member_name
        output_folder_path.mkdir(parents=True, exist_ok=True)

        photos_downloaded = 0

        # For each img_url and filename combination, save 
        for (img_url, filename) in reversed(img_url_list):
            
            output_file_path = output_folder_path/filename

            # If file doesn't exist, download it, else print info and don't download
            if not output_file_path.is_file():
                try:
                    print(f"Downloading {img_url} to {output_file_path.resolve()}")
                    image = requests.get(img_url)
                    with open(output_file_path, 'wb') as f:
                        f.write(image.content)
                    photos_downloaded += 1
                except:
                    print(f"Couldn't download {img_url}!")
                    continue
            else:
                print(f"Not downloading {img_url} as {filename} already exists in {output_folder_path.resolve()}!")

        print(f"{photos_downloaded} photos downloaded to {output_folder_path.resolve()}!")

    return None

if __name__ == "__main__":
    download_images(CT_NUMBER, OUTPUT_FOLDER_PATH)
    # download_images(ct_number = 58, output_folder_name = "rena_photos")