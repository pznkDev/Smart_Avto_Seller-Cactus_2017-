import datetime
import json
import re


def load_file(file_name, path=''):
    """Loads data for further pre-processing
       Returns array of unique resumes"""

    cars = []
    links = set()
    with open(path + file_name) as f:
        for line in f.readlines():
            car = json.loads(line)

            if "mileage" in car.keys():
                cars.append(car)
    print("total:", len(cars))
    return cars


def get_mileage_dev(car):
    return (int(car["mileage"]) * 1000) / ((2017 - int(car["year"])) * 25000)


def get_day_views_dev(car):
    months = {"января": "1",
              "февраля": "2",
              "марта": "3",
              "апреля": "4",
              "мая": "5",
              "июня": "6",
              "июля": "7",
              "августа": "8",
              "сентября": "9",
              "октября": "10",
              "ноября": "11",
              "декабря": "12"
              }
    wdays = {"понедельник": "1",
             "вторник": "2",
             "среду": "3",
             "четверг": "4",
             "пятницу": "5",
             "субботу": "6",
             "воскресение": "7"}
    days = 0
    intersect = set(car["created"].split()) & set(months.keys())
    if intersect:
        days = datetime.date(2017, int(months[intersect.pop()]), int(car["created"].split()[0]))
        days = (datetime.date.today() - days).days
    elif "часов назад" in car["created"]:
        days = 0
    elif "вчера" in car["created"].lower():
        days = 1
    elif "в" in car["created"]:
        days = abs(int(wdays[car["created"].split()[1]]) - datetime.date.today().weekday())
    # print(days)
    return int(car["views"]) / days if days else int(car["views"])


def get_photos(car):
    return int(car["num_photos"])


def get_equip(car):
    return len(car["equip"].split()) if "equip" in car.keys() else 0


def get_ad_info(car):
    templates = ["не бит",
                 "не крашен",
                 "идеально",
                 "прекрасно",
                 "состояни",
                 "поехал",
                 "оригин",
                 "сел"
                 "вложений не требует",
                 "завел",
                 "двигатель работатет",
                 "дилер",
                 "как новый",
                 "хороший",
                 "перекуп",
                 "площадк",
                 "не беспокоить",
                 "не курил",
                 "не затертый",
                 "часики",
                 "не может",
                 "заменены"
                 "срочно",
                 "не такси",
                 "обслуж",
                 "вовремя",
                 "детали по телефону",
                 "реальний пробіг",
                 "реальный пробег",
                 "не скручен",
                 "капитал",
                 "коштив",
                 "не ставил",
                 "помен",
                 "затертый",
                 "отлич",
                 "заменен",
                 "окей",
                 "покупателям торг",
                 "новая",
                 "третій",
                 "третий",
                 "полного",
                 "возле"
                 ]
    resell = 0
    if "additional" in car.keys():
        for temp in templates:
            resell += len(re.findall(temp, car["additional"].lower()))
        return resell


def score(cars):
    scores = list()
    for car in cars:
        # if "additional" in car.keys():
        #     print(car["link"], car["additional"])
        # print(car["created"])
        curr_scores = dict()
        curr_scores["mileage_dev"] = get_mileage_dev(car)
        curr_scores["day_views"] = get_day_views_dev(car)
        curr_scores["num_photos"] = get_photos(car)
        curr_scores["equip"] = get_equip(car)
        curr_scores["ad_info"] = get_ad_info(car)
        curr_scores["link"] = car["link"]
        scores.append(curr_scores)
    return scores


def main(cars):
    scrs = score(cars)
    for dct in scrs:
        dct["score"] = dct["num_photos"] * 10 + dct["equip"] * 10
    scrs = sorted(scrs, key=lambda x: x["score"], reverse=True)
    return scrs[:4]


if __name__ == '__main__':
    crs = load_file("output.txt")
    main(crs)
    #
    # scrs = score(crs)
    # a = list()
    # for dct in scrs:
    #     a.append(dct["day_views"])
    #     #  print(dct["day_views"])
    # intersection = []
    # for i in range(len(crs) - 1):
    #     intersection = set(crs[i]["car_name"].split()) & set(crs[i + 1]["car_name"].split())
    #     # print(intersection)
    # name = "-".join([s for s in crs[0]["car_name"].split() if s in intersection]).lower()
    # mark, model = name.split("-", 1)
    # model = "-".join(model.split())
