import requests
from bs4 import BeautifulSoup

work = requests.Session()
header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0"}
url = input("Paste the link: https://www.olx.ua/d/category/city/filters: ")
def img_url():
    for i in range(1, 26):
        response = work.get((url + "?page={}").format(i), headers=header)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="css-1sw7q4x")
        for parse in data:
            try:
                name = parse.find("h6", class_="css-16v5mdi er34gjf0")
                price = parse.find("p", class_="css-10b0gli er34gjf0")
                link = parse.find("a", class_="css-rc5s2u").get("href")
                text = name.text, "\n", price.text, "\n", "https://www.olx.ua"+link, "\n"
                with open("links.txt", "a") as f:
                    f.writelines(text)
                print(name.text, "\n", price.text, "\n", "https://www.olx.ua"+link)
                yield "https://www.olx.ua"+link
            except AttributeError:
                pass

for url in img_url():
    response = work.get(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    description = soup.find("div", class_="css-bgzo2k er34gjf0")
    print(description.text, "\n")
    img = soup.find_all("div", class_="swiper-zoom-container")
    for d in img:
        im = d.find("img").get("data-src")
        if im is None:
            im = d.find("img").get("src")
        named_img = im[47:].replace("/", "_")
        print(named_img)
        with open("C:\\Users\\ThinkPad\\PycharmProjects\\parserOLX\\img\\"+named_img+".jpg", "wb") as f:
            response = work.get(im, stream=True, headers=header)
            for chuck in response.iter_content(1024):
                f.write(chuck)
img_url()