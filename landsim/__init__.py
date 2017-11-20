import numpy as np
from random import choice, uniform, randint
from . import name_gen
from termcolor import colored

color_string_dict = {0 : colored('0', 'cyan'),
                     1 : colored('1', 'white'),
                     2 : colored('2', 'yellow'),
                     3 : colored('3', 'green'),
                     5 : colored('5', 'red'),
                     -1 : colored('9', 'white')}

def _print_map(layer, color=None):
    out_str = ''
    for y in range(layer.shape[0]):
        for x in range(layer.shape[1]):
            if color is None:
                out_str += color_string_dict[int(layer[x][y])] + " "
            else:
                if int(layer[x][y]) == -1:
                    out_str += 2*color_string_dict[-1] + " "
                else:
                    if len(str(int(layer[x][y]))) == 1:
                        out_str += colored('0'+str(int(layer[x][y])), 'red')
                    else:
                        out_str += colored(str(int(layer[x][y])), 'red')
                    out_str += " "
        out_str += '\n'
    print(out_str)

class map:
    def __init__(self, x, y, n_cities=0, n_water=0):
        self._land_layer = _land_layer(x,y)
        self._cities = []
        self._city_layer = _city_layer(x,y)
        if n_cities:
            for i in range(n_cities):
                self.add_city()
        if n_water:
            for i in range(n_water):
                self._land_layer.add_water_source()

    def add_city(self):
        self._cities.append(city(self))
        _x, _y = self._cities[-1].get_location()
        self._city_layer._grid[_y][_x] = len(self._cities)

    def add_water_source(self):
        return self._land_layer._add_water_source()

    def build_station(self, id_):
        try:
            assert id_ > 0
            self._cities[id_-1].add_station()
        except:
            print("Invalid City ID '{}'".format(id_))

    def get_city_info(self, id_):
        try:
            assert id_ > 0
            print(self._cities[id_-1].print_info())
        except:
            print("Invalid City ID '{}'".format(id_))

    def print_layer(self, name):
        if name == 'land':
            self._land_layer._print_layer()
        elif name == 'cities':
            return self._city_layer._print_layer()
        else:
            print("Invalid Layer Name")

    def print_map(self):
        _tmp0 = np.copy(self._city_layer._grid)
        _tmp1 = np.copy(self._land_layer._grid)
        np.place(_tmp0, _tmp0 != -1, [5])
        _tmp = np.where(_tmp0 == -1, 
                        _tmp1, 
                        _tmp0)
        _print_map(_tmp)

class _city_layer:
    def __init__(self, x, y):
        self._grid = np.full((x,y), -1)

    def _add_city(self):
        _x, _y = self._cities[-1].get_location()
        self._grid[_y][_x] = 5

    def _print_layer(self):
        _tmp0 = np.copy(self._grid)
        return _print_map(_tmp0, 'red')

class _land_layer:
    def __init__(self, x, y):
        self._grid = np.random.rand(x,y)+np.random.randint(1,4, size=(x,y))
        self._generate_map()

    def _get_neighbours(self, x, y):
        _neighbours = []
        if( x != 0 ):
            _neighbours.append((x-1,y))
            if( y != 0 ):
                _neighbours.append((x-1, y-1))
            if( y != self._grid.shape[0]-1 ):
                _neighbours.append((x-1, self._grid.shape[0]-1))
        if( x != self._grid.shape[1]-1 ):
            _neighbours.append((x+1, y))
            if( y != 0 ):
                _neighbours.append((x+1, y-1))
            if( y != self._grid.shape[0]-1 ):
                 _neighbours.append((x+1, self._grid.shape[0]-1))
        return _neighbours


    def _get_weighted_value(self, x, y):
       _neighbours = self._get_neighbours(x, y)
       _vals = []
       for neighbour in _neighbours:
           _vals.append(uniform(self._grid[neighbour[1]][neighbour[0]],
                              self._grid[neighbour[1]][neighbour[0]-1]))
       return choice(_vals)

    def _generate_map(self):
        for y in range(self._grid.shape[0]):
            for x in range(self._grid.shape[1]):
                self._grid[y][x] = self._get_weighted_value(x,y)

    def _choose_flow_dir(self, x,y):
        _options = []
        for neighbour in self._get_neighbours(x,y):
            if self._grid[neighbour[1]][neighbour[0]] == 0:
                _x, _y = neighbour
                _pos_bool = 2*_x-1 < self._grid.shape[1] and 2*_y-1 < self._grid.shape[0]
                _neg_bool = 2*_x-1 > 0 and 2*_y-1 > 0
                if _pos_bool and _neg_bool:
                    _options.append((2*_x-1,2*_y-1))
                if _x == x:
                    if 2*_y+1 < self._grid.shape[0]:
                        if x+1 < self._grid.shape[1]:
                            _options.append((x+1, 2*_y-1))
                        if x-1 > 0:
                            _options.append((x-1, 2*_y-1))
                if _y == y:
                    if 2*_x+1 < self._grid.shape[1]:
                        if y+1 < self._grid.shape[0]:
                            _options.append((2*_x-1, y+1))
                        if y-1 > 0:
                            _options.append((2*_x-1, y-1))
                if len(_options) > 0:
                    return choice(_options)
        _x_low = -1
        _x_high = 1
        _y_low = -1
        _y_high = 1

        if x+_x_low < 0:
            _x_low = 0
        if x+_x_high > self._grid.shape[1]-1:
            _x_high = 0
        if y+_y_low < 0:
            _y_low = 0
        if y+_y_high > self._grid.shape[0]-1:
            _y_high = 0

        return (x+randint(_x_low, _x_high), y+randint(_y_low, _y_high))

    def _place_water_source(self, x, y):
        self._grid[y][x] = 0
        _success = True
        _x, _y = x, y
        _trials = 0
        while _success:
            try:
                coords = self._choose_flow_dir(_x,_y)
                self._grid[coords[1]][coords[0]] = 0
                _x, _y = coords
                _trials += 1
            except:
                _trials += 1
                _x, _y = x, y
                continue
            if _trials > self._grid.shape[0]+10:
                _success = False

    def _add_water_source(self):
        self._place_water_source(randint(0, self._grid.shape[1]-1), randint(0, self._grid.shape[0]-1))


    def _print_layer(self):
        return _print_map(self._grid)

class city:
    def __init__(self, map_):
        from random import randint
        self._name = name_gen.gen_name()
        self._population = randint(1000,1E5)
        self._stations = []
        self._location = None
        self._place_at_random(map_)

    def print_info(self):
        _info='''
        {}
        -----------------------
        Location: ({}, {})
        Population: {}
        Stations: {}
        -----------------------
        '''.format(self._name,
                   self._location[1]+1,
                   self._location[0]+1,
                   self._population,
                   ','.join(self._stations))
        return _info 

    def get_name(self):
        return self._name

    def add_station(self):
        self._stations.append(name_gen.gen_station_name(self._name))

    def get_stations(self):
        return self._stations

    def get_location(self):
        return self._location

    def _place_at_random(self, map_):
        _val = 0
        while _val != 3:
            _x = randint(0, map_._land_layer._grid.shape[1]-1)
            _y = randint(0, map_._land_layer._grid.shape[0]-1)
            for neighbour in map_._land_layer._get_neighbours(_x, _y):
                if map_._city_layer._grid[neighbour[1]][neighbour[0]] != -1:
                    continue
            _val = int(map_._land_layer._grid[_y][_x])
        self._location = (_x, _y)

