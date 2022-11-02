import math
import random
import pygame
pygame.init()

sh = 800
sw = 800

run = True
clock = pygame.time.Clock()
gameover = False
life = 3

bg = pygame.image.load('assets/spaceBG.png')
player = pygame.image.load('assets/player.png')
asteroids_small = pygame.image.load('assets/AsteroidS.png')
asteroids_medium = pygame.image.load('assets/AsteroidM.png')
asteroids_large = pygame.image.load('assets/AsteroidL.png')

pygame.display.set_caption('Asteroids')
win = pygame.display.set_mode((sw, sh))


# Player and control class
class Player(object):
    def __init__(self):
        self.img = player
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw // 2
        self.y = sh // 2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians((self.angle + 90)))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def draw(self, win):
        #win.blit(self.img, [self.x, self.y, self.w, self.h])
        win.blit(self.rotatedSurf, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def updateLocation(self):
        if self.x > sw + 50:
            self. x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0

# Bullet Class
class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return True


# Asteroid class
class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroids_small
        elif self.rank == 2:
            self.image = asteroids_medium
        else:
            self.image = asteroids_large
        self.w = 50 * rank
        self.h =50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])), (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir =1
        else:
            self.xdir = -1

        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1, 3)
        self.yv = self.ydir * random.randrange(1, 3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))



# To display assets on screen
def redrawGameWindow():
    win.blit(bg, (0, 0))
    font = pygame.font.SysFont('corbel', 30)
    lifeText = font.render('Lives: '+ str(life), 1, (255, 255, 255))
    playAgain = font.render('Press Space to play again', 1, (255, 255, 255))
    scoreText = font.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(lifeText, (25, 25))
    if gameover:
        win.blit(playAgain, (sw//2 - playAgain.get_width()//2, sh//2 - playAgain.get_height()//2))
    win.blit(scoreText, (sw - scoreText.get_width() - 25, 25))

    player.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullet:
        b.draw(win)


    pygame.display.update()


player = Player()
playerBullet = []
asteroids = []
count = 0
score = 0


# game loop // running
while run:
    clock.tick(60)
    count += 1
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid(ran))
        player.updateLocation()
        for b in playerBullet:
            b.move()
            if b.checkOffScreen():
                playerBullet.pop(playerBullet.index(b))

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv



            if (player.x >= a.x and player.x <= a.x + a.w) or (player.x + player.w >= a.x and player.x + player.w <= a.x + a.w):
                if (player.y >= a.y and player.y <= a.y + a.h) or (player. y + player.h >= a.y and player.y + player.h <= a.y + a.h):
                    life -= 1
                    asteroids.pop(asteroids.index(a))
                    break


            # bullet collision
            for b in playerBullet:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and  b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            score += 5
                            na1 = Asteroid(2)
                            na2 = Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            score += 10
                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 20
                        asteroids.pop(asteroids.index(a))
                        playerBullet.pop(playerBullet.index(b))

        if life <= 0:
            gameover = True


        # game controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.turnLeft()
        if keys[pygame.K_d]:
            player.turnRight()
        if keys[pygame.K_w]:
            player.moveForward()



    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    playerBullet.append(Bullet())
                else:
                    gameover = False
                    life = 3
                    score = 0
                    asteroids.clear()


    redrawGameWindow()

pygame.quit()