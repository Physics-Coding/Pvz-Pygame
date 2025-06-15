import pygame


class PotatoMine(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(PotatoMine, self).__init__()
        # --- Image Loading (No changes here) ---
        self.image = pygame.image.load("..\pvz\png\PotatoMine\PotatoMineInit\PotatoMineInit_0.png").convert_alpha()
        self.explode_image = pygame.image.load("..\pvz\png\PotatoMine\PotatoMineExplode\PotatoMineExplode_0.png").convert_alpha()
        self.images = [pygame.image.load("..\pvz\png\PotatoMine\PotatoMine\PotatoMine_{:0d}.png".format(i)).convert_alpha() for i in
                       range(0, 8)]
        
        # --- Attribute Initialization ---
        self.rect = self.image.get_rect()
        self.rect.left = rect[0]
        self.rect.top = rect[1]

        self.pre = 0
        self.pre_time = 80  # Arming time
        self.pred = False   # Flag to check if armed
        
        # --- State Flags ---
        self.boom = False      # Trigger for explosion
        self.booming = False   # NEW: State flag for the explosion animation itself
        
        self.energy = 60
        self.zombies = set()

    def update(self, *args):
        # If the explosion has started, kill the sprite on the next frame.
        # This allows the explosion image to be drawn for one frame.
        if self.booming:
            self.kill()
            return

        # State 1: Arming phase
        if self.pre <= self.pre_time:
            self.pre += 1
            # Your energy/zombie logic for the arming phase
            for zombie in self.zombies:
                if not zombie.Alive:
                    self.energy += 0
                else:
                    self.energy -= 1
            if self.energy <= 0:
                for zombie in self.zombies:
                    zombie.GOGO = False
                self.kill()
        
        # State 2: Armed and waiting
        else:
            self.pred = True  # The mine is now officially armed
            
            # If an external event (like a zombie collision) sets self.boom to True
            if self.boom:
                self.image = self.explode_image
                self.booming = True  # Set the booming state to true
                # NOTE: The actual damage to zombies should be applied here.
            else:
                # If not booming, continue the normal armed animation
                self.image = self.images[args[0] % len(self.images)]