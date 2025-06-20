import pygame


class CherryBomb(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(CherryBomb, self).__init__()
        # 加载图片
        self.image = pygame.image.load("..\pvz\png\CherryBomb\CherryBomb_0.png").convert_alpha()
        self.explode_image = pygame.image.load("..\pvz\png\CherryBomb\Boom.png").convert_alpha()
        self.images = [pygame.image.load("..\pvz\png\CherryBomb\CherryBomb_{:0d}.png".format(i)).convert_alpha() for i in
                       range(0, 6)]
        
        # rect设置(大小位置)
        self.rect = self.image.get_rect()
        self.rect.left = rect[0]
        self.rect.top = rect[1]

        # pre:已经准备的时间 pre_time:需要准备的时间 pred:是否准备完成
        self.time = 0
        self.last_time = len(self.images)  
        
        # boom:是否爆炸 booming:爆炸是否开始
        self.boom = False      
        self.booming = False   
        
        self.attack = 300
        self.zombies = set()

    def update(self, *args):
        if self.booming:
            self.kill()
            return
            
        # boom==True说明樱桃炸弹已经种植,将booming设为true,便于下一帧渲染爆炸图片
        if self.boom:
            # 延时时间8帧
            self.image = self.images[self.time]
            self.time += 1
            if self.time == self.last_time:
                self.booming = True  
                self.image = self.explode_image