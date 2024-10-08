import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import argparse
import os
import sys
from loguru import logger

parser = argparse.ArgumentParser(
     prog='Hinatazaka Blog Photos Downloader',
     description="This program downloads photos from Hinatazaka blogs.")

parser.add_argument('-c', '--ct_number', type = int, help = "When you go to the page with all of the members' blogs as selected in the dropdown menu in https://www.hinatazaka46.com/s/official/diary/member?ima=0000, there will be a 'ct' number in the URL. E.g. for Kanemura Miku (https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=12) the ct number is 12")
parser.add_argument('-d', '--download_location', type = str, help = r"The download location for the downloaded messages; can be relative or absolute. E.g. 'C:\Users\<your username>\Downloads\osushi_photos' or just 'osushi_photos'")
parser.add_argument('-l', '--log_filename', type = str, help = "Filename to be used for the logfile e.g. 'hinatazaka_blog_downloader_log.txt'; if unspecified, there will be no logfile.")
args = parser.parse_args()
CT_NUMBER = args.ct_number
OUTPUT_FOLDER_PATH = args.download_location
LOG_FILENAME = args.log_filename

logger.remove(0) # Remove default logger so that we can set stderr to TRACE
if LOG_FILENAME is not None:
    logger.add(Path(OUTPUT_FOLDER_PATH)/LOG_FILENAME, level="INFO")
    logger.add(sys.stderr, level="TRACE")
else:
    logger.add(sys.stderr, level="TRACE")

logger.info(f"Run on {datetime.now()}")

def download_images(ct_number, output_folder_path):

    params = {
        'page': '0',
        'ct': ct_number, # 48009 etc
    }

    # If output_folder_path is None, set current working directory as output path
    if output_folder_path is None:
        output_folder_path = Path(os.getcwd())

    # If ct_number is None, download all available member blogs
    if ct_number is None:
        response = requests.get('https://www.hinatazaka46.com/s/official/diary/member')
        soup = BeautifulSoup(response.text, 'html.parser')
        member_blog_list = [
            (
                x.text.split("(")[0], 
                x.get("value").split("ct=")[-1]
            ) for x in soup.find('select', {'name': "member_select"}).find_all('option')
            if x.get("value").split("ct=")[-1] != ""
            ]
        
        for member_name, ct_number in member_blog_list:
            logger.info(f"Downloading {member_name}")
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
            logger.trace(f"Parsing blog page: {i}")

            response = requests.get('https://www.hinatazaka46.com/s/official/diary/member/list', params=params)

            soup = BeautifulSoup(response.text, 'html.parser')

            # Get member name for use in folder name
            if i == 0:
                member_name = soup.find('div', {'class': "c-blog-member__name"}).text.strip()

            blog_urls = soup.find_all('a', {'class': "c-button-blog-detail"})

            # End of pages
            if len(blog_urls) == 0:
                break

            href_list = [f"https://www.hinatazaka46.com{x.get("href")}" for x in blog_urls]
            blog_url_list.extend(href_list)

            blog_dates = soup.find_all('div', {'class': "c-blog-article__date"})
            fix_datetimes = lambda x: datetime.strptime(x.replace("\n", "").strip(), '%Y.%m.%d %H:%M').strftime('%Y_%m_%d_-_%H_%M')
            datetimes = [fix_datetimes(x.text) for x in blog_dates]
            datetime_list.extend(datetimes)

        # For each blog url, get list of image urls in the form of tuple (image url, date_time_-_imagename.ext)
        img_url_list = []
        for i, blog_url in enumerate(blog_url_list):

            logger.trace(f"Getting image urls from {i}: {blog_url}")

            blog_id = blog_url.split("/")[-1].split("?")[0]

            response = requests.get(blog_url)

            soup = BeautifulSoup(response.text, 'html.parser')

            img_urls = soup.find_all('img')

            img_urls = [x for x in img_urls if x.has_attr("src")]

            src_list = [(x.get("src"), 
                        f"{datetime_list[i]}_-_{blog_id}_-_{x.get("src").split("/")[-1]}") for x in img_urls if "diary" in x.get("src")]

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
                    logger.trace(f"Downloading {img_url} to {output_file_path.resolve()}")
                    image = requests.get(img_url)
                    with open(output_file_path, 'wb') as f:
                        f.write(image.content)
                    photos_downloaded += 1
                except:
                    logger.debug(f"Couldn't download {img_url}!")
                    continue
            else:
                logger.debug(f"Not downloading {img_url} as {filename} already exists in {output_folder_path.resolve()}!")

        logger.info(f"{photos_downloaded} photos downloaded to {output_folder_path.resolve()}!")

    return None

if __name__ == "__main__":
    download_images(CT_NUMBER, OUTPUT_FOLDER_PATH)
    # download_images(ct_number = 12, output_folder_name = "miku_photos")