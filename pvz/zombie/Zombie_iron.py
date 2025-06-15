import pygame
from zombie.Zombie import Zombie


class Zombie_iron(Zombie):
    def __init__(self):
        super(Zombie_iron, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("../pvz/png/Zombie/lz/Zombie_000.png").convert_alpha(),(128,102))
        self.images_iron = [pygame.transform.scale(pygame.image.load("../pvz/png/Zombie/iron/Iron/BucketheadZombie_{:0d}.png".format(i)).convert_alpha(),(128,102))
                          for i in range(0, 15)]
        self.attack_iron = [pygame.transform.scale(pygame.image.load("../pvz/png/Zombie/iron/IronAttack/BucketheadZombieAttack_{:0d}.png".format(i)).convert_alpha(),(128,102))
                          for i in range(0, 11)]
        self.energy = 100

    def update(self, *args, **kwargs) -> None:
        if self.energy > 10:
            if self.GOGO:
                self.image = self.attack_iron[args[0] % len(self.attack_iron)]
            else:
                self.image = self.images_iron[args[0] % len(self.images_iron)]
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
