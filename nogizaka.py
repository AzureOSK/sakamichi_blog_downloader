import requests
from bs4 import BeautifulSoup

def download_images(ct_number, output_folder_name):

    cookies = {
        'WAPID': 'no9pUG4vBB3d9E2xt0TMTtm50wOYfrQKMir',
        'wap_last_event': 'showWidgetPage',
        'wovn_selected_lang': 'ja',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ja;q=0.8,de;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': 'WAPID=no9pUG4vBB3d9E2xt0TMTtm50wOYfrQKMir; wap_last_event=showWidgetPage; wovn_selected_lang=ja',
        'dnt': '1',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    params = {
        # 'ima': '0029',
        'page': '0',
        'ct': ct_number, # 48009 etc
        # 'cd': 'MEMBER',
    }

    # response = requests.get('https://www.nogizaka46.com/s/n46/diary/MEMBER/list', params=params, cookies=cookies, headers=headers)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # blog_urls = soup.find_all('a', {'class': "bl--card js-pos a--op hv--thumb"})
    # blog_urls[0].get("href")

    blog_url_list = []
    datetime_list = []
    i = -1
    while True:
        i = i + 1
        params["page"] = i
        print(f"Page: {i}")

        response = requests.get('https://www.nogizaka46.com/s/n46/diary/MEMBER/list', params=params, cookies=cookies, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')

        blog_urls = soup.find_all('a', {'class': "bl--card js-pos a--op hv--thumb"})

        # End of pages
        if blog_urls[0].find('p', {'class': "bl--card__ttl"}).text == '該当するデータがございません':
            break

        href_list = [f"https://www.nogizaka46.com{x.get("href")}" for x in blog_urls]
        blog_url_list.extend(href_list)

        datetimes = [x.find('p', {'class': "bl--card__date"}).text.replace(".", "_").replace(" ", "_-_").replace(":", "_") for x in blog_urls]
        datetime_list.extend(datetimes)

    img_url_list = []
    for i, blog_url in enumerate(blog_url_list):

        print(blog_url)

        response = requests.get(blog_url, params=params, cookies=cookies, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')

        img_urls = soup.find_all('img')

        src_list = [(f"https://www.nogizaka46.com{x.get("src")}", 
                    f"{datetime_list[i]}_-_{x.get("src").split("/")[-1]}") for x in img_urls]

        img_url_list.extend(src_list)

    for (img_url, filename) in img_url_list:
        image = requests.get(img_url)

        with open(f"./{output_folder_name}/{filename}", 'wb') as f:
            f.write(image.content)

    return f"Photos downloaded to {output_folder_name}!"

if __name__ == "__main__":
    download_images(ct_number = 48014, output_folder_name = "rei_photos")