import requests

from AutoApp.models import Region, Mark, Model


def fill_database():

    Mark.objects.all().delete()
    Model.objects.all().delete()

    # ### REGION LIST --------------------------------------------
    # regions = requests.get("http://api.auto.ria.com/states")
    # regions_list = regions.json()
    # for region in regions_list:
    #     region_new = Region(value_id=region['value'], name=region['name'])
    #     region_new.save()


    ### MARK LIST ----------------------------------------------
    marks = requests.get("http://api.auto.ria.com/categories/1/marks")
    marks_list = marks.json()
    for mark in marks_list:
        mark_new = Mark(value_id=mark['value'], name=mark['name'])
        mark_new.save()


    ### MODEL LIST ----------------------------------------------
    marks = requests.get("http://api.auto.ria.com/categories/1/marks")
    marks_list = marks.json()

    for mark in marks_list:
        mark_id = mark["value"]
        model_str = "http://api.auto.ria.com/categories/1/marks/{0}/models".format(mark_id)
        models = requests.get(model_str)
        models_list = models.json()
        if not models_list:
            continue
        for model in models_list:
            model_new = Model(value_id=model['value'], mark_id=mark['name'], name=model['name'])
            model_new.save()
