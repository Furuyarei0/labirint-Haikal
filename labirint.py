# Create your game in this file!
from pygame import*

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed_x, speed_y):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.x_speed = speed_x
        self.y_speed = speed_y
    
    def update(self):
        if player.rect.x <= width-80 and player.x_speed > 0 or player.rect.x >= 0 and player.x_speed < 0:
            self.rect.x += self.x_speed
        if player.rect.y <= height-80 and player.y_speed > 0 or player.rect.y >= 0 and player.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: 
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0: 
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: 
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire(self):
        bullet = Bullet('bolt-caster.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 10:
            self.side  = 'right'
        if self.rect.x >= width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x,player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > width + 10:
            self.kill()

width = 600
height = 600
windows = display.set_mode ((width, height))
display.set_caption("Maze")
background_color = (158, 118, 191)
w1 = GameSprite('platform2.png',width / 2 - width / 3, height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 200, 340, 50, 400)
barriers = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()
barriers.add(w1)
barriers.add(w2)

player = Player('knight.png', 5, height - 80, 80, 80, 0, 0)
monster1 = Enemy('monster.gif', width - 80, 170, 80, 80, 5)
monster2 = Enemy('monster.gif', width - 80, 70, 80, 80, 5)
monsters.add(monster1)
monsters.add(monster2)
final_sprite = GameSprite('castle.png', width - 85, height - 100, 80, 80)

finish = False

run = True

while run:
    time.delay(50)
    
    player.reset()

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:    
            if e.key == K_LEFT:
                player.x_speed = -5
            elif e.key == K_RIGHT:
                player.x_speed = 5
            elif e.key == K_UP:
                player.y_speed = -5
            elif e.key ==  K_DOWN:
                player.y_speed = 5
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0
            elif e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0
    
    if not finish:
        windows.fill(background_color)

        player.update()
        bullets.update()
        
        player.reset()
        bullets.draw(windows)
        barriers.draw(windows)
        final_sprite.reset()

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(windows)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.spritecollide(player, monsters, False):
            finish = True
            img = image.load('game over.jpg')
            d = img.get_width() // img.get_height()
            windows.fill((255, 255, 255))
            windows.blit(transform.scale(img, (height * d, height)), (90, 0))

        if sprite.collide_rect(player, final_sprite):
            finish = True
            img = image.load('win.jpg')
            windows.fill((255, 255, 255))
            windows.blit(transform.scale(img, (width, height)), (0,0))

    display.update()