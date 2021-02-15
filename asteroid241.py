"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
# ---ADDED FEATURES---
# A MONSTER SHOWS UP TO FIRE LASER AFTER ALL ASTEROIDS HAVE BEEN DESTROYED
# SOUND WHEN THE SHIP FIRES LASER
# A HEALTH BAR ON THE TOP OF THE SCREEN FOR THE SHIP
# A HEALTH BAR FOR THE MONSTER WHEN IT SHOW UP
# CHANGED THE ORIGINAL SPACE BACKGROUND TO A DESIRED IMAGE
# INCREASED THE INITIAL ASTEROID COUNT
# THE GAME AS THE ABILITY TO RESTART AND PLAY AGAIN AFTER A WIN OR LOSS
# AS FOR THE SHIELD FEATURE (WORKED ON THIS WITH A CLASS MEMBER, ERIC IZEKOR, AND OTHER TEAM MEMBERS)




import arcade
import random
import math
from abc import ABC, abstractmethod

MONSTER_SPEED = 2
MONSTER_SCALE = 0.25
MONSTER_LASER_SCALE = .10
MONSTER_LIVE = 500


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60
BULLET_SCALE = .75

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30
SHIP_SCALE = .75

SHIELD_RADIUS = 63
SHIELD_SCALE = .75

INITIAL_ROCK_COUNT = 10
ASTEROID_SCALE = .75

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2


class Point:
    """ Initialize of point used by objects in the game"""
    def __init__(self):
        self.x = 0
        self.y = 0


class Velocity:
    """ Initialize velocity object, used by Ship, Bullet, Asteroids, Monster and Monster Laser """

    def __init__(self):
        self.dx = 0
        self.dy = 0


class FlyingObject(ABC):
    """ Initialize of all flying object """
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.angle = 0
        self.object = -1
        self.rotate = 0
        self.alive = True
        self.rotation = 0

    def advance(self):
        """
        In charge of flying objects movement
        """
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        self.rotate += self.rotation
        if self.rotate == 359:
            self.rotate = 0

    def engage_wrap(self):
        """
        In charge of flying objects wraps
        """
        if self.center.x > SCREEN_WIDTH:
            # MOVE TO THE LEFT
            self.center.x = 0

        elif self.center.x < 0:
            # MOVE TO THE RIGHT
            self.center.x = SCREEN_WIDTH

        elif self.center.y > SCREEN_HEIGHT:
            # MOVE TO THE BOTTOM
            self.center.y = 0

        elif self.center.y < 0:
            # MOVE TO THE TOP
            self.center.y = SCREEN_HEIGHT

    @abstractmethod
    def draw(self):
        pass


class Shield(FlyingObject):
    """ Initialize of a Shield object, which utilizes class: Ship """

    def __init__(self, ship):
        self.ship = ship
        super().__init__()
        self.radius = SHIELD_RADIUS
        self.scale = SHIELD_SCALE
        self.shield_type = 6

        # Sounds
        #self.shield_down_sound = arcade.load_sound("sfx_shieldDown.ogg")

    def draw(self):
        """
        In charge of drawing ship shield
        """
        self.center.x = self.ship.center.x
        self.center.y = self.ship.center.y
        self.angle = self.ship.angle

        if self.shield_type == 6:
            # WHOLE SHIELD
            texture = arcade.load_texture("shield3.png")
            angle = self.angle - 90
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture, angle)

        elif self.shield_type == 5:
            # PARTIALLY AFFECTED SHIELD
            texture = arcade.load_texture("shield2.png")
            angle = self.angle - 90
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture, angle)

        elif self.shield_type == 4:
            # MAJORLY AFFECTED SHIELD
            texture = arcade.load_texture("shield1.png")
            angle = self.angle - 90
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture, angle)

        elif self.shield_type == 2:
            # DAMAGED SHIELD
            texture = arcade.load_texture("ship_damage.png")
            angle = self.angle - 90
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture, angle)

        elif self.shield_type < 2:
            # KILLS SHIP AFTER CERTAIN NUMBER OF HITS
            self.ship.alive = False


class Ship(FlyingObject):
    """ Initialize of a Ship object, which utilizes class: flyingObject """

    def __init__(self):
        super().__init__()
        self.radius = SHIP_RADIUS
        self.center.x = SCREEN_WIDTH - 50
        self.center.y = 50
        self.scale = SHIP_SCALE

    def draw(self):
        """
        In charge of drawing ship
        """
        texture = arcade.load_texture("ship.png")
        angle = self.angle - 90
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture, angle)

    # SHIP THRUST FORWARD
    def thrust_forward(self):
        self.velocity.dx += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    # SHIP THRUST BACKWARD
    def thrust_backward(self):
        self.velocity.dx -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    # SHIP ROTATE RIGHT
    def rotate_right(self):
        self.angle -= SHIP_TURN_AMOUNT

    # SHIP ROTATE LEFT
    def rotate_left(self):
        self.angle += SHIP_TURN_AMOUNT


class Bullet(FlyingObject):
    """ Initialize of a Bullet object, which utilizes class: flyingObject """

    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        self.scale = BULLET_SCALE
        self.frame_counter = 0
        self.laser_sound = arcade.load_sound('laser.wav')


    def draw(self):
        """
        In charge of drawing ship bullet
        """
        texture = arcade.load_texture("laser.png")
        angle = self.angle - 90
        # Draw bullet
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture, angle)

    def fire_bullet(self, angle, ship_velocity_dx, ship_velocity_dy):
        """
        In charge of firing ship bullet, direction and speed wise
        """
        self.velocity.dx = ship_velocity_dx + math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = ship_velocity_dy + math.sin(math.radians(angle)) * BULLET_SPEED


class Asteroid(FlyingObject):
    """ Initialize of an Asteroid object, which utilizes class: flyingObject """

    def __init__(self):
        super().__init__()
        self.scale = ASTEROID_SCALE
        self.asteroid_type = 0
        self.radius = 0

    def get_center_x(self):
        return self.center.x

    def get_center_y(self):
        return self.center.y

    def draw(self):
        """
        In charge of drawing asteroids
        """
        if self.asteroid_type == 0:
            self.radius = BIG_ROCK_RADIUS
        elif self.asteroid_type == 1:
            self.radius = MEDIUM_ROCK_RADIUS
        elif self.asteroid_type == 2 or self.asteroid_type == 3:
            self.radius = SMALL_ROCK_RADIUS

        if self.asteroid_type == 0:
            # BIG ASTEROID
            texture = arcade.load_texture("big.png")
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture, 90 - self.rotate)

        if self.asteroid_type == 1:
            # MEDIUM ASTEROID
            texture = arcade.load_texture("medium.png")
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture, 90 - self.rotate)

        if self.asteroid_type == 2 or self.asteroid_type == 3:
            # SMALL ASTEROID
            texture = arcade.load_texture("small.png")
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture, 90 - self.rotate)


class Monster(FlyingObject):
    """ Initialize of an Monster object, which utilizes class: flyingObject """
    def __init__(self):
        super().__init__()
        self.alive = False
        self.scale = MONSTER_SCALE
        self.texture = arcade.load_texture("Monster_spaceship.png")
        self.center.x = 0 + ((self.texture.width * MONSTER_SCALE) // 2)
        self.movement = 2
        self.live = MONSTER_LIVE
        self.radius = (self.texture.height * self.scale) / 2

    def advance(self):
        """
        In charge of Monster movement
        """
        self.center.y += self.movement

    def draw(self):
        """
        In charge of drawing monster
        """
        texture = self.texture
        angle = self.angle - 90
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * texture.width, self.scale * texture.height, texture)

    def engage_wrap(self):
        """
        In charge of monster wrap, note, monster wraps differently from other flying objects
        """
        if self.center.y > SCREEN_HEIGHT:
            self.center.y = SCREEN_HEIGHT
            self.movement *= -1

        elif self.center.y < 0:
            self.center.y = 0
            self.movement *= -1


class MonsterLaser():
    """ Initialize of a monster laser, not a flying object"""
    def __init__(self):
        self.scale = MONSTER_LASER_SCALE
        self.center = Point()
        self.velocity = Velocity()
        self.center.x = 0 + 200
        self.texture = arcade.load_texture("ml.png")
        self.radius = (self.texture.width * self.scale) / 2

    def draw(self, monster_y):
        """
        In charge of drawing monster laser
        """
        self.center.y = monster_y
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.scale * self.texture.width,
                                      self.scale * self.texture.height, self.texture)

    def advance(self):
        """
        In charge of monster laser movement
        """
        self.center.x += BULLET_SPEED


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.held_keys = set()

        self.asteroids = []
        self.asteroid_med_counter = 0
        self.asteroid_small_counter = 0
        self.ship = Ship()
        self.shield = Shield(self.ship)
        self.bullets = []
        self.monster_lasers = []
        self.monster = Monster()
        self.game_over = False
        self.timer = 0
        self.game_win = False


    def setup(self):
        """ Initial game set up, only called to create the game from start """

        self.background = arcade.load_texture("space123.jpeg")  # LOAD BACKGROUND IMAGE

        # START WITH SET NUMBER OF ASTEROIDS
        for i in range(INITIAL_ROCK_COUNT):
            self.create_target(0, Asteroid())

        # SHIP ANGLE POINTER
        self.ship.angle = 135

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # PRINTS BACKGROUND IMAGE
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # DRAWS SHIP
        if self.ship.alive:
            self.ship.draw()
            self.shield.draw()

        # DRAWS EACH ASTEROID
        for asteroid in self.asteroids:
            asteroid.draw()

        # DRAWS EACH BULLET
        for bullet in self.bullets:
            bullet.draw()

        if self.monster.alive:
            self.monster.draw()

        if self.monster.alive:
            for monster_laser in self.monster_lasers:
                monster_laser.draw(self.monster.center.y)


        if self.game_over:
            # PRINTS IMAGE FOR GAME OVER
            texture = arcade.load_texture("gameover123.png")
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, texture.width * 0.35, texture.height * 0.35, texture,
                                          0)

            # GAME PLAY AGAIN INSTRUCTIONS
            score_text = "********* PRESS ENTER TO PLAY AGAIN *********"
            start_x = (SCREEN_WIDTH / 2) - 180
            start_y = (SCREEN_HEIGHT / 2) - 120
            arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.YELLOW)

        if self.game_win:
            # PRINTS IMAGE FOR GAME WIN
            texture = arcade.load_texture("win.png")
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, texture.width, texture.height,
                                          texture,
                                          0)
            # GAME PLAY AGAIN INSTRUCTIONS
            score_text = "********* PRESS ENTER TO PLAY AGAIN *********"
            start_x = (SCREEN_WIDTH / 2) - 180
            start_y = (SCREEN_HEIGHT / 2) - 120
            arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.YELLOW)

        self.draw_health_ship()
        if self.monster.alive:
            self.draw_health_monster()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_off_screen()
        # Advance ship
        self.ship.advance()
        if self.monster:
            self.monster.advance()
            self.monster.engage_wrap()
        # ADVANCE ASTEROIDS
        for asteroid in self.asteroids:
            asteroid.advance()

        # ADVANCE SHIP BULLETS
        for bullet in self.bullets:
            bullet.advance()
            bullet.frame_counter += 1
            if bullet.frame_counter == BULLET_LIFE:
                bullet.alive = False
                bullet.frame_counter = 0

        for monster_laser in self.monster_lasers:
            monster_laser.advance()

        self.check_collisions()
        self.cleanup_objects()
        self.check_game_over()
        self.check_game_win()

        self.timer += 1
        if self.timer % 200 == 0 and self.monster.alive:
            self.monster_lasers.append(MonsterLaser())

    def create_target(self, target_type, previous_target):
        """
        Creates the correct asteroid, uses polymorphism to modify different attributes of the Asteroid() class and the asteroids it to the list.
        """
        original_angle = random.uniform(0, 360)

        if target_type == 0:  # ASTEROID TYPE ONE CREATION
            asteroid = previous_target
            asteroid.center.x = random.uniform(10, SCREEN_WIDTH * .75)
            asteroid.rotation = BIG_ROCK_SPIN
            asteroid.center.y = random.uniform(SCREEN_HEIGHT * .25, SCREEN_HEIGHT)
            asteroid.velocity.dx = math.cos(math.radians(original_angle)) * BIG_ROCK_SPEED
            asteroid.velocity.dy = math.sin(math.radians(original_angle)) * BIG_ROCK_SPEED
            asteroid.asteroid_type = 0

        elif target_type == 1:  # TWO MEDIUM (large asteroid hit)
            asteroid = Asteroid()
            asteroid.asteroid_type = 1
            if self.asteroid_med_counter == 0:
                asteroid.rotation = MEDIUM_ROCK_SPIN
                asteroid.velocity.dx = previous_target.velocity.dx + 2
                asteroid.velocity.dy = previous_target.velocity.dy
                self.asteroid_med_counter = 1
            elif self.asteroid_med_counter == 1:
                asteroid.rotation = MEDIUM_ROCK_SPIN
                asteroid.velocity.dx = previous_target.velocity.dx - 2
                asteroid.velocity.dy = previous_target.velocity.dy
                self.asteroid_med_counter = 0

            asteroid.center.x = previous_target.center.x
            asteroid.center.y = previous_target.center.y

        elif target_type == 2:  # ONE SMALL ASTEROID FROM BIG
            asteroid = Asteroid()
            asteroid.asteroid_type = 2
            asteroid.rotation = SMALL_ROCK_SPIN
            asteroid.velocity.dx = previous_target.velocity.dx
            asteroid.velocity.dy = previous_target.velocity.dy + 5
            asteroid.center.x = previous_target.center.x
            asteroid.center.y = previous_target.center.y

        elif target_type == 3:  # TWO SMALL ASTEROIDS FROM MEDIUM
            asteroid = Asteroid()
            asteroid.asteroid_type = 3

            if self.asteroid_small_counter == 0:
                asteroid.rotation = SMALL_ROCK_SPIN
                asteroid.velocity.dx = previous_target.velocity.dx + 1.5
                asteroid.velocity.dy = previous_target.velocity.dy + 1.5
                self.asteroid_small_counter = 1
            elif self.asteroid_small_counter == 1:
                asteroid.rotation = SMALL_ROCK_SPIN
                asteroid.velocity.dx = previous_target.velocity.dx - 1.5
                asteroid.velocity.dy = previous_target.velocity.dy - 1.5
                self.asteroid_small_counter = 0

            asteroid.center.x = previous_target.center.x
            asteroid.center.y = previous_target.center.y

        self.asteroids.append(asteroid)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.rotate_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.rotate_right()

        if arcade.key.UP in self.held_keys:
            self.ship.thrust_forward()

        if arcade.key.DOWN in self.held_keys:
            self.ship.thrust_backward()

        # Machine gun mode... (LOVE THIS :)
        if arcade.key.RSHIFT in self.held_keys:
            bullet = Bullet()
            bullet_angle = self.ship.angle
            bullet.angle = self.ship.angle + 90
            bullet.center.x = self.ship.center.x
            bullet.center.y = self.ship.center.y
            ship_velocity_dx = self.ship.velocity.dx
            ship_velocity_dy = self.ship.velocity.dy
            bullet.fire_bullet(bullet_angle, ship_velocity_dx, ship_velocity_dy)
            self.bullets.append(bullet)

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:  # FIRES WHEN SHIP IS ALIVE
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # Fire the bullet here!
                bullet = Bullet()
                bullet_angle = self.ship.angle
                bullet.angle = self.ship.angle + 90
                bullet.center.x = self.ship.center.x
                bullet.center.y = self.ship.center.y
                ship_velocity_dx = self.ship.velocity.dx
                ship_velocity_dy = self.ship.velocity.dy
                bullet.fire_bullet(bullet_angle, ship_velocity_dx, ship_velocity_dy)
                arcade.play_sound(bullet.laser_sound)
                self.bullets.append(bullet)

        # CHECKS TO SEE IF PLAY WANTS TO PLAY AGAIN
        if self.game_over:
            if key == arcade.key.RETURN:
                self.play_again()

        if self.game_win:
            if key == arcade.key.RETURN:
                self.play_again()

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)

    def cleanup_objects(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)

    def check_collisions(self):
        """ Checks to see if anything has collided. Removes dead items. """

        for bullet in self.bullets:
            for asteroid in self.asteroids:

                # MAKING SURE BULLET AND ASTEROID ARE ALIVE BEFORE THIS WORKS
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                            abs(bullet.center.y - asteroid.center.y) < too_close):
                        # A HIT!!!!!!!!!!
                        bullet.alive = False
                        asteroid.alive = False

                        if asteroid.asteroid_type == 0:
                            self.create_target(2, asteroid)
                            self.create_target(1, asteroid)
                            self.create_target(1, asteroid)

                        elif asteroid.asteroid_type == 1:
                            self.create_target(3, asteroid)
                            self.create_target(3, asteroid)

        for monster_laser in self.monster_lasers:
            # MAKING SURE SHIP IS ALIVE BEFORE IT WORKS
            if self.ship.alive:
                too_close = monster_laser.radius + self.ship.radius
                if (abs(monster_laser.center.x - self.ship.center.x) < too_close and
                        abs(monster_laser.center.y - self.ship.center.y) < too_close):
                    # A HIT!!!!!!!!!!
                    if self.ship.alive and self.shield.shield_type == -1:
                        self.ship.alive = False
                    else:
                        self.shield.shield_type -= 0.1

        # IN CHARGE OF SHIP BULLET COLLISION WITH THE MONSTER, IF BOTH ALIVE
        for bullet in self.bullets:
            if bullet.alive and self.monster.alive:
                    too_close = bullet.radius + self.monster.radius
                    if (abs(bullet.center.x - self.monster.center.x) < too_close and
                            abs(bullet.center.y - self.monster.center.y) < too_close):
                        # A HIT!!!!!!!!!!
                        bullet.alive = False
                        self.monster.live -= 1
                        if self.monster.live == 0:
                            self.monster.alive = False

        # IN CHARGE OF KILLING SHIP UPON COLLISION
        for asteroid in self.asteroids:
            if asteroid.alive and self.ship.alive and self.shield.shield_type == -1:

                too_close = asteroid.radius + self.ship.radius
                if (abs(self.ship.center.x - asteroid.center.x) < too_close and
                        abs(self.ship.center.y - asteroid.center.y) < too_close):
                    asteroid.alive = False
                    self.ship.alive = False

        # DECREASES SHIP SHIELD UPON COLLISION
        for asteroid in self.asteroids:
            if asteroid.alive and self.ship.alive:

                too_close = asteroid.radius + self.shield.radius
                if (abs(self.shield.center.x - asteroid.center.x) < too_close and
                        abs(self.shield.center.y - asteroid.center.y) < too_close):
                    #arcade.play_sound(self.shield.shield_down_sound)
                    asteroid.alive = False
                    self.shield.shield_type -= 1

    def check_off_screen(self):
        """
        Checks to see if any object has left the screen
        """

        for asteroid in self.asteroids:
            asteroid.engage_wrap()

        for bullet in self.bullets:
            bullet.engage_wrap()

        self.ship.engage_wrap()

    def draw_health_ship(self):
        if self.shield.shield_type == 6:
            self.health = 100
        elif self.shield.shield_type == 5:
            self.health = 83
        elif self.shield.shield_type == 4:
            self.health = 66
        elif self.shield.shield_type == 3:
            self.health = 50
        elif self.shield.shield_type == 2:
            self.health = 33
        elif self.shield.shield_type == 1:
            self.health = 0

        arcade.draw_rectangle_filled(SCREEN_WIDTH / 1.8, SCREEN_HEIGHT - 10, self.health, 10, arcade.color.FIREBRICK)
        arcade.draw_rectangle_outline(SCREEN_WIDTH / 1.8, SCREEN_HEIGHT - 10, 100, 10, arcade.color.WHITE)
        arcade.draw_text("SHIP LIFE:", start_x=SCREEN_WIDTH / 2.6, start_y=SCREEN_HEIGHT - 15, font_size=12,
                             color=arcade.color.WHITE)

    def draw_health_monster(self):
        if self.monster.live == 500:
            self.m_health = 100
        elif 400 <= self.monster.live < 500:
            self.m_health = 83
        elif 300 <= self.monster.live < 400:
            self.m_health = 66
        elif 200 <= self.monster.live < 300:
            self.m_health = 50
        elif 100 <= self.monster.live < 200:
            self.m_health = 33
        elif 0 < self.monster.live < 100:
            self.m_health = 16
        elif self.monster.live == 0:
            self.m_health = 0

        arcade.draw_rectangle_filled(190, SCREEN_HEIGHT - 10, self.m_health, 10, arcade.color.GREEN)
        arcade.draw_rectangle_outline(190, SCREEN_HEIGHT - 10, 100, 10, arcade.color.WHITE)
        arcade.draw_text("MONSTER LIFE:", start_x=10, start_y=SCREEN_HEIGHT - 15, font_size=12,
                             color=arcade.color.WHITE)


    def check_game_over(self):
        if not self.ship.alive:
            self.game_over = True
        else:
            self.game_over = False
        return self.game_over


    def check_game_win(self):
        """
        Check to see game's current state, and acts as needed
        """
        if not self.asteroids and self.monster.live > 0:
            self.monster.alive = True
        elif not self.monster.alive and not self.asteroids:
            self.game_win = True
        else:
            self.game_win = False
        return self.game_win

    def play_again(self):
        """
        Provides the possibility for the game to reset to starting point,
        after player decides to play again
        """
        self.held_keys = set()

        self.asteroids = []
        self.asteroid_med_counter = 0
        self.asteroid_small_counter = 0
        self.ship = Ship()
        self.shield = Shield(self.ship)
        self.bullets = []
        self.monster_lasers = []
        self.monster = Monster()
        self.game_over = False
        self.timer = 0
        self.game_win = False
        self.setup()


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
window.setup()
arcade.run()