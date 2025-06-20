import time, pygame, sys
from plant.Peashooter import Peashooter
from plant.SunFlower import SunFlower
from plant.Wallnut import Wallnut
from plant.Sun import Sun
from plant.Sun2 import Sun2
from plant.JXC import JXC
from plant.Bullet import Bullet
from plant.Bullet_jxc import Bullet_jxc
from plant.PotatoMine import PotatoMine
from plant.CherryBomb import CherryBomb
from level.level_settings import game_level_general
import random

# 游戏尺寸
pygame.init()
backgd_size = (820, 560)

# 资源路径
screen = pygame.display.set_mode(backgd_size)
pygame.display.set_caption("植物大战僵尸")
bg_img_obj = pygame.image.load("../pvz/png/a3.png").convert_alpha()
sunFlowerImg = pygame.image.load("../pvz/png/SunFlower/SunFlower_00.png").convert_alpha()
wallNutImg = pygame.image.load("../pvz/png/Wallnut/Wallnut_00.png").convert_alpha()
peaShooterImg = pygame.image.load("../pvz/png/Peashooter/Peashooter00.png").convert_alpha()
jxcImg = pygame.image.load("../pvz/png/jxc/JXC00.png").convert_alpha()
potatomineImg = pygame.image.load("../pvz/png/potatomine/PotatoMine/PotatoMine_0.png").convert_alpha()
cherrybombImg = pygame.image.load("../pvz/png/CherryBomb/CherryBomb_0.png")
sunbackImg = pygame.transform.scale(pygame.image.load("../pvz/png/SeedBank02.png").convert_alpha(),(596,70))
sunflower_seed = pygame.image.load("../pvz/png/SunFlower_kp.png")
wallnut_seed = pygame.image.load("../pvz/png/Wallnut_kp.png")
peashooter_seed = pygame.image.load("../pvz/png/Peashooter_kp.png")
jxc_seed = pygame.image.load("../pvz/png/jxc_kp.png")
potatomine_seed = pygame.transform.scale(pygame.image.load("../pvz/png/PotatoMine_kp.png"),(42,58))
CherryBomb_seed = pygame.transform.scale(pygame.image.load("../pvz/png/Cherrybomb_kp.png"),(42,58))
shovel_Box = pygame.image.load("../pvz/png/screen/shovelBox.png")
shovel = pygame.image.load("../pvz/png/screen/shovel.png")

# 结算图片
victory = pygame.image.load("../pvz/png/screen/GameVictory.png").convert_alpha()
lose = pygame.image.load("../pvz/png/screen/GameLose.jpg").convert_alpha()




def game_menu():
    """
    显示游戏主菜单，处理按钮点击，并包含一个可弹出的选项菜单。
    """
    # 加载菜单所需的所有资源
    menu_bg = pygame.image.load("../pvz/png/screen/MainMenu.png").convert()
    menu_bg = pygame.transform.scale(menu_bg, backgd_size)
    button_img = pygame.image.load("../pvz/png/screen/Adventure_button.png").convert_alpha()
    options_panel_img = pygame.image.load("../pvz/png/screen/options_panel.png").convert_alpha()
    
   # 播放背景音乐
    try:
        pygame.mixer.music.load("../pvz/music/intro.opus")
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("未找到背景音乐文件 ../pvz/png/menu_music.mp3，将无声运行。")

    # --- 字体定义 ---
    # 大字体用于花瓶按钮，小字体用于面板内文字
    vase_font = pygame.font.SysFont("黑体", 22, bold=True)
    panel_font = pygame.font.SysFont("黑体", 20)

    # --- 按钮和UI元素的位置定义 ---
    # “开始冒险”按钮 - 向右移动了10个像素
    button_rect = button_img.get_rect(topleft=(420, 75))
    
    # 右下角三个花瓶按钮（矩形区域）
    options_btn_rect = pygame.Rect(590, 455, 60, 30)
    about_btn_rect = pygame.Rect(660, 480, 60, 30) # 新增“关于”按钮
    exit_btn_rect = pygame.Rect(735, 475, 60, 30)
    
    # --- 创建按钮的文本 Surface (这是之前缺失的关键步骤) ---
    options_text = vase_font.render("Options", True, (240, 240, 240))
    about_text = vase_font.render("About", True, (240, 240, 240))
    exit_text = vase_font.render("Exit", True, (240, 240, 240))

    # --- 选项菜单内的元素 ---
    options_panel_rect = options_panel_img.get_rect(center=screen.get_rect().center)
    volume_slider_rect = pygame.Rect(options_panel_rect.left + 140, options_panel_rect.top + 250, 200, 20)
    close_options_rect = pygame.Rect(options_panel_rect.right - 55, options_panel_rect.top + 20, 35, 35)
    # --- 新增：选项菜单底部的退出按钮 ---
    options_exit_btn_rect = pygame.Rect(0, 0, 140, 40)
    options_exit_btn_rect.centerx = options_panel_rect.centerx
    options_exit_btn_rect.bottom = options_panel_rect.bottom - 60
    options_exit_text = panel_font.render("Return Menu", True, (255, 255, 255))


    # --- 关于菜单内的元素 ---
    about_panel_rect = options_panel_img.get_rect(center=screen.get_rect().center)
    close_about_rect = pygame.Rect(about_panel_rect.right - 55, about_panel_rect.top + 100, 35, 35)
    # 作者信息
    author_info_texts = [
        "Game Maker: WangJing",
        "Inspiration: PopCap Games",
        ""
    ]
    author_surfaces = [panel_font.render(line, True, (255, 255, 255)) for line in author_info_texts]


    # 菜单状态变量
    menu_running = True
    options_visible = False # 控制选项面板是否显示
    about_visible = False   # 控制关于面板是否显示
    dragging_volume = False # 是否正在拖动音量滑块

    while menu_running:
        # --- 事件处理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- 鼠标按下事件 ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 根据当前显示的面板，决定响应哪些点击
                if options_visible:
                    if volume_slider_rect.collidepoint(event.pos):
                        dragging_volume = True
                    elif (not options_panel_rect.collidepoint(event.pos) or 
                          close_options_rect.collidepoint(event.pos) or 
                          options_exit_btn_rect.collidepoint(event.pos)):
                        options_visible = False
                elif about_visible:
                    # 点击关于面板任意位置或关闭按钮都会关闭它
                    about_visible = False
                else:
                    # 主菜单按钮点击判断
                    if button_rect.collidepoint(event.pos):
                        print("点击了开始冒险！")
                        menu_running = False
                    elif options_btn_rect.collidepoint(event.pos):
                        print("打开选项菜单...")
                        options_visible = True
                    elif about_btn_rect.collidepoint(event.pos):
                        print("打开关于菜单...")
                        about_visible = True
                    elif exit_btn_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            
            # --- 鼠标松开事件 ---
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_volume = False

            # --- 鼠标移动事件 ---
            if event.type == pygame.MOUSEMOTION and dragging_volume:
                mouse_x = max(volume_slider_rect.left, min(event.pos[0], volume_slider_rect.right))
                volume = (mouse_x - volume_slider_rect.left) / volume_slider_rect.width
                pygame.mixer.music.set_volume(volume)

        # --- 绘制 ---
        # 1. 绘制主菜单背景和按钮
        screen.blit(menu_bg, (0, 0))
        screen.blit(button_img, button_rect)
        
        # 2. 绘制花瓶按钮的文字
        screen.blit(options_text, options_text.get_rect(center=options_btn_rect.center))
        screen.blit(about_text, about_text.get_rect(center=about_btn_rect.center))
        screen.blit(exit_text, exit_text.get_rect(center=exit_btn_rect.center))
        
        # 3. 根据状态，决定是否绘制弹出面板
        if options_visible:
            screen.blit(options_panel_img, options_panel_rect)
            # 绘制音量条
            pygame.draw.rect(screen, (100, 100, 100), volume_slider_rect)
            current_volume = pygame.mixer.music.get_volume()
            handle_x = volume_slider_rect.left + current_volume * volume_slider_rect.width
            handle_rect = pygame.Rect(0, 0, 20, 30)
            handle_rect.center = (handle_x, volume_slider_rect.centery)
            pygame.draw.rect(screen, (200, 200, 200), handle_rect)
            volume_text = panel_font.render(f"Volume: {int(current_volume * 100)}%", True, (255, 255, 255))
            screen.blit(volume_text, (volume_slider_rect.left, volume_slider_rect.top))
            
            # 绘制菜单的退出按钮
            pygame.draw.rect(screen, (80, 80, 80), options_exit_btn_rect, border_radius=10)
            screen.blit(options_exit_text, options_exit_text.get_rect(center=options_exit_btn_rect.center))

        elif about_visible:
            screen.blit(options_panel_img, about_panel_rect)
            # 逐行绘制作者信息
            for i, surface in enumerate(author_surfaces):
                text_rect = surface.get_rect(centerx=about_panel_rect.centerx, y=about_panel_rect.top + 200 + i * 20)
                screen.blit(surface, text_rect)

        # 刷新屏幕
        pygame.display.update()

    # 游戏开始前，停止菜单的背景音乐
    pygame.mixer.music.stop()

def single_game_loop(level_settings:dict=None):
    global choose
    global text
    global sun_num_surface
    game_state = "PLAYING"  # 初始状态为 "PLAYING"
    running = True
    index = 0
    zombie_num = 0
    game_res = -1
    # text为阳光值
    text = "200"
    sun_font = pygame.font.SysFont("黑体", 25)
    sun_num_surface = sun_font.render(str(text), True, (0, 0, 0))
    # 定义植物组，子弹组，僵尸组，阳光组
    spriteGroup = pygame.sprite.Group()
    bulletGroup = pygame.sprite.Group()
    zombieGroup = pygame.sprite.Group()
    sunsprite = pygame.sprite.Group()

    # 定义特殊事件
    clock = pygame.time.Clock()
    GEN_SUN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(GEN_SUN_EVENT, 2000)
    GEN_BULLET_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(GEN_BULLET_EVENT, 2000)
    GEN_ZOMBIE_EVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(GEN_ZOMBIE_EVENT, 8000)
    GEN_SUN2_EVENT = pygame.USEREVENT + 4
    pygame.time.set_timer(GEN_SUN2_EVENT, 20000)

    # 背景音乐
    pygame.mixer.music.load("../pvz/music/battle.opus")
    pygame.mixer.music.play(-1)
    
    # 游戏参数设置 
    level = level_settings['level']
    total_zombie_num = level_settings['zombie_num']
    # 用于显示统计信息的字体
    info_font = pygame.font.SysFont("黑体", 30)
    # 局内参数
    choose = 0
    zombie_num = 0
    while running:
        clock.tick(20)
        # 绘制右下角关卡和僵尸数统计
        level_text_str = f"Level: {level}"
        zombie_text_str = f"Zombies: {zombie_num}/{total_zombie_num}"

        # 将字符串渲染成 Surface
        level_surface = info_font.render(level_text_str, True, (255, 255, 255), (0,0,0)) # 白字黑底，更清晰
        zombie_surface = info_font.render(zombie_text_str, True, (255, 255, 255), (0,0,0)) # 白字黑底，更清晰

        # 定位 Surface
        screen_rect = screen.get_rect()
        # 将关卡文本定位在屏幕右下角 (留出10像素边距)
        level_rect = level_surface.get_rect(bottomright=(screen_rect.right - 10, screen_rect.bottom - 10))
        # 将僵尸数文本定位在关卡文本的正上方 (留出5像素间距)
        zombie_rect = zombie_surface.get_rect(bottomright=(screen_rect.right - 10, level_rect.top - 5))
        
        
        # 绘制背景 植物栏 僵尸 子弹 植物   
        screen.blit(bg_img_obj, (0, 0))
        screen.blit(sunbackImg, (20, 0.5))
        screen.blit(sun_num_surface, (45, 50))
        screen.blit(sunflower_seed, (95, 5))
        screen.blit(peashooter_seed, (136, 5))
        screen.blit(wallnut_seed, (177, 5))
        screen.blit(jxc_seed, (218, 5))
        screen.blit(potatomine_seed, (259,5))
        screen.blit(CherryBomb_seed, (301,5))
        # 绘制铲子框 铲子
        screen.blit(shovel_Box, (680,0))
        screen.blit(shovel, (680,0))
        screen.blit(level_surface, level_rect)
        screen.blit(zombie_surface, zombie_rect)
        spriteGroup.update(index)
        spriteGroup.draw(screen)
        bulletGroup.update(index)
        bulletGroup.draw(screen)
        zombieGroup.update(index)
        zombieGroup.draw(screen)
        sunsprite.update(index)
        sunsprite.draw(screen)
        if game_state == "PLAYING":
            # 子弹击打僵尸逻辑
            for bullet in bulletGroup:
                for zombie in zombieGroup:
                    if pygame.sprite.collide_mask(bullet, zombie):
                        zombie.energy -= bullet.attack
                        bulletGroup.remove(bullet)

                            
            # 僵尸啃食植物逻辑
            for sprite in spriteGroup:
                # 土豆地雷特判
                if isinstance(sprite, PotatoMine) and sprite.pred == True:
                    # 土豆地雷爆炸逻辑：附近一格的僵尸全部死亡
                    for zombie in zombieGroup:  
                        if pygame.sprite.collide_mask(sprite, zombie):
                            sprite.boom = True
                            for zombie_ in zombieGroup:
                                if abs(zombie_.rect.top - sprite.rect[1]) <=80 and abs(zombie_.rect.left - sprite.rect[0]) < 80:
                                    zombie_.energy -= sprite.attack # 僵尸血量

                # 樱桃炸弹逻辑
                if isinstance(sprite, CherryBomb):
                    if sprite.booming == True:
                        for zombie in zombieGroup:
                            if abs(zombie.rect.top - sprite.rect[1]) <= 180 and abs(zombie.rect.left - sprite.rect[0]) < 180:
                                zombie.energy -= sprite.attack
                
                for zombie in zombieGroup:
                    if pygame.sprite.collide_mask(sprite, zombie):
                        zombie.GOGO = True
                        sprite.zombies.add(zombie)     
                    if isinstance(sprite, JXC):
                        if abs(zombie.rect.top - sprite.rect[1]) <= 40 and zombie.rect.left < 760:
                            sprite.attack = True
                            if sprite.att == 11:
                                bullet_jxc = Bullet_jxc(sprite.rect, backgd_size, zombie.rect[0])
                                bulletGroup.add(bullet_jxc)
                                break
            
            # 从种子蓝选择植物
            (x, y) = pygame.mouse.get_pos()
            if choose == 1:
                screen.blit(sunFlowerImg, (x - sunFlowerImg.get_rect().width // 2, y - sunFlowerImg.get_rect().height // 2))
            if choose == 2:
                screen.blit(peaShooterImg,
                            (x - peaShooterImg.get_rect().width // 2, y - peaShooterImg.get_rect().height // 2))
            if choose == 3:
                screen.blit(wallNutImg, (x - wallNutImg.get_rect().width // 2, y - wallNutImg.get_rect().height // 2))
            if choose == 4:
                screen.blit(jxcImg, (x - jxcImg.get_rect().width // 2, y - jxcImg.get_rect().height // 2))
            if choose == 5:
                screen.blit(potatomineImg, (x - potatomineImg.get_rect().width // 2,y - potatomineImg.get_rect().height //2))
            if choose == 6:
                screen.blit(cherrybombImg, (x - cherrybombImg.get_rect().width // 2, y - cherrybombImg.get_rect().height // 2)) 
            if choose == 7:
                screen.blit(shovel, (x - shovel.get_rect().width // 2, y - shovel.get_rect().height // 2))
            
            # 生成随机阳光 僵尸 向日葵阳光 子弹
            index += 1
            for event in pygame.event.get():
                if event.type == GEN_SUN2_EVENT:
                    sun2 = Sun2()
                    sunsprite.add(sun2)
                if event.type == GEN_ZOMBIE_EVENT:
                    zombie_num += 1
                    zombie_set = level_settings['zombie_kinds']
                    zombie = random.choice(zombie_set)()
                    zombieGroup.add(zombie)
                    
                if event.type == GEN_SUN_EVENT:
                    for sprite in spriteGroup:
                        if isinstance(sprite, SunFlower):
                            now = time.time()
                            if now - sprite.lasttime >= 10:
                                sun = Sun(sprite.rect)
                                sunsprite.add(sun)
                                sprite.lasttime = now
                if event.type == GEN_BULLET_EVENT:
                    for sprite in spriteGroup:
                        for zombie in zombieGroup:
                            if isinstance(sprite, Peashooter) \
                                    and 0 < sprite.rect[1] - zombie.rect[1] < 50 \
                                    and zombie.rect[0] < 760:
                                bullet = Bullet(sprite.rect, backgd_size)
                                bulletGroup.add(bullet)
                                break
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_key = pygame.mouse.get_pressed()
                    if pressed_key[0]:
                        pos = pygame.mouse.get_pos()
                        x, y = pos
                        if 82 <= x < 123 and 5 <= y <= 63 and int(text) >= 50:
                            choose = 1
                        elif 123 <= x < 164 and 5 <= y <= 63 and int(text) >= 100:
                            choose = 2
                        elif 164 <= x < 205 and 5 <= y <= 63 and int(text) >= 50:
                            choose = 3
                        elif 205 <= x < 246 and 5 <= y <= 63 and int(text) >= 100:
                            choose = 4
                        elif 246 <= x < 287 and 5 <= y <= 63 and int(text) >= 25:
                            choose = 5
                        elif 287 <= x < 328 and 5 <= y <= 63 and int (text) >= 125:
                            choose = 6
                        elif 675 <= x <= 740 and 0 <= y <=70:
                            choose = 7
                        elif 36 < x < 800 and 70 < y < 550:
                            if choose == 1:
                                trueX = x // 90 * 85 + 35
                                trueY = y // 100 * 95 - 15
                                canHold = True
                                for sprite in spriteGroup:
                                    if abs(sprite.rect.left-trueX) <= 40 and abs(sprite.rect.top - trueY) <= 40:
                                        canHold = False
                                        break
                                if not canHold or trueY < 25:
                                    break
                                sunflower = SunFlower(time.time(), (trueX, trueY))
                                spriteGroup.add(sunflower)
                                choose = 0
                                text = int(text)
                                text -= 50
                                myfont = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = myfont.render(str(text), True, (0, 0, 0))
                            if choose == 2:
                                trueX = x // 90 * 85 + 32
                                trueY = y // 100 * 95 - 18
                                canHold = True
                                for sprite in spriteGroup:
                                    if abs(sprite.rect.left-trueX) <= 40 and abs(sprite.rect.top - trueY) <= 40:
                                        canHold = False
                                        break
                                if not canHold or trueY < 25:
                                    break
                                peashooter = Peashooter((trueX, trueY))
                                spriteGroup.add(peashooter)
                                choose = 0
                                text = int(text)
                                text -= 100
                                myfont = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = myfont.render(str(text), True, (0, 0, 0))
                            if choose == 3:
                                trueX = x // 90 * 85 + 35
                                trueY = y // 100 * 95 - 15
                                canHold = True
                                for sprite in spriteGroup:
                                    if abs(sprite.rect.left-trueX) <= 40 and abs(sprite.rect.top - trueY) <= 40:
                                        canHold = False
                                        break
                                if not canHold or trueY < 25:
                                    break
                                wallNut = Wallnut((trueX, trueY))
                                spriteGroup.add(wallNut)
                                choose = 0
                                text = int(text)
                                text -= 50
                                myfont = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = myfont.render(str(text), True, (0, 0, 0))
                            if choose == 4:
                                trueX = x // 90 * 85 + 22
                                trueY = y // 100 * 95 - 35
                                canHold = True
                                for sprite in spriteGroup:
                                    if abs(sprite.rect.left-trueX) <= 40 and abs(sprite.rect.top - trueY) <= 40:
                                        canHold = False
                                        break
                                if not canHold or trueY < 25:
                                    break
                                jxc = JXC((trueX, trueY))
                                spriteGroup.add(jxc)
                                choose = 0
                                text = int(text)
                                text -= 100
                                myfont = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = myfont.render(str(text), True, (0, 0, 0))
                            if choose == 5:
                                trueX = x //90 * 85 + 30
                                trueY = y //100 * 95
                                canHold = True
                                for sprite in spriteGroup:
                                    if abs(sprite.rect.left-trueX) <= 40 and abs(sprite.rect.top - trueY) <= 40:
                                        canHold = False
                                        break
                                if not canHold or trueY < 25:
                                    break
                                potatomine = PotatoMine((trueX, trueY))
                                spriteGroup.add(potatomine)
                                choose = 0
                                text = int(text)
                                text -= 25
                                myfont = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = myfont.render(str(text), True, (0, 0, 0))
                            if choose == 6:
                                trueX = x //90 * 85 + 30
                                trueY = y //100 * 95
                                canHold = True
                                for sprite in spriteGroup:
                                    if abs(sprite.rect.left-trueX) <= 40 and abs(sprite.rect.top - trueY) <= 40:
                                        canHold = False
                                        break
                                if not canHold or trueY < 25:
                                    break
                                cherrybomb = CherryBomb((trueX,trueY))
                                cherrybomb.boom = True
                                spriteGroup.add(cherrybomb)
                                choose = 0
                                text = int(text)
                                text -= 125
                                myfont = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = myfont.render(str(text), True, (0, 0, 0))
                            if choose == 7:
                                trueX = x 
                                trueY = y - 20
                                for sprite in spriteGroup:
                                    if abs(sprite.rect.left-trueX) <= 40 and abs(sprite.rect.top - trueY) <= 40:
                                        sprite.kill()
                        for sun in sunsprite:
                            if sun.rect.collidepoint(pos):
                                sunsprite.remove(sun)
                                text = str(int(text) + 25)
                                sun_font = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = sun_font.render(str(text), True, (0, 0, 0))
                    elif pressed_key[2]:
                        choose = 0
                for zombie in zombieGroup:
                    if zombie.rect.left <= 0:
                        print("你的脑子被僵尸吃了")
                        game_state = "LOSE"
                        game_res = 0
                        break
                if zombie_num >= total_zombie_num:
                    # 停止继续生成僵尸
                    pygame.time.set_timer(GEN_ZOMBIE_EVENT, 0)
                    # 判断是否胜利
                    if not zombieGroup:
                        print("胜利")
                        game_state = "VICTORY"
                        game_res = 1
                        break
            
        elif game_state == "VICTORY":
            # 绘制胜利动画
            screen.blit(victory, victory.get_rect(center=screen.get_rect().center))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        running = False # 点击鼠标，退出循环
        elif game_state =="LOSE":
            screen.blit(lose, lose.get_rect(center=screen.get_rect().center))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        running = False # 点击鼠标，退出循环
        pygame.display.update()
    return game_res
    
            
    

def game(levels_num=4, level_settings_general:dict=None):
    """
    profile:
        从level_settings中读取每个level的setting,传入单局游戏循环
    input:
        level:游戏关卡数(目前只支持4关)
        
    """
    for i in range(levels_num):
        game_res = single_game_loop(level_settings_general[i])
        if game_res == 0 or game_res == -1:
            break
        
    

if __name__ == '__main__':
    game_menu()
    game(levels_num=5, level_settings_general=game_level_general)
