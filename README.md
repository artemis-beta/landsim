# landsim
Generate Terrain/Land Using Random Number Generation in Python! To use this module:
```
import landsim as ls

x, y = 30, 30                          # Create a map of size 30x30

my_map = ls.landmap(x, y)

my_map.add_water_source()              # Randomly add a water source

my_cities = []

for n_city in range(20):               # Create 20 cities randomly on the map
    my_cities.append(ls.city(my_map))

my_map.print_map()                     # Print map to terminal

city_example = my_cities[0]

city_example.get_name()                # Cities are given names!

city_example.add_station()             # Stations can be built with their own 
                                       # names too!
```

![Alt text](./example.png?raw=true "An Example Map")
