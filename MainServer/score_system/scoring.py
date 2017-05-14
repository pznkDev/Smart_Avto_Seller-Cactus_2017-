import datetime
import json
import math
import re

import numpy as np

from AutoApp import parser


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


def averagePrice(year, auto):
    avrPr = 0
    number = 0
    for i in auto:
        if int(i["year"]) == year:
            avrPr += int(i["price"].replace(' ', "")[:-1])
            number += 1

    avrPr = avrPr / number
    return avrPr


def averageMileage(year, auto):
    avrMil = 0
    number = 0
    for i in auto:
        if int(i["year"]) == year:
            try:
                avrMil += int(i["mileage"])
            except Exception:
                pass
            number += 1

    avrMil = avrMil / number
    return avrMil


def averageMilYear(yearInwork, averageMileage):
    return averageMileage/yearInwork


def setOfYear(auto):
    setYear = set()
    for i in auto:
        setYear.add(int(i["year"]))

    setYear = list(setYear)
    return setYear


def arrAvrMilYear(currentYear, auto):
    pairAvrMilY = []
    arrYr = setOfYear(auto)
    arrAvrMilYr = []

    for i in arrYr:
        arrAvrMilYr.append(averageMilYear(currentYear - i + 1,averageMileage(i, auto)))

    for i in range(len(arrYr)):
        pair = [0, 0]
        pair[0] = arrYr[i]
        pair[1] = arrAvrMilYr[i]
        pairAvrMilY.append(pair)

    return pairAvrMilY


def pairYrMilPr(pairAvrMilY, auto):
    pairYrMilPr = []
    for i in range(len(pairAvrMilY)):
        pair = []
        pair.append(pairAvrMilY[i][0])
        pair.append(pairAvrMilY[i][1])
        pair.append(averagePrice(pairAvrMilY[i][0], auto))
        pairYrMilPr.append(pair)

    return pairYrMilPr


def top(pairYrMilPr, auto):
    arrTop = []
    for i in auto:
        year = int(i["year"])
        try:
            mileage = int(i["mileage"])
        except Exception:
            mileage = 0

        price = int(i["price"].replace(' ', "")[:-1])

        pair = []
        for j in pairYrMilPr:
            if j[0] == year:
                diffPrice = math.fabs(price - j[2])
                difMilage = math.fabs(mileage - j[1])
                if math.sqrt(diffPrice*difMilage) == 0:
                    pair.append(0)
                elif 100/math.sqrt(diffPrice*difMilage) >= 3:
                    pair.append(3)
                else:
                    pair.append(100/math.sqrt(diffPrice*difMilage))

                pair.append(i['link'])
                arrTop.append(pair)

    sortArrTop = selection_sort(arrTop)
    print(sortArrTop)
    return sortArrTop


def selection_sort(arrayToSort):
    a = arrayToSort
    for i in range(len(a)):
        idxMin = i
        for j in range(i+1, len(a)):
            if a[j][0] > a[idxMin][0]:
                idxMin = j
        tmp = a[idxMin]
        a[idxMin] = a[i]
        a[i] = tmp
    return a


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
        days = abs(int(wdays[car["created"].split()[1]]) - datetime.date.today().weekday()) + 2
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
        curr_scores["day_views_dev"] = get_day_views_dev(car)
        curr_scores["num_photos"] = get_photos(car)
        curr_scores["equip"] = get_equip(car)
        if "additional" in car.keys():
            curr_scores["ad_len"] = len(car["additional"].split())
            curr_scores["ad_info"] = get_ad_info(car)
        else:
            curr_scores["ad_len"] = 0
            curr_scores["ad_info"] = 0
        curr_scores["link"] = car["link"]
        curr_scores["price"] = car["price"]
        scores.append(curr_scores)
    return scores


def main(cars):
    scrs = score(cars)
    intersection = []
    for i in range(len(cars) - 1):
        intersection = set(cars[i]["car_name"].split()) & set(cars[i + 1]["car_name"].split())
        # print(intersection)
    name = "-".join([s for s in cars[0]["car_name"].split() if s in intersection]).lower()
    mark, model = name.split("-", 1)
    #     average_price = parse_price(mark, model)[:-1].replace(" ", "")
    day_views_mean = np.mean([x["day_views_dev"] for x in scrs])
    takeData = datetime.date.today()
    currentYear = int(takeData.year)
    features_v = top(pairYrMilPr(arrAvrMilYear(currentYear, cars), cars), cars)
    print(features_v)
    i = 0
    for car_score in scrs:
        total_score = [x[0] for x in features_v if x[1] == car_score["link"]][0] * 400
        print("-"*50)
        print(car_score["link"])
        i += 1
        # mileage_dev
        total_score += car_score["mileage_dev"] * 50
        print("1", car_score["mileage_dev"] * 50)

        # price_dev
        # total_score += abs(int(average_price) - int(car_score["price"][:-1].replace(" ", ""))) / -100

        # day_views
        if day_views_mean < car_score["day_views_dev"]:
            total_score += (day_views_mean - car_score["day_views_dev"]) * 10
        print("2-", (day_views_mean - car_score["day_views_dev"]) * 10)

        # photo
        if car_score["num_photos"] < 10:
            total_score -= abs(10 - car_score["num_photos"]) * 10
            print("3", abs(10 - car_score["num_photos"]) * 10)
        elif car_score["num_photos"] > 25:
            total_score -= abs(25 - car_score["num_photos"]) * 10
            print("3-", abs(25 - car_score["num_photos"]) * 10)
        # equip
        total_score += 2 * car_score["equip"]
        print("4", 2 * car_score["equip"])

        # ad_info
        if car_score["ad_len"] < 12:
            total_score -= 40 * (12 - car_score["ad_len"])
            print("5-", 40 * (12 - car_score["ad_len"]))
        else:
            total_score += 15 * car_score["ad_len"]
            print("5-", 15 * car_score["ad_len"])

        total_score -= car_score["ad_info"] * 150
        car_score["score"] = total_score

    print(len(features_v))
    scrs = sorted(scrs, key=lambda x: x["score"], reverse=True)
    for sc in scrs:
        print(sc["score"], sc["link"])
    return scrs


if __name__ == '__main__':
    crs = load_file("output.txt")
    scrs = main(crs)

    # takeData = datetime.date.today()
    # currentYear = int(takeData.year)
    # samy = top(pairYrMilPr(arrAvrMilYear(currentYear, crs), crs), crs)
    #
    # for i in range(len(scrs)):
        # print(scrs[i]["score"], samy[i][0], scrs[i]["link"], samy[i][1])


    # print(samy)
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
    # model = "-".join(model.split())6