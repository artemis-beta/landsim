from setuptools import setup

setup(name                =  'landsim'                                     ,
      version             =  '0.1.0'                                       ,
      description         =  'Map generation from Monte Carlo.'            ,
      url                 =  'http://github.com/artemis-beta/landsim'      ,
      author              =  'Kristian Zarebski'                           ,
      author_email        =  'krizar312@yahoo.co.uk'                       ,
      license             =  'MIT'                                         ,
      packages            =  ['landsim']                                   ,
      zip_safe            =  False                                         ,
      tests_require       =  ['nose2']                                    ,
      install_requires    =  [ 'numpy'      ,
                             ]
     )
