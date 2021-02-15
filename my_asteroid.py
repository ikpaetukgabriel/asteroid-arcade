"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
from abc import ABC, abstractmethod
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2


class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def initiate_asteroid_x(self, start):
        if start == 1:
            return 0
        elif start == 2:
            return 800
        elif start == 3:
            return random.randint(50, 750)
        else:
            return random.randint(50, 750)

    def initiate_asteroid_y(self, start):
        if start == 1:
            return random.randint(50, 550)
        elif start == 2:
            return random.randint(50, 550)
        elif start == 3:
            return 0
        else:
            return 600

class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0


class FlyingObject(ABC):
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.angle = 0
        self.rotate = 0
        self.rotation = 0


    def wrap(self):
        if self.center.x > SCREEN_WIDTH:
            self.center.x = 0

        if self.center.x < 0:
            self.center.x = SCREEN_WIDTH

        if self.center.y > SCREEN_HEIGHT:
            self.center.y = 0

        if self.center.y < 0:
            self.center.y = SCREEN_HEIGHT



    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        self.rotate += self.rotation
        if self.rotate == 359:
            self.rotate = 0

    @abstractmethod
    def draw(self):
        pass




class Ship(FlyingObject):
    def __init__(self):
        super().__init__()
        self.rotate = SHIP_TURN_AMOUNT
        self.radius = SHIP_RADIUS
        self.center.x = SCREEN_WIDTH // 2
        self.center.y = SCREEN_HEIGHT // 2


    def draw(self):
        texture = arcade.load_texture('ship.png')
        angle = self.angle - 90
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width * 0.5, texture.height * 0.5, texture, angle)


    def rotate_right(self):
        self.angle -= SHIP_TURN_AMOUNT

    def rotate_left(self):
        self.angle += SHIP_TURN_AMOUNT

    def move_forward(self):
        self.velocity.dx += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    def reduce_speed(self):
        self.velocity.dx -= (SHIP_THRUST_AMOUNT / 2)
        if self.velocity.dx < 0:
            self.velocity.dx = 0

        self.velocity.dy -= (SHIP_THRUST_AMOUNT / 2)
        if self.velocity.dy < 0:
            self.velocity.dy = 0


class Bullet(FlyingObject):

    def __init__(self):
        super().__init__()
        self.frame = 0
        self.radius = BULLET_RADIUS

    def draw(self):
        texture = arcade.load_texture('laser.png')
        angle = self.angle - 90
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width * 0.5, texture.height * 0.5, texture, angle)

    def fire_bullet(self, ship_angle, ship_velocity_x, ship_velocity_y):
        self.velocity.dx = ship_velocity_x + math.cos(math.radians(ship_angle)) * BULLET_SPEED
        self.velocity.dy = ship_velocity_y + math.sin(math.radians(ship_angle)) * BULLET_SPEED


class Angle():
    def __init__(self):
        pass

    def initiate_angle(self, start):
        if start == 1:
            return random.randint(-30, 30)
        elif start == 2:
            return random.randint(150, 210)
        elif start == 3:
            return random.randint(60, 120)
        else:
            return random.randint(240, 300)

class Asteroid(FlyingObject, ABC):

    def __init__(self):
        super().__init__()
        self.start = random.randint(1,4)

        self.center.x = self.center.initiate_asteroid_x(self.start)
        self.center.y = self.center.initiate_asteroid_y(self.start)

        angle = Angle()
        self.direction = angle.initiate_angle(self.start)

        self.velocity.dx = math.cos(math.radians(self.direction)) * BIG_ROCK_SPEED
        self.velocity.dy = math.sin(math.radians(self.direction)) * BIG_ROCK_SPEED

        self.radius = BIG_ROCK_RADIUS

        self.rotation = 0

        self.dr = 1

        self.texture = arcade.load_texture("big.png")

    def spin(self):
        self.rotation += self.dr

    @abstractmethod
    def split(self):
        pass

    @abstractmethod
    def hit_ship(self):
        pass


class BigAsteroid(Asteroid):

    def __init__(self):
        super().__init__()
        self.health = 2
        self.dr = BIG_ROCK_SPIN

    def split(self):
        self.health -= 1

        if self.health == 0:
            list = [MediumAsteroid(self.center.x, self.center.y, self.velocity.dx, self.velocity.dy + 2),
                    MediumAsteroid(self.center.x, self.center.y, self.velocity.dx, self.velocity.dy - 2),
                    SmallAsteroid(self.center.x, self.center.y, self.velocity.dx + 5, self.velocity.dy)]
            self.alive = False
        else:
            list = []
        return list

    def hit_ship(self):
        return 6


class MediumAsteroid(Asteroid):

    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.velocity.dx = dx
        self.velocity.dy = dy
        self.radius = MEDIUM_ROCK_RADIUS
        self.texture = arcade.load_texture("medium.png")
        self.width = 35
        self.height = 35
        self.dr = MEDIUM_ROCK_SPIN

    def split(self):
        list = [SmallAsteroid(self.center.x, self.center.y, self.velocity.dx + 1.5, self.velocity.dy + 1.5),
                SmallAsteroid(self.center.x, self.center.y, self.velocity.dx - 1.5, self.velocity.dy - 1.5), ]

        self.alive = False

        return list

    def hit_ship(self):
        return 5


class SmallAsteroid(Asteroid):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.velocity.dx = dx
        self.velocity.dy = dy
        self.radius = SMALL_ROCK_RADIUS
        self.texture = arcade.load_texture("small.png")
        self.width = 22
        self.height = 22
        self.dr = SMALL_ROCK_SPIN

    def split(self):
        list = []

        self.alive = False
        return list

    def hit_ship(self):
        return 3














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
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        self.ship = Ship()
        self.bullets = []
        self.asteroids = []
        self.asteroid


    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        self.ship.draw()

        for bullet in self.bullets:
            bullet.draw()



    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        # TODO: Tell everything to advance or move forward one step in time
        self.ship.advance()
        self.ship.wrap()

        for bullet in self.bullets:
            bullet.advance()
            bullet.frame += 1
            if bullet.frame == BULLET_LIFE:
                bullet.alive = False
                bullet.frame = 0


        # TODO: Check for collisions

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
            self.ship.move_forward()

        if arcade.key.DOWN in self.held_keys:
            self.ship.reduce_speed()



        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullet()
                bullet.center.x = self.ship.center.x
                bullet.center.y = self.ship.center.y
                ship_velocity_dx = self.ship.velocity.dx
                ship_velocity_dy = self.ship.velocity.dy
                angle_of_bullet, bullet.angle = self.ship.angle, self.ship.angle + 90
                bullet.fire_bullet(angle_of_bullet, ship_velocity_dx, ship_velocity_dy)
                self.bullets.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()