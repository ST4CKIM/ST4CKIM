from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

def get_url_today(institute, course, groub):
    try:
        driver = webdriver.Chrome()
        url = "http://www.mstu.edu.ru/study/timetable/"
        driver.get(url)
        driver.find_element(By.XPATH, f"""//*[@id="dd1"]/form/p/select[2]/option[{institute}]""").click()
        driver.find_element(By.XPATH, f"""//*[@id="dd1"]/form/p/select[3]/option[{course}]""").click()
        driver.find_element(By.XPATH, """//*[@id="dd1"]/form/p/button""").click()
        html = driver.page_source
        driver.close()
        soup = BeautifulSoup(html, "lxml")
        all_elemets_table = soup.find("tbody").find_all("tr")
        for element_table in all_elemets_table:
            name_groub = element_table.find("a", class_="btn-default").text
            if groub == name_groub:
                url_groub = url + element_table.find("a",class_ = "btn-default").get("href")
                return (url_groub)
    except Exception as ex:
        print(ex)

def get_timetable(url):
    rep = requests.get(url)
    soup = BeautifulSoup(rep.text,"lxml")
    all_day_on_week = soup.find("div", class_="table-row")
    c = 0
    for day_week in all_day_on_week:
        c += 1
        if c == 7:
            break
        else:
            title_day = day_week.find("tr").text
            print()
            print(title_day)
            print()
            paras = day_week.find_all("tr")
            all_day_raspisanie = []
            for para in paras[1:]:
                elements_para = para.find_all("td")
                namber = ""
                predmet = ""
                prepodovatel = ""
                mesto = ""
                count = 0
                for element in elements_para:
                    pip = "\xa0"

                    celemnt = element.text
                    if pip in celemnt:
                        celemnt = celemnt.replace(pip,"")
                    s = ""
                    if celemnt != s:
                        count +=1
                        if count == 1:
                            namber = celemnt
                        elif count == 2:
                            predmet = celemnt
                        elif count == 3:
                            prepodovatel = celemnt
                        elif count == 4:
                            mesto = celemnt
                data = {
                    "Номер пары":namber,
                    "Предмет": predmet,
                    "Преподаватель": prepodovatel,
                    "Номер аудитории": mesto
                }
                all_day_raspisanie.append(data)

        with open(f"data/{title_day}.json", "w", encoding="utf-8") as file:
            json.dump(all_day_raspisanie, file, indent=4, ensure_ascii=False)











def main():
    #institute = input("Введите ваш институт:")
    #institute = institute.lower()
    #course = int(input("Введите ваш курс:")) + 1
    #groub = input("Введите вашу группу:")
    #groub = groub.lower()
    #if course<2 or course>8:
        #print("Чел на данный момент существует только 7 курсов.... головой думай")
        #exit()
    #else:
        #course = str(course)

    #if institute == "ети":
        #institute = "2"
    #elif institute == "има":
        #institute = "3"
    #elif institute == "аф":
        #institute = "4"
    #elif institute == "иат":
        #institute = "5"


    institute = "5"
    course = "2"
    groub = "ПИб21о-1"
    url = get_url_today(institute, course, groub)
    print(url)
    get_timetable(url)


if __name__=="__main__":
    main()




