from django.http import HttpResponse

from AutoApp.db_filling import fill_database
from AutoApp.parser import parse
import telegram_bot_script.telegram_main as telegram

# Create your views here.


def load(request):
    print('start filling database')
    fill_database()
    return HttpResponse("hello, files loading success")


def parse_test(request):
    r = "https://auto.ria.com/search/?" \
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
    # parser.parse(r)
    return HttpResponse(parse(r))


def start_bot(request):
    telegram.start_telegram_bot()

    return HttpResponse("hello, files loading success")
