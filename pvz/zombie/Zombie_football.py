import pygame
from zombie.Zombie import Zombie


class Zombie_football(Zombie):
    def __init__(self):
        super(Zombie_football, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("../pvz/png/Zombie/lz/Zombie_000.png").convert_alpha(),(128,102))
        self.images_football = [pygame.transform.scale(pygame.image.load("../pvz/png/Zombie/football/FootballZombie/FootballZombie_{:0d}.png".format(i)).convert_alpha(),(128,102))
                          for i in range(0, 22)]
        self.images_football_losehelmet = [pygame.transform.scale(pygame.image.load("../pvz/png/Zombie/football/FootballZombieLostHelmet/FootballZombieLostHelmet_{:0d}.png".format(i)).convert_alpha(),(128,102))
                          for i in range(0,22)]
        self.attack_football = [pygame.transform.scale(pygame.image.load("../pvz/png/Zombie/football/FootballZombieAttack/FootballZombieAttack_{:0d}.png".format(i)).convert_alpha(),(128,102))
                          for i in range(0, 20)]
        self.attack_football_losehelmet = [pygame.transform.scale(pygame.image.load("../pvz/png/Zombie/football/FootballZombieLostHeadAttack/FootballZombieLostHeadAttack_{:0d}.png".format(i)).convert_alpha(),(128,102))
                          for i in range(0, 10)]
        self.energy = 200
        self.speed = 1.0

    def update(self, *args, **kwargs) -> None:
        if 100 < self.energy <= 200:
            if self.GOGO:
                self.image = self.attack_football[args[0] % len(self.attack_football)]
            else:
                self.image = self.images_football[args[0] % len(self.images_football)]
            if self.rect.left > -120 and not self.GOGO:
                self.rect.left -= self.speed
        elif 10 < self.energy <= 100:
            if self.GOGO:
                self.image = self.attack_football_losehelmet[args[0] % len(self.attack_football_losehelmet)]
            else:
                self.image = self.images_football_losehelmet[args[0] % len(self.images_football_losehelmet)]
            if self.rect.left > -120 and not self.GOGO:
                self.rect.left -= self.speed
        elif 0 < self.energy <= 10:
            if self.GOGO:
                self.image = self.attack_images[args[0] % len(self.attack_images)]
            else:
                self.image = self.images[args[0] % len(self.images)]
            if self.rect.left > -120 and not self.GOGO:
                self.rect.left -= self.speed
        else:
            if self.dietimes < 38:
                self.image = self.dieimages[self.dietimes]
                self.dietimes += 1
            else:
                if self.dietimes == 38:
                    self.Alive = False
                    self.kill()
