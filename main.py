'''Version 6'''

import pygame  # imports pygame library
import random  # imports the random library
from os import path
'''Constants'''

# Game screen
WIDTH = 480  # screen is 480px wide
HEIGHT = 600  # screen is 600px tall
FPS = 60  # 60 frames per second

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
'''Images'''

pygame.init()  # initialises the pygame library
pygame.mixer.init(
)  # initialises the mixer module for sound loading and playback
screen = pygame.display.set_mode(
    (WIDTH,
     HEIGHT))  #creates a screen that has the already decided width and height
pygame.display.set_caption(
    "Shmup!")  # presents the title of the game (a shmup)
clock = pygame.time.Clock()  # creates an object to to help track time

font_name = pygame.font.match_font(
    'arial')  # assigns the arial font to 'font_name'


def draw_text(
    surf, text, size, x, y
):  # function to draw text (paramters are the surface, the actual text and position)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()  # creates border for the text
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)  # draws the text onto the surface

def newmob(): # function to create new mobs when some are destroyed
      m = Mob()
      all_sprites.add(m)
      mobs.add(m)

def draw_shield_bar(surf, x, y, pct): # function to draw the shield bar
    if pct < 0:
        pct = 0

    # dimensions of the shield bar
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) # creates border for the outline
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT) # creates border for the filled in part
    pygame.draw.rect(surf, GREEN, fill_rect) # draws the green portion of the shield bar
    pygame.draw.rect(surf, WHITE, outline_rect, 2) # draws the white outline

'''Classes'''


class Player(pygame.sprite.Sprite):  # defines the player sprite

    def __init__(self):  # defines the characteristics of the sprite
        pygame.sprite.Sprite.__init__(self)  # initialises the sprite
        self.image = playerShip  # makes the sprite 50px by 40px
        self.image = pygame.transform.scale(playerShip,
                                            (50, 38))  # shrink image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(
        )  # creates a border/rectangle around the sprite
        self.radius = 20  # defines the radius of the circle as 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # creates a red circle on top of the player sprite to help indicate its hitbox
        self.rect.centerx = WIDTH / 2  # this calculates where the centre of the screen is in terms of the x co-ords
        self.rect.bottom = HEIGHT - 10  # this calculates the point at the bottom of the border (10 px up from the bottom)
        self.speedx = 0  # creates a variable which tracks how fast the player (sprite) is moving along the x co-ords
        self.shield = 100 # the shield starts off with a 'strength' of 100
        self.shoot_delay = 250 # measures how long (in milliseconds) the ship should wait before launching another bullet
        self.last_shot = pygame.time.get_ticks() # keeps track of the time the last bullet was fired

    def update(
        self
    ):  # defines how the sprite will change, on each frame, as the game progresses
        self.speedx = 0  # this is set to 0 to allow smoother movement (every time key is pressed, speed resets)
        keystate = pygame.key.get_pressed(
        )  # sets up an event where a key on the keyboard is pressed
        if keystate[pygame.K_LEFT]:  # if you press the left arrow key
            self.speedx = -8  # the player moves to the left of where it originally was
        if keystate[pygame.K_RIGHT]:  # if you press the right arrow key
            self.speedx = 8  # the player moves to the right of where it originally was
        if keystate[pygame.K_SPACE]:
            self.shoot() # as long as user holds down space bar the player will shoot
        self.rect.x += self.speedx  # the sprite's border is meant to move at the same speed as the actual sprite
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        # the above ensures that the player sprite does not go off screen

    def shoot(self):  # player shooting function
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
          self.last_shot = now
          bullet = Bullet(self.rect.centerx, self.rect.top) # aligns bullet to the centre of player but above them
          all_sprites.add(bullet) # adds bullet to the sprite group
          bullets.add(bullet) # adds each bullet to the list of bullets
          shoot_sound.play() # plays the shoot sound when bullet is shot


class Mob(pygame.sprite.Sprite):  # defines the enemy sprite

    def __init__(self):  # defines the characteristics of the sprite
        pygame.sprite.Sprite.__init__(self)  # initialises the sprite
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect(
        )  # creates a border around this sprite as well
        self.radius = int(
            self.rect.width * .85 / 2
        )  # means that a bit of the meteors stick out underneath the circle
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # also creates a red circle to indicate its hitbox
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        # above lines mean that the mob sprite appears at random co-ords (though always above the top of the screen)
        self.speedy = random.randrange(
            1, 8
        )  # means that the mob sprite moves down the screen by a random value (chosen from between 1 and 8)
        self.speedx = random.randrange(
            -3, 3
        )  # means that the mobs don't move straight down, but diagonally (as x value is randomised)
        self.rot = 0  # measures how many degrees meteors should be rotated (starts off at 0)
        self.rot_speed = random.randrange(
            -8, 8
        )  # measures how many degrees the sprite should rotate each time (bigger numbers = faster rotation) - the value chosen is random due to 'randrange'
        self.last_update = pygame.time.get_ticks(
        )  # measures how many milliseconds have elapsed since the clock started

    def rotate(
            self):  # function that dictates how rotations work in the program
        now = pygame.time.get_ticks()  # checks what time it is currently
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            # above lines mean that if 50 milliseconds have elapsed, a rotation must occur - also updates the value of rot and applies the rotation to the original image
            old_center = self.rect.center  # records the old location of the rectangle's center
            self.image = new_image
            self.rect = self.image.get_rect()  # calculates the new rectangle
            self.rect.center = old_center  # sets the center to the saved one

    def update(self):
        self.rotate()  # runs the rotate function
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:  # if the sprite goes off the bottom/side of the screen...
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        # above lines move the sprite back to a random position above the top

class Bullet(pygame.sprite.Sprite
             ):  # defines the bullet sprite that will be shot from the player

    def __init__(
        self, x, y
    ):  # defines the characteristics of the sprite and tells it where to appear (which is where the player happens to be at that time)
        pygame.sprite.Sprite.__init__(self)  # initialises the sprite
        self.image = laser
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # creates a border
        self.rect.bottom = y  # assigns the bottom of the border with the top of the screen
        self.rect.centerx = x  # assigns the centre of the border with value x
        self.speedy = -10  # means that the bullet will always move upwards

    def update(self):  # governs how the bullet will change as game goes on
        self.rect.y += self.speedy
        # below lines kill bullet if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


# Load all game graphics
background = pygame.image.load("starfield.png").convert()
background_rect = background.get_rect()
laser = pygame.image.load("laserBlue14.png").convert()

meteor1 = pygame.image.load('meteorGrey_big1.png').convert()
meteor2 = pygame.image.load('meteorGrey_med1.png').convert()
meteor3 = pygame.image.load('meteorGrey_small1.png').convert()
meteor4 = pygame.image.load('meteorGrey_tiny1.png').convert()

playerShip = pygame.image.load("playerShip1_blue.png").convert()

meteor_images = [meteor1, meteor2, meteor3, meteor4]

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

#Load all sound files
shoot_sound = pygame.mixer.Sound("pew.wav")
expl_sound1 = pygame.mixer.Sound("expl3.wav")
expl_sound2 = pygame.mixer.Sound("expl6.wav")

expl_sounds = [expl_sound1, expl_sound2]

pygame.mixer.music.load("tgfcoder-FrozenJam-SeamlessLoop.ogg")
pygame.mixer.music.set_volume(0.4) # makes music slightly quieter

all_sprites = pygame.sprite.Group(
)  # creates a group called 'all_sprites' which will contain all the sprites
player = Player()  # instantiates the player sprite
all_sprites.add(player)  # adds the player (class) to the group
mobs = pygame.sprite.Group()  # makes list for all the mobs
bullets = pygame.sprite.Group()  # makes list for all the bullets
for i in range(8):
  newmob()
  
score = 0
pygame.mixer.music.play(loops=-1) # repeats music literally
'''Game loop'''

running = True
while running:  # while the game has started
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False  # if the player has chosen to quit the game, the game stops running
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                # checks if the user has pressed the space key to shoot, if this is true, a bullet is shot

    # Update
    all_sprites.update(
    )  # runs function update() to all of the sprites, meaning that they all react to key presses

    hits = pygame.sprite.groupcollide(
        mobs, bullets, True, True
    )  # records/tracks the collisions between bullets and mobs - if this occurs, triggers mob being destroyed -> means meteors are destroyed when hit and don't continue to exist
    for hit in hits:
        score += 50 - hit.radius # score increases based on the size of meteors
        random.choice(expl_sounds).play() # plays a random choice of sounds
        newmob() # generates new meteors

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2 # for every collision, the shield becomes weaker
        newmob() # more meteors are generated
        if player.shield <= 0:
            running = False # game ends when shield is destroyed

    # Draw / render
    screen.fill(BLACK)  # fill the screen with black
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # draw all of the sprites onto the screen so that they can be seen
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield) # draws the shield bar
    # *after* drawing everything, flip the display
    pygame.display.flip()  # updates the full display surface to the screen

pygame.quit()  # end the game
