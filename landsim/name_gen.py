_pre = ["West ", "East ", "North ", "South ", "Little ", "Greater ",
        "Upper ", "Lower ", "King's "]

_first = [ "Ash", "Bur", "Dor", "Castle", "Berk", "Dun", "Al", "Temple",
           "Roch", "Ave", "Bar", "Ban", "Port", "Heath", "Farn", "Whit",
           "Orp", "Chester", "Stan", "Beck", "Bex", "Brad", "Abbots", "Abbey",
           ]

_second = [ "gate", "ton", "ford", "wood", "leigh", "ley", "don", "mouth", 
            "bury", "borough", "vale", "brook", "hurst", "pool", "land",
            "bourne", "sey", "burn", "cester", "chapel", "church", "ham", "hampton",
            "minster", "mouth", "ness", "port", "shaw", "wich", "wick", "wold",
            "worth", "well", "market", "chester", "cott", "dale", "head"
            ]

_third = [" Hill", " Downs", " Spa", " Low", " Cross", " End", " Dale", " Regis",
          " Magna", " Wick", " Castle", " Vale", " Major", " Minor"]

_station = [" Central", " St. Thomas", " St. John's", " St. David's",
            " Square"]

_location = ["-on-the-Moor", "-on-Sea", "-on-the-Hill"]

def gen_station_name(name):
    from random import randint, choice

    _out_str = name

    if randint(0,10) > 6:
      _out_str += choice(_station)
    elif randint(0,10) > 7:
       _out_str += ' & ' + gen_name(False, False)
    elif randint(0,10) > 7:
       _out_str += ' ' + gen_name(False, False) + ' Road'
    
    return _out_str

def gen_name(can_have_third=True, can_have_pre=True):
    from random import choice, randint
 
    _out_str = ''
   
    if randint(0,10) > 7 and can_have_pre:
        _out_str = choice(_pre)
        _out_str += choice(_first) + choice(_second)

    elif randint(0,10) > 5 and can_have_third:
        _out_str += choice(_first) + choice(_second)
        _out_str += choice(_third)

    else:
        _out_str += choice(_first) + choice(_second)
        if randint(0,10) > 8:
            _out_str += choice(_location)

    return _out_str

if __name__ in "__main__":
    print(gen_name(True))
