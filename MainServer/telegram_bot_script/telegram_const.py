token = ""

msg_greeting = '''\r
    Hello, my name is *SmartAvtoSeller* and i will help you to choose your dream-car. \n *Do you want to try ?*
    '''

msg_in_mark = '''\r
    _Enter mark:_
    '''

msg_wrong_mark = '''\r
    Sorry, but no mark with name _"%s"_ in our database. Perhaps you looked for *"%s"* 
'''

msg_in_model = '''\r
    _Enter model:_
    '''

msg_wrong_model = '''\r
    Sorry, but no model with name _"%s"_ in our database. Perhaps you looked for *"%s"* 
'''

msg_in_region = '''\r
    _Enter region:_
    '''

msg_confirm_search = '''\r
    Do you want to search with following params:
    mark: *%s*
    model: *%s*
    region: *%s* ?
    '''

msg_cancel = '''\r
    What a *pity*. Perhaps another time :) \nTo start again print *'hello'*.
'''

all_marks = ['Chevrolet', 'Fiat', 'Daewoo', 'kia', 'Opel']
all_models = ['1', '2', '3', '4']
all_regions = ['1', '2', '3', '4']

state_init = 'state_init'
state_start = 'state_start'
state_in_mark = 'state_in_mark'
state_in_model = 'state_in_model'
state_in_region = 'state_in_type'
state_confirm_search = 'state_confirm'

