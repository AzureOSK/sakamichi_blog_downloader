# Sakamichi Blog Photos Downloader

## How to use
1. Download the .exe into any PATH folder.
    - If you don't know what this means, put the .exe into `C:\Users\<your username>`
2. In cmd or powershell, cd into the folder that you downloaded the .exe into.
    - If you don't know what this means, run the command `cd "C:\Users\<your username>"` in cmd or powershell

## Parameters
- `--ct_number`: The ct number as specified in the url of a member's blog page (see below)
- `--download_location`: The location of where the photos will be saved. This can be a relative or absolute path.

## If downloading photos from a single Nogizaka member's blog
1. Go to [https://www.nogizaka46.com/s/n46/diary/MEMBER?ima=0955](https://www.nogizaka46.com/s/n46/diary/MEMBER?ima=0955)
2. Select the member from whose blog you want to download photos from using the dropdown menu.
3. Look at the url bar, e.g. for Sugawara Satsuki her url is [https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=2021&ct=55391](https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=2021&ct=55391)
4. This means her ct_number is `55391`.
5. In cmd or powershell, run `./nogizaka_blog_downloader.exe --ct_number 55391 --download_location "nogizaka_blog_photos"`
    - You can also run `./nogizaka_blog_downloader.exe --ct_number 55391 --download_location "C:\Users\<your username>\nogizaka_blog_photos"`
6. Press Enter and let the script run, and when it finishes, all the photos should be downloaded to the location specified in `--download_location`

## If downloading photos from a single Hinatazaka member's blog
1. Go to [https://www.hinatazaka46.com/s/official/diary/member?ima=0000](https://www.hinatazaka46.com/s/official/diary/member?ima=00005)
2. Select the member from whose blog you want to download photos from using the dropdown menu.
3. Look at the url bar, e.g. for Sugawara Satsuki her url is [https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=12](https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=12)
4. This means her ct_number is `12`.
5. In cmd or powershell, run `./hinatazaka_blog_downloader.exe --ct_number 12 --download_location "hinatazaka_blog_photos"`
    - You can also run `./hinatazaka_blog_downloader.exe --ct_number 12 --download_location "C:\Users\<your username>\hinatazaka_blog_photos"`
6. Press Enter and let the script run, and when it finishes, all the photos should be downloaded to the location specified in `--download_location`

## If downloading photos from every member's blog
1. In cmd or powershell, run `./nogizaka_blog_downloader.exe` or `./hinatazaka_blog_downloader.exe` without the ct_number parameter.
    - E.g. `./nogizaka_blog_downloader.exe --download_location nogizaka_blog_photos` or `./hinatazaka_blog_downloader.exe --download_location hinatazaka_blog_photos`