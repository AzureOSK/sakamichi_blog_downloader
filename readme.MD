# Sakamichi Blog Photos Downloader

## How to use
1. Download the .exe into any PATH folder.
    - If you don't know what this means, put the .exe into `C:\Users\<your username>`
2. In cmd or powershell, cd into the folder that you downloaded the .exe into.
    - If you don't know what this means, run the command `cd "C:\Users\<your username>"` in cmd or powershell

## If downloading photos from a Nogizaka blog
1. Go to [https://www.nogizaka46.com/s/n46/diary/MEMBER?ima=0955](https://www.nogizaka46.com/s/n46/diary/MEMBER?ima=0955)
2. Select the member from whose blog you want to download photos from using the dropdown menu.
3. Look at the url bar, e.g. for Sugawara Satsuki her url is [https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=2021&ct=55391](https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=2021&ct=55391)
4. This means her ct_number is `55391`.
5. In cmd or powershell, run `./nogizaka_blog_downloader --ctnumber 55391 --download_location "satsuki_photos"`
    - You can also run `./nogizaka_blog_downloader --ctnumber 55391 --download_location "C:\Users\<your username>\satsuki_photos"`
6. Press Enter and let the script run, and when it finishes, all the photos should be downloaded to the locatuion specified in `--download_location`

## If downloading photos from a Hinatazaka blog
1. Go to [https://www.hinatazaka46.com/s/official/diary/member?ima=0000](https://www.hinatazaka46.com/s/official/diary/member?ima=00005)
2. Select the member from whose blog you want to download photos from using the dropdown menu.
3. Look at the url bar, e.g. for Sugawara Satsuki her url is [https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=12](https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=12)
4. This means her ct_number is `12`.
5. In cmd or powershell, run `./hinatazaka_blog_downloader --ctnumber 12 --download_location "osushi_photos"`
    - You can also run `./hinatazaka_blog_downloader --ctnumber 12 --download_location "C:\Users\<your username>\osushi_photos"`
6. Press Enter and let the script run, and when it finishes, all the photos should be downloaded to the locatuion specified in `--download_location`