import numpy as np
from random import choice, uniform, randint
from termcolor import colored

color_string_dict = {0 : colored('0', 'cyan'),
                     1 : colored('1', 'white'),
                     2 : colored('2', 'yellow'),
                     3 : colored('3', 'green')}

class landmap:
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
           _vals.append(uniform(self._grid[neighbour[1]][neighbour[0]],self._grid[neighbour[1]][neighbour[0]-1]))
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

    def add_water_source(self):
        self._place_water_source(randint(0, self._grid.shape[1]-1), randint(0, self._grid.shape[0]-1))


    def print_map(self):
        out_str = ''
        for y in range(self._grid.shape[0]):
            for x in range(self._grid.shape[1]):
                out_str += color_string_dict[int(self._grid[x][y])] + " "
            out_str += '\n'
        print(out_str)


if __name__ in "__main__":
    _map = landmap(20,20)
    _map.add_water_source()
    _map.add_water_source()
    _map.print_map()
