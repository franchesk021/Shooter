from pygame import *
from random import randint

window = display.set_mode((700,500))
display.set_caption('Шутер крутой очень')


background = transform.scale(image.load('galaxy.jpg'),(700,500))

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
mixer.music.set_volume(0.5)
fire = mixer.Sound('fire.ogg')

font.init()

def draw_counter(x,y,text):
    img = font.SysFont('neon',30).render(text,True,(250,250,250))
    window.blit(img,(x,y))

def draw_result(text,x,y,size,color):
    img = font.SysFont("verdana", size).render(text,True,color)
    rect = img.get_rect()
    window.blit(img,(x-rect.w/2,y - rect.h/2))


clock = time.Clock()
dt = 0



class GameSprite(sprite.Sprite):
    def __init__(self,filename,x,y,w,h):
        super().__init__()
        self.image = transform.scale(image.load(filename),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image,(self.rect.x , self.rect.y))

class Player(GameSprite):
    def __init__(self,filename,x,y,w,h,speed):
        super().__init__(filename,x,y,w,h)
        self.speed = speed
        self.ammo = 5
        self.reload = 3
        self.reload_timer = 0
        self.is_reloading = False

    def update(self):
        global dt
        keys_pressed = key.get_pressed()

        #первый спрайт
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed * dt

        if keys_pressed[K_d] and self.rect.x < 700-5-self.rect.w:
            self.rect.x += self.speed * dt 

        if self.is_reloading:
            self.reload_timer += dt
            if self.reload_timer >= self.reload:
                self.is_reloading = False 
                self.ammo = 5

    def fire(self):
        global bullets
        if self.ammo > 0:
            self.ammo -= 1 
            fire.play()
            bullet = Bullet('bullet.png',self.rect.centerx-10, self.rect.top, 20, 40, 300)
            bullets.add(bullet)
            if self.ammo == 0 :
                self.is_reloading = True
                self.reload_timer = 0



class Bullet(GameSprite):
    def __init__(self,filename,x,y,w,h,speed):
        super().__init__(filename,x,y,w,h)
        self.speed = speed

    def update(self):
        global dt

        self.rect.y -= self.speed * dt
        if self.rect.y < 0-self.rect.h:
            self.kill()
        





class Enemy(GameSprite):
    def __init__(self,filename,w,h):
        super().__init__(filename,0,0,w,h)
        self.reset()
        self.pos_y = randint(-250,-self.rect.h)
        
    def reset(self):
        self.rect.x = randint(0,700-self.rect.w)
        self.rect.y = - self.rect.h
        self.pos_y = self.rect.y
        self.speed = randint(50,70)

    def update(self):
        global dt,miss_score
        self.pos_y += self.speed * dt
        self.rect.y = self.pos_y
        if self.rect.y > 500 :
            miss_score += 1
            self.reset()

    
class Asteroid(GameSprite):
    def __init__(self,filename,w,h):
        super().__init__(filename,0,0,w,h)
        self.reset()
        self.pos_y = randint(-250,-self.rect.h)
        
    def reset(self):
        self.rect.x = randint(0,700-self.rect.w)
        self.rect.y = - self.rect.h
        self.pos_y = self.rect.y
        self.speed = randint(250,300)

    def update(self):
        global dt,miss_score
        self.pos_y += self.speed * dt
        self.rect.y = self.pos_y
        if self.rect.y > 500 :
            self.reset()


enemies = sprite.Group()
enemies.add(Enemy('ufo.png',80,48))
enemies.add(Enemy('ufo.png',80,48))
enemies.add(Enemy('ufo.png',80,48))
enemies.add(Enemy('ufo.png',80,48))
enemies.add(Enemy('ufo.png',80,48))

asteroids = sprite.Group()
asteroids.add(Asteroid('asteroid.png',48,48))
asteroids.add(Asteroid('asteroid.png',48,48))
asteroids.add(Asteroid('asteroid.png',48,48))


bullets = sprite.Group()


        

player = Player('rocket.png',350,400,70,100,300)

miss_score = 0
score = 0

game = True
finish = False 
result = ''

while game:
    for evt in event.get():
        if evt.type == QUIT:
            game = False
        elif evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                player.fire()
                event.set_grab(True)
                mouse.set_visible(False)


        elif evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                event.set_grab(False)
                mouse.set_visible(True)
            elif finish and evt.key == K_r:
                for enemy in enemies:
                    enemy.reset()
                    enemy.pos_y = randint(-250,-enemy.rect.h)

                for asteroid in asteroids:
                    asteroid.reset()
                    asteroid.pos_y = randint(-250,-asteroid.rect.h)

                bullets.empty()

                finish = False 
                miss_score = 0 
                score = 0 
                player.rect.centerx = 350
                player.is_reloading = False
                player.ammo = 5

    if not finish:
        player.update()
        enemies.update()
        bullets.update()
        asteroids.update()

        collided = sprite.groupcollide(enemies,bullets,False,True)
        for enemy in collided:
            enemy.reset()
            score += 1
        if sprite.spritecollide(player,enemies,False):
            finish = True
            result = 'lose'

        if sprite.spritecollide(player,asteroids,False):
            finish = True
            result = 'lose'

        if miss_score >= 3:
            finish = True
            result = 'lose'
            
        if score >= 25:
            finish = True
            result = 'win'
            

         

    

    


    window.blit(background,(0,0)) 
    player.draw()
    enemies.draw(window)
    bullets.draw(window)
    asteroids.draw(window)



    








    draw_counter(10,30,f'Пропущено: {miss_score}')
    draw_counter(10,10,f'Баллы: {score}')

    if player.is_reloading:
        draw_result(f'reloading {round(player.reload - player.reload_timer,1)}',350,480,30,(255,255,255))

    if finish:
        if result == 'win':
            draw_result('YOU WIN',350,250,60,(100,255,100))
        elif result == 'lose':
            draw_result('YOU LOSE',350,250,60,(255,100,100))

    display.update()
    dt = clock.tick(120) / 1000






    













    



