import pygame


class PotatoMine(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(PotatoMine, self).__init__()
        # 加载图片
        self.image = pygame.image.load("..\pvz\png\PotatoMine\PotatoMineInit\PotatoMineInit_0.png").convert_alpha()
        self.explode_image = pygame.image.load("..\pvz\png\PotatoMine\PotatoMineExplode\PotatoMineExplode_0.png").convert_alpha()
        self.images = [pygame.image.load("..\pvz\png\PotatoMine\PotatoMine\PotatoMine_{:0d}.png".format(i)).convert_alpha() for i in
                       range(0, 8)]
        
        # rect设置(大小位置)
        self.rect = self.image.get_rect()
        self.rect.left = rect[0]
        self.rect.top = rect[1]
        
        # 伤害
        self.attack = 100

        # pre:已经准备的时间 pre_time:需要准备的时间 pred:是否准备完成
        self.pre = 0
        self.pre_time = 80  
        self.pred = False  
        
        # boom:是否爆炸 booming:爆炸是否开始
        self.boom = False      
        self.booming = False   
        
        self.energy = 60
        self.zombies = set()

    def update(self, *args):
        if self.booming:
            self.kill()
            return

        # 准备阶段
        if self.pre <= self.pre_time:
            self.pre += 1
            # 僵尸啃食土豆地雷
            for zombie in self.zombies:
                if not zombie.Alive:
                    self.energy += 0
                else:
                    self.energy -= 1
            if self.energy <= 0:
                for zombie in self.zombies:
                    zombie.GOGO = False
                self.kill()
        
        # 准备完成
        else:
            self.pred = True  
            
            # boom==True说明土豆地雷已经触碰到僵尸,将booming设为true,便于下一帧渲染爆炸图片
            if self.boom:
                self.image = self.explode_image
                self.booming = True  
                
            else:
                
                self.image = self.images[args[0] % len(self.images)]