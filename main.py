import pygame
import random
import os


FPS=60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIDTH=500
HEIGHT=600

#遊戲初始化&建立視窗
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock() #建立一個物件

#載入圖片
background_img=pygame.image.load(os.path.join("img","background.png")).convert() #從os.path往下目前路徑往下找img 再往下找background
player_img=pygame.image.load(os.path.join("img","player.png")).convert()
bullet_img=pygame.image.load(os.path.join("img","bullet.png")).convert()
#rock_img=pygame.image.load(os.path.join("img","rock.png")).convert()
rock_imgs=[]
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

font_name=pygame.font.match_font('arial') #載入arial字體
font_name=os.path.join("font.ttf")

def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size) #建立物件
    text_surface=font.render(text,True,WHITE)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

def draw_health(surf,hp,x,y):
    if hp<0:
        hp=0
    BAR_LENGTH=100
    BAR_HEIGHT=10
    fill=(hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_init():
    draw_text(screen,'射水母',64,WIDTH/2,HEIGHT/4)
    draw_text(screen, '← →移動飛船 空白鍵發射子彈', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵開始遊戲!', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,36)) #利用transform函式讓改變圖片大小
        self.image.set_colorkey(BLACK) #去掉圖片黑色背景
        self.rect = self.image.get_rect() #將產生的圖片定住
        self.radius=20
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx=8
        self.health=100
    
    def update(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x +=2
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -=2
        
        if self.rect.right> WIDTH:
            self.rect.right=WIDTH
        if self.rect.left < 0:
            self.rect.left=0

    def shoot(self):
        bullet=Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs) 
        self.image_ori.set_colorkey(BLACK)#去掉圖片黑色背景
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect() #將產生的圖片定住
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
         #從上面掉下來的石頭
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
    
    def rotate(self):
        self.total_degree+=self.rot_degree
        self.total_degree=self.total_degree%360
        self.image=pygame.transform.rotate(self.image_ori,self.rot_degree)
        center=self.rect.center
        self.rect=self.image.get_rect() #重新定位石頭位置
        self.rect.center=center

    def update(self):
        self.rotate()
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top>HEIGHT or self.rect.left>WIDTH or self.rect.right<0: #石頭是否超出邊界
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 5)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK) #去掉圖片黑色背景
        self.rect = self.image.get_rect() #將產生的圖片定住
        #發射的子彈,x,y是根據飛船的位置
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy=-10

    
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom <0: #子彈底部小於0, 已經超出視窗
            self.kill() #從sprite群組刪掉
    


all_sprites=pygame.sprite.Group() #all_sprite群組
rocks=pygame.sprite.Group()
bullets=pygame.sprite.Group()

player=Player()
all_sprites.add(player)
for i in range(8):
    r=Rock()
    all_sprites.add(r)
    

all_sprites=pygame.sprite.Group() #all_sprite群組
player=Player()
all_sprites.add(player)
for i in range(8):
    r=Rock()
    all_sprites.add(r)
    rocks.add(r)
score=0


running=True #遊戲是否繼續

#遊戲迴圈
show_init=True
while running:
    if show_init:
        close=draw_init()
        if close:
            break
        show_init=False
    clock.tick(FPS) #1秒最多執行幾次
    #取的輸入
    for event in pygame.event.get(): #回傳所有發生的事件
        if event.type== pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key== pygame.K_SPACE: #按下空白鍵
                player.shoot()
    #更新遊戲
    all_sprites.update()
    hits=pygame.sprite.groupcollide(rocks,bullets,True,True) #把兩個群組放入函式,True代表碰到後刪除
    for hit in hits: #把刪掉的石頭 重新補回來
        r=Rock()
        all_sprites.add(r)
        rocks.add(r)
        score += hit.radius #石頭越大分數越高


    # 判斷石頭 飛船相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        r=Rock()
        all_sprites.add(r)
        rocks.add(r)
        player.health -= hit.radius * 2
        if player.health <= 0:
            running=False

    #畫面顯示
    screen.fill(BLACK) #(R,G,B)
    screen.blit(background_img,(0,0)) #第一個參數是圖片,第二個是位置
    all_sprites.draw(screen) #把畫面畫出來
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,player.health,5,15)
    pygame.display.update()



pygame.quit()