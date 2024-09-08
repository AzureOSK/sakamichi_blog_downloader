import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

def download_images(ct_number, output_folder_name):

    params = {
        'page': '0',
        'ct': ct_number, # 48009 etc
    }

    # response = requests.get('https://www.hinatazaka46.com/s/official/diary/member/list', params=params)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # blog_urls = soup.find_all('a', {'class': "c-button-blog-detail"})
    # blog_urls[0].get("href")

    # Get list of blog urls, list of datetimes
    blog_url_list = []
    datetime_list = []
    i = -1
    while True:
        i = i + 1
        params["page"] = i
        print(f"Parsing blog page: {i}")

        response = requests.get('https://www.hinatazaka46.com/s/official/diary/member/list', params=params)

        soup = BeautifulSoup(response.text, 'html.parser')

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

        print(f"Getting image urls from {i}: {blog_url}")

        response = requests.get(blog_url, params=params)

        soup = BeautifulSoup(response.text, 'html.parser')

        img_urls = soup.find_all('img')

        src_list = [(x.get("src"), 
                     f"{datetime_list[i]}_-_{x.get("src").split("/")[-1]}") for x in img_urls if "diary" in x.get("src")]

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
    print(download_images(ct_number = 12, output_folder_name = "miku_photos"))