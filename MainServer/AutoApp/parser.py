import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import score_system.scoring as scoring

# PATH OF PHANTOMJS
# driver = webdriver.PhantomJS(executable_path=r"D:\Web\ria\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver = webdriver.Firefox()
driver.set_window_size(1400, 1000)


def parse_price(mark, model):
    req = "https://auto.ria.com/car/{0}/{1}/price/".format(mark, model)
    driver.get(req)
    bs_p = BeautifulSoup(driver.page_source, "lxml")
    return bs_p.select(".price-wrap .i-block")[0].text


def parse_links(search_req):
    driver.get(search_req)
    time.sleep(1)

    # send key down event
    elem = driver.find_element_by_tag_name("body")
    for _ in range(40):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    # parse
    bs = BeautifulSoup(driver.page_source, "lxml")
    print("Found:", bs.select("#resultsCount .count")[0].text)
    links = bs.select("a.address")
    hrefs = set()
    for a in links:
        try:
            if "https://auto.ria.com" not in a["href"]:
                continue
            hrefs.add(a["href"])

        except KeyError:
            print("Error while parsing:", a)
            break
    print("Parsed links:", len(hrefs))
    return list(hrefs)[:10]


def parse_car_details(car_link):
    # print("Source:", car_link)
    car_details = dict()
    try:
        car_details["link"] = car_link
        driver.get(car_link)
        time.sleep(2)
        bs_car = BeautifulSoup(driver.page_source, "lxml")
        ad_name = bs_car.select("h1.head")[0]["title"]
        car_details["car_name"], car_details["year"] = ad_name.rsplit(" ", 1)
        car_details["price"] = bs_car.select("span.price")[0].text
        car_details["num_photos"] = bs_car.select("div.count-photo")[0].text.split()[2]
        dates = bs_car.select("div.item.created")
        for tag in dates:
            tag_str = tag.text.lower()
            if "зарегистрирован" in tag_str:
                car_details["registered"] = tag.text.rsplit(" ", 1)[1]

        descr = bs_car.select("#description dd")
        for tag in descr:
            tag_str = tag.text.lower().strip()
            if ":" in tag_str:
                if "читать еще скрыть" in tag_str:
                    tag_str = tag_str.replace("читать еще скрыть", "")
                slice_from = tag_str.index(":") + 1
                if "пробег:" in tag_str:
                    car_details["mileage"] = tag_str[slice_from: tag_str.index("тыс")]
                elif "город:" in tag_str:
                    car_details["city"] = tag_str[slice_from:]
                elif "состояние" in tag_str:
                    car_details["condition"] = tag_str[slice_from:]
                elif "безопасность" in tag_str or \
                        "комфорт" in tag_str or\
                        "мультимедиа" in tag_str:
                    if "equip" not in car_details.keys():
                        car_details["equip"] = tag_str[slice_from:]
                    else:
                        car_details["equip"] += " " + tag_str[slice_from:]
            elif tag.attrs:
                if "additional-data" in tag["class"]:
                        car_details["additional"] = tag.text
        car_details["views"] = bs_car.select("#advViews")[0].text
        car_details["created"] = " ".join(bs_car.select(".i-block.date-add")[0]["title"].split()[2:])
    except Exception:
        print("Error while parsing", car_link)
        return None
    return car_details


def parse(search_req):
    links = parse_links(search_req)
    parsed_data = list()
    print("Parsed details:")
    f = open("output.txt", "w")
    for link in links:
        parsed_car = parse_car_details(link)
        if parsed_data is not None:
            parsed_data.append(parsed_car)
        # time.sleep(2)
        json.dump(parsed_car, f)
        f.write("\n")
        print(len(parsed_data))
        print(link)

    results = scoring.main(parsed_data)
    return results


if __name__ == '__main__':
    req = "https://auto.ria.com/search/?" \
          "category_id=1&" \
          "marka_id=84&" \
          "model_id=30786&" \
          "state%5B0%5D=10&" \
          "s_yers%5B0%5D=0&" \
          "po_yers%5B0%5D=0&" \
          "price_ot=&" \
          "price_do=&" \
          "currency=1&" \
          "countpage=100"

    # parse_car_details("https://auto.ria.com/auto_volkswagen_golf-iv_18475652.html")
    data = parse(req)
    # for jsn in data:
    #     print(jsn)