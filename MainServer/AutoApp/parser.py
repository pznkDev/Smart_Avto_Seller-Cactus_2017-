import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# PATH OF PHANTOMJS
driver = webdriver.PhantomJS(executable_path=r"D:\Web\ria\phantomjs-2.1.1-windows\bin\phantomjs.exe")
# browser = webdriver.Firefox(executable_path=r"C:\Users\ConcatN\anaconda3\selenium\geckodriver.exe")
driver.set_window_size(1400, 1000)


def parse_links(search_req):
    driver.get(search_req)
    time.sleep(0.5)

    # send key down event
    elem = driver.find_element_by_tag_name("body")
    for _ in range(50):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)

    # parse
    bs = BeautifulSoup(driver.page_source, "lxml")
    print("Found:", bs.select("#resultsCount .count")[0].text)
    links = bs.select("a.address")
    hrefs = set()
    for a in links:
        try:
            hrefs.add(a["href"])

        except KeyError:
            print("Error while parsing:", a)
            break
    print("Parsed links:", len(hrefs))
    return hrefs


def parse_car_details(car_link):
    # print("Source:", car_link)
    car_details = dict()
    driver.get(car_link)
    bs_car = BeautifulSoup(driver.page_source, "lxml")
    ad_name = bs_car.select("h1.head")[0]["title"]
    car_details["car_name"], car_details["year"] = ad_name.rsplit(" ", 1)
    car_details["price"] = bs_car.select("span.price")[0].text
    car_details["num_photos"] = bs_car.select("div.count-photo")[0].text.split()[2]
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
        else:
            try:  # fix it
                if "additional-data" in tag["class"]:
                    car_details["additional"] = tag.text
            except KeyError:
                # print(tag.text)
                pass
    # print(car_details)
    return car_details


def parse(search_req):
    links = parse_links(search_req)
    parsed_data = list()
    print("Parsed details:")
    for link in links:
        parsed_data.append(parse_car_details(link))
        time.sleep(1)
        print(len(parsed_data))
    return parsed_data


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
    # parse_car_details("https://auto.ria.com/auto_volkswagen_golf-iv_19677527.html")
    data = parse(req)
    for jsn in data:
        print(jsn)
