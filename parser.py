import json
from bs4 import BeautifulSoup
import requests


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}

#count = 0
#all_url={}
#for namber_url in range(1,115):
    #url = f"https://hi-tech.news/page/{namber_url}/"
    #rep = requests.get(url)
    #soup = BeautifulSoup(rep.text, "lxml")
    #all_url_in_list = soup.find_all("div", class_ = "read-more-wrap")
    #for url_in_list in all_url_in_list:
        #count += 1
        #url = url_in_list.find("a").get("href")
        #print(count)
        #all_url[count] = url
#with open("all_url.json","w",encoding="utf-8") as file:
    #json.dump(all_url, file, indent=4, ensure_ascii=False)
def get_info_in_url(all_url):
    main_url = "https://hi-tech.news/"
    result_data = []
    count = 0
    for number_articles, url_articles in all_url.items():
        count += 1
        rep = requests.get(url_articles, headers=headers)
        soup = BeautifulSoup(rep.text,"lxml")
        main_div_articles = soup.find("div",class_ = "post")
        articles_url_img = main_url + main_div_articles.find("div", class_ = "post-media-full").find("img").get("src")
        date_publication = main_div_articles.find("div", class_ = "tile-meta").find("div", class_ = "tile-views").text
        title_articles = main_div_articles.find("div", class_ = "post-content").find("h1").text
        main_text_articles = main_div_articles.find("div", class_ = "post-content").find("div", class_ = "the-excerpt").text
        print(f"Обработал {number_articles}/3404")

        result_data.append(
            {
                "articles_url_img": articles_url_img,
                "date_publication": date_publication,
                "title_articles":title_articles,
                "main_text_articles":main_text_articles
            }
        )
    with open("all_info.json","w", encoding="utf-8") as jsonfile:
        json.dump(result_data, jsonfile, indent=4, ensure_ascii=False)
    print("Работу завершил сэр.")




def main():
    with open("all_url.json", encoding="utf-8") as file:
        all_url = json.load(file)
        get_info_in_url(all_url)




if __name__=="__main__":
    main()





