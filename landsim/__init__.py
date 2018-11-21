#============================================================================#
#                                LandSim                                     #
#                           Kristian Zarebski                                #
#                                                                            #
# Creates a map of pixel-like areas of different land types as well as       #
# spawns water sources and cities with names and population info. The module #
# is currently experimental with new features being added on occasion.       #
#
#============================================================================#

import numpy as np
from random import choice, uniform, randint
from . import name_gen
from termcolor import colored

color_string_dict = {0 : colored('■', 'cyan'),
                     1 : colored('■', 'white'),
                     2 : colored('■', 'yellow'),
                     3 : colored('■', 'green'),
                     5 : colored('■', 'red'),
                     -1 : colored('■', 'white')}

def _print_map(layer_array, color=None, color_dict=color_string_dict):
    '''Print map layer'''
    out_str = ''
    for y in range(layer_array.shape[0]):
        for x in range(layer_array.shape[1]):
            if color is None:
                out_str += color_dict[int(layer_array[y][x])] + " "
            else:
                if int(layer_array[y][x]) == -1:
                    out_str += 2*color_dict[-1] + " "
                else:
                    if len(str(int(layer_array[y][x]))) == 1:
                        out_str += colored('0'+str(int(layer_array[y][x])), 'red')
                    else:
                        out_str += colored(str(int(layer_array[y][x])), 'red')
                    out_str += " "
        out_str += '\n'
    print(out_str)

class map:
    def __init__(self, x, y, n_cities=0, n_water=0):
        '''
        Map class to create a map consisting of squares of different colours
        representing different land types. Note the ability to display the map
        depends entirely on the size of the terminal/notebook being used
        (obviously a 50x50 map is going to have issues on a terminal of width 20
        characters!)

        Arguments
        ---------

        x    (int)        map width

        y    (int)        map height


        Optional Arguments
        ------------------

        n_cities     (int)      number of cities to place on map

        n_water      (int)      number of water sources to spawn
        '''

        self._land_layer = _land_layer(x,y)
        self._resource_layer = _resource_layer(x,y, self._land_layer)
        self._cities = []
        self._city_layer = _city_layer(x,y)
        if n_cities:
            for i in range(n_cities):
                self.add_city()
        if n_water:
            for i in range(n_water):
                self._land_layer._add_water_source()

    def add_city(self):
        '''Add a new randomly placed city to the map'''
        self._cities.append(city(self))
        _x, _y = self._cities[-1].get_location()
        self._city_layer._grid[_y][_x] = len(self._cities)

    def add_water_source(self):
        '''Add a new randomly placed water source to the map'''
        return self._land_layer._add_water_source()

    def build_station(self, id_):
        '''
        Add a station to the named city

        Arguments
        ---------

        id    (int)      the city id number
        '''
        try:
            assert id_ > 0
            self._cities[id_-1].add_station()
        except:
            print("Invalid City ID '{}'".format(id_))

    def get_city_info(self, id_):
        '''
        Print the information for a given city

        Arguments
        ---------

        id    (int)      the city id number
        '''
        try:
            assert id_ > 0
            print(self._cities[id_-1].print_info())
        except:
            print("Invalid City ID '{}'".format(id_))

    def print_layer(self, name):
        '''
        Print a selected layer.

        Arguments
        ---------

        name      (string)       name of map layer
                                 (cities/land/resources)
        '''
        _print_dict = {'cities' : self._city_layer,
                       'land'   : self._land_layer,
                       'resources' : self._resource_layer}
        
        if name in _print_dict:
            return _print_dict[name]._print_layer()
        
        else:
            print("Invalid Layer Name")

    def print_map(self):
        '''Print the map'''
        _tmp0 = np.copy(self._city_layer._grid)
        _tmp1 = np.copy(self._land_layer._grid)
        np.place(_tmp0, _tmp0 != -1, [5])
        _tmp = np.where(_tmp0 == -1, 
                        _tmp1, 
                        _tmp0)
        _print_map(_tmp)

class _layer(object):
    '''
    Layer class for creating new map layer

    Arguments
    ---------

    x    (int)       layer width

    y    (int)       layer height
    '''
    def __init__(self, x, y):
        self._grid = np.full((x,y), -1)

    def _print_layer(self):
        '''Print the layer'''
        return _print_map(self._grid)


class _city_layer(_layer):
    '''Special instance of layer class for cities'''
    def __init__(self, x, y):
        _layer.__init__(self, x, y)

    def _add_city(self):
        _x, _y = self._cities[-1].get_location()
        self._grid[_y][_x] = 5

    def _print_layer(self):
        _tmp0 = np.copy(self._grid)
        return _print_map(_tmp0, 'red')

class _resource_layer(_layer):
    def __init__(self, x, y, template):
        _layer.__init__(self, x, y)
        self._colors = {9 : colored('■', 'white'),
                        1 : colored('#', 'grey' ),
                        2 : colored(',,', 'green')}

        template._generate_map()
        _tmp = np.copy(self._grid)
        np.place(_tmp, self._grid > 2, [9])
        np.place(_tmp, self._grid < 0, [0])
        self._grid = np.where(_tmp == 0, 
                              np.full((x,y),9),
                              _tmp)
    def _print_layer(self):
        return _print_map(self._grid, color_dict=self._colors)

class _land_layer(_layer):
    def __init__(self, x, y):
        _layer.__init__(self, x, y)
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


class city:
    def __init__(self, map_):
        '''
        City class which holds all information for a city contained within
        a map. Cities are spawned within maps.

        Arguments
        ---------

        map_       (map)       parent map
        '''
        from random import randint
        self._name = name_gen.gen_name()
        self._population = randint(1000,1E5)
        self._stations = []
        self._location = None
        self._place_at_random(map_)

    def print_info(self):
        '''Print the city information'''
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
        '''Returns the name of the city'''
        return self._name

    def add_station(self):
        '''Adds a new station to the city'''
        self._stations.append(name_gen.gen_station_name(self._name))

    def get_stations(self):
        '''Returns a list of all stations within the city'''
        return self._stations

    def get_location(self):
        '''Returns co-ordinates for the given city'''
        return self._location

    def _place_at_random(self, map_):
        '''Randomly place a city on the stated map'''
        _val = 0
        while _val != 3:
            _x = randint(0, map_._land_layer._grid.shape[1]-1)
            _y = randint(0, map_._land_layer._grid.shape[0]-1)
            for neighbour in map_._land_layer._get_neighbours(_x, _y):
                if map_._city_layer._grid[neighbour[1]][neighbour[0]] != -1:
                    continue
            _val = int(map_._land_layer._grid[_y][_x])
        self._location = (_x, _y)

