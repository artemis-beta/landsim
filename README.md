# landsim
Generate Terrain/Land Using Random Number Generation in Python! To use this module:
```
import landsim as ls

x, y = 30, 30                          # Create a map of size 30x30
                                       
my_map = ls.map(x, y, 
                n_cities=20, 
                n_water=5)             # Create map with 20 cities and
                                       # 5 water sources

my_map.add_water_source()              # Randomly add another water source

my_map.add_city()                      # Randomly add a new city

my_map.print_map()                     # Print map to terminal

my_map.print_layer('cities')           # Print only a layer ('land'/'cities')
                                       # the cities layer displays city ids

my_map.get_city_info(i)                # Get info for city id=i

my_map.build_station(i)                # Build at town id=i

```

![Alt text](./example.png?raw=true "An Example Map")
