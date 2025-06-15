from zombie import Zombie, Zombie_lz, Zombie_iron
from plant import SunFlower, Peashooter, Wallnut, JXC, PotatoMine


zombie = (Zombie.Zombie, Zombie_lz.Zombie_lz, Zombie_iron.Zombie_iron)
plant = (SunFlower.SunFlower, Peashooter.Peashooter, Wallnut.Wallnut, JXC.JXC, PotatoMine.PotatoMine)

game_level_0={
    'level':0,
    'plant_kinds':(plant[0], plant[1]),
    'zombie_num':10,
    'zombie_kinds':(zombie[0], zombie[1])
}

game_level_1={
    'level':1,
    'plant_kinds':(plant[0], plant[1], plant[2]),
    'zombie_num':20,
    'zombie_kinds':(zombie[0], zombie[1])
}

game_level_2={
    'level':2,
    'plant_kinds':(plant[0], plant[1], plant[2], plant[4]),
    'zombie_num':30,
    'zombie_kinds':(zombie[0], zombie[1])
}

game_level_3={
    'level':3,
    'plant_kinds':(plant[0], plant[1], plant[2],plant[3], plant[4]),
    'zombie_num':40,
    'zombie_kinds':(zombie[0], zombie[1], zombie[2])
}


game_level_general={
    0:game_level_0,
    1:game_level_1,
    2:game_level_2,
    3:game_level_3
}