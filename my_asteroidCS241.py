import random
import arcade
from abc import abstractmethod
from abc import ABC
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GAME_INTRO = 0
GAME_RUN = 1
GAME_DEATH = 2
GAME_WIN = 3

LASER_RADIUS = 11
LASER_SPEED = 10
LASER_LIFE = 60

SHIP_THRUST_AMOUNT = 3
SHIP_RADIUS = 18
SHIP_HEALTH = 15

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 23

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 15

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 9


class Point:

    def __init__(self):
        # this will be generating the center for the object.
        self.x = 0
        self.y = 0

    def initiate_asteroid_x(self, start):
        """
        The object will pass  in random start number
        This number will decide which side of the screen the
        asteroid will spawn at.
        This function will return the x point.
        """
        # left side
        if start == 1:
            return 0
        # right side
        elif start == 2:
            return 800
        # bottom
        elif start == 3:
            return random.randint(50, 750)
        # top
        else:
            return random.randint(50, 750)

    def initiate_asteroid_y(self, start):
        """
        The object will pass  in random start number
        This number will decide which side of the screen the
        asteroid will spawn at.
        This function will return the y point.
        """
        # left side
        if start == 1:
            return random.randint(50, 550)
        # right side
        elif start == 2:
            return random.randint(50, 550)
        # bottom
        elif start == 3:
            return 0
        # top
        else:
            return 600


class Velocity:

    def __init__(self):
        # this will create a velocity attribute for the
        # object.
        self.dx = 0
        self.dy = 0


class Angle:

    def __init__(self):
        pass

    def initiate_angle(self, start):
        """
        The object will pass  in random start number
        This number will decide which side of the screen the
        astroid will spawn at.
        This function will return an appropriate angle
        that the astroid should start will with.
        """

        # left side
        if start == 1:
            return random.randint(-30, 30)
        # right side
        elif start == 2:
            return random.randint(150, 210)
        # bottom
        elif start == 3:
            return random.randint(60, 120)
        # top
        else:
            return random.randint(240, 300)

class FlyingObject:
    """
    This is a base class for all flying objects (lasers and ship and astroids)
    """

    def __init__(self):
        self.center = Point()  # initially 0 for x and y
        self.velocity = Velocity()  # initially 0 for dx and dy
        self.alive = True  # always start being alive
        self.height = 0  # figure height
        self.width = 0  # figure width
        self.texture = arcade.load_texture("ship.png")  # import the texture
        self.rotation = 0  # how much the figure is rotation
        self.alpha = 1000  # will not be transparent
        self.radius = 0
        # self.color = (0,200,50)    # this was used hit box detection

    def draw(self):
        # display the figure
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture,
                                      self.rotation, self.alpha)

        # used to check hit boxes
        # get rid of hash tags to check it out
        # arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, self.color)

    def check_wrap(self):
        """
        Every flying object will wrap.
        meaning that if goes off the screen it will
        move to another side of the screen
        """

        if self.center.y > SCREEN_HEIGHT:
            # move it to the bottom
            self.center.y = 0

        if self.center.y < 0:
            # move it the top
            self.center.y = SCREEN_HEIGHT

        if self.center.x > SCREEN_WIDTH:
            # move it to the left
            self.center.x = 0

        if self.center.x < 0:
            # move it to the right
            self.center.x = SCREEN_WIDTH

    def advance(self):
        # change the position by adding velocity
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy



class Asteroid(FlyingObject, ABC):
    """
    This class inherits from FLyingObject.
    This is the base class for all other asteroids.
    """

    def __init__(self):
        super().__init__()
        # this decides which side of the screen to spawn at.
        self.start = random.randint(1, 4)

        # uses the function from point to find the x and y
        self.center.x = self.center.initiate_asteroid_x(self.start)
        self.center.y = self.center.initiate_asteroid_y(self.start)

        # uses angle object and its methods
        # to find the direction it should go
        angle = Angle()
        self.direction = angle.initiate_angle(self.start)

        # uses the direction to get the correct speed
        self.velocity.dx = math.cos(math.radians(self.direction)) * BIG_ROCK_SPEED
        self.velocity.dy = math.sin(math.radians(self.direction)) * BIG_ROCK_SPEED

        self.radius = BIG_ROCK_RADIUS

        # starts at 0, but this will increase as the astroids advance
        self.rotation = 0

        self.dr = 1

        self.texture = arcade.load_texture("big.png")
        self.width = 50
        self.height = 50

    def spin(self):
        self.rotation += self.dr

    @abstractmethod
    def split(self):
        # this will be implemented in the child classes
        pass

    @abstractmethod
    def hit_ship(self):
        # this will be implemented in the child classes
        pass


class BigAsteroid(Asteroid):

    def __init__(self):
        super().__init__()
        # takes two hits to kill
        self.health = 2
        self.dr = BIG_ROCK_SPIN

    def split(self):
        # takes one away from health
        self.health -= 1

        # checks if the astorid is dead
        if self.health == 0:
            # when the laser hits the astroid, it will split and
            # produce two medium and 1 small astroid.
            # velocity is changed from the orginal astroid
            list = [MediumAsteroid(self.center.x, self.center.y, self.velocity.dx, self.velocity.dy + 2),
                    MediumAsteroid(self.center.x, self.center.y, self.velocity.dx, self.velocity.dy - 2),
                    SmallAsteroid(self.center.x, self.center.y, self.velocity.dx + 5, self.velocity.dy)]
            # kills it
            self.alive = False

        else:
            list = []

        # either returns the new astroids or an empty list
        return list

    def hit_ship(self):
        # does 8 damage to the ship
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
        # kill it
        self.alive = False

        # returns a list of two small asteroids
        # when it is hit by a laser
        return list

    def hit_ship(self):
        # does 5 damage to the ship
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
        # asteroid is done splitting
        list = []

        # kill it
        self.alive = False

        # returns an empty list
        return list

    def hit_ship(self):
        # does only damage of 2 to ship
        return 3

class Laser(FlyingObject):

    def __init__(self, angle, x, y, dx, dy):
        # angle: same angle as the ship's
        # x, y: same position as the ship's

        super().__init__()
        self.center.x = x
        self.center.y = y
        self.rotation = angle  # receives angle (to be used for speed)
        self.ship_dx = dx
        self.ship_dy = dy
        self.velocity.dx = math.cos(math.radians(self.rotation)) * LASER_SPEED  # + self.ship_dx
        self.velocity.dy = math.sin(math.radians(self.rotation)) * LASER_SPEED  # + self.ship_dx
        # I decided that for my game I did not want to add ship speed to
        # to the velocty of the lasers. I wanted the lasers to always
        # have a constant velocity. However, I have shown above that I
        # know how to implement it. you only need to get rid of the hastag
        # in the top two lines of code to make it work.
        self.texture = arcade.load_texture("laser.png")
        self.width = 25
        self.height = 6
        self.time_alive = 0.0  # used to keep track how long laser has been alive
        self.radius = LASER_RADIUS

    def check_alive(self):
        # this function is called every frame
        # it will add one.
        self.time_alive += 1

        # lasers will only last for the 60 frames.
        if self.time_alive > LASER_LIFE:
            self.alive = False

    def hit_ship(self):
        # does 7 damage to the ship
        return 7

class Ship(FlyingObject):

    def __init__(self):
        super().__init__()
        self.center.x = 400
        self.center.y = 300
        self.thrust = SHIP_THRUST_AMOUNT
        self.rotation = 0
        self.texture1 = arcade.load_texture("ship.png")
        self.width = 40
        self.height = 35
        self.radius = SHIP_RADIUS
        self._health = SHIP_HEALTH

    def ignite_thrusters(self):
        self.velocity.dx += math.cos(math.radians(self.rotation + 90)) * self.thrust
        self.velocity.dy += math.sin(math.radians(self.rotation + 90)) * self.thrust

    def check_state(self, frame):
        # makes the ship transparent when the ship
        # was recently hit. Helps the player to know
        # when their invincibility runs out
        if frame < 40:
            self.alpha = .3
        else:
            self.alpha = 1

        # if health at 0 then kill it
        if self.health == 0:
            self.alive = False

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        if health < 0:
            self._health = 0
        else:
            self._health = health


class Ship_Thrusters(Ship):

    def __init__(self):
        super().__init__()
        # Exact same ship, but with a different texture that has thrusters
        self.texture = arcade.load_texture("ship_Thruster.png")

class Game(arcade.Window):
    """
    This class handles all  the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    """

    """
    Extras Added:
    Ship has health and is displayed on screen
    Ship can get hurt by your own laser
    Ship shoots in the direction of the mouse
    Increase ship velocity with space bar in
    the direction ship is facing
    Ship has glowing thrusters when the space bar is pressed
    You move ship direction with mouse location
    Ship has invincibility for a time after it is hit
    Big asteroids take 2 hits to split
    The game can restart the game after the player won or died
    Astroids always spawn at the sides of the screens
    Improved hit box detection
    Added optional graphics to show the hit boxes 
    Added game intro screen
    Game ends when asteroids are all cleared or when player dies
    A different screen appears when player dies or wins.
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

        # create a ship
        self.ship = Ship()

        # create a ship that has thrusters
        self.ship_thrusters = Ship_Thrusters()

        # this will be used to determine when to draw the ship with thrusters
        self.draw_thrust = 0

        # list for all asteroids
        self.asteroids = []

        # start at with 5 asteroids incoming
        self.create_asteroids()

        # list for all lasers
        self.lasers = []

        # keeps track of frame count
        self.frame = 0

        # keeps track of delta time
        self.remember_time = 0

        # the state of the game
        # starts with the game intro
        self.current_state = GAME_INTRO

    def frame_count(self):
        """
        This function counts the frames
        """
        self.frame += 1

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # if self.draw_thrust has a value of 1 or more then draw the
        # ship with thrusters
        if self.draw_thrust > 0 and self.current_state != GAME_DEATH:
            self.ship_thrusters.draw()

        # draws ship
        # will stop drawing the ship when
        # the player loses the game
        if self.current_state != GAME_DEATH:
            self.ship.draw()

            # draw each laser in laser list
            for laser in self.lasers:
                laser.draw()

        # calls function to draw health on screen
        self.draw_health()

        # draw the intro to the game
        if self.current_state == GAME_INTRO:
            self.draw_warning()

        # move the asteroids when the game is the running state
        # or when the player dies.
        if self.current_state == GAME_RUN or self.current_state == GAME_DEATH:
            # goes through the asteroid list and draws them
            for asteroid in self.asteroids:
                asteroid.draw()

        # if current state of the game is death
        # then display the death screen
        if self.current_state == GAME_DEATH:
            self.draw_end()

        # if the player wins
        # then display the win screen
        if self.current_state == GAME_WIN:
            self.draw_win()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.remember_time += delta_time

        # count the frame
        self.frame_count()

        # calls the check wrap function
        # dont wrap when the game ends.
        # Acts as if the ship "left the screen"
        if self.current_state != GAME_WIN:
            self.check_wrap()

        # advance the lasers
        for laser in self.lasers:
            laser.advance()

        # advance the ship
        self.ship.advance()

        # now advance the ship with thrusters
        self.ship_thrusters.advance()

        if self.draw_thrust > 0:
            # if we should be drawing the thrusters
            # then add 1 each time the update function is called
            self.draw_thrust += 1
            if self.draw_thrust == 10:
                # now if it goes to 10 then set it to zero
                # so it doesn't draw again untill the space is pressed.
                self.draw_thrust = 0

        # switches from intro state to run state after 4 seconds
        if self.remember_time > 4 and self.current_state != GAME_WIN:
            self.current_state = GAME_RUN

        # only advance the asteroids and create asteroids
        # if the state is in run mode
        if self.current_state == GAME_RUN:

            # advance the asteroids
            for asteroid in self.asteroids:
                asteroid.advance()
                asteroid.spin()

        # check collisions
        self.check_collisions()

        # update the current state of the ship
        self.ship.check_state(self.frame)

        # finally we clean up any dead objects
        self.clean_up_objects()

    def create_asteroids(self):
        """
        Creates 5 asteroids and adds it to the list.
        To be called in the init at the start of the game
        """

        for i in range(1, 6):
            self.asteroids.append(BigAsteroid())


    def check_wrap(self):
        """
        goes through every object and calls their check wrap function
        """

        for asteroid in self.asteroids:
            asteroid.check_wrap()

        for laser in self.lasers:
            laser.check_wrap()

        self.ship.check_wrap()
        self.ship_thrusters.check_wrap()

    def check_collisions(self):
        """
        Checks to see if lasers have hit asteroids.
        then
        Checks to see if asteroids have hit the ship.
        then
        Checks to see if lasers have hit the ship.
        """

        for laser in self.lasers:
            for asteroid in self.asteroids:

                # Make sure they are both alive before checking for a collision
                if laser.alive and asteroid.alive:
                    too_close = laser.radius + asteroid.radius

                    if ((laser.center.x - asteroid.center.x) ** 2 + (
                            laser.center.y - asteroid.center.y) ** 2) ** .5 < too_close:
                        # its a hit!
                        laser.alive = False
                        list = asteroid.split()
                        self.asteroids += list

        for asteroid in self.asteroids:
            # Make sure they are both alive before checking for a collision
            if self.ship.alive and asteroid.alive:
                too_close = self.ship.radius + asteroid.radius
                if ((self.ship.center.x - asteroid.center.x) ** 2 + (
                        self.ship.center.y - asteroid.center.y) ** 2) ** .5 < too_close:
                    # its a hit!
                    if self.frame > 40:
                        hit_points = asteroid.hit_ship()
                        self.ship.health -= hit_points
                        self.frame = 0

        for laser in self.lasers:
            # Make sure they are both alive before checking for a collision
            if self.ship.alive and laser.alive and laser.time_alive > 30:
                too_close = self.ship.radius + laser.radius
                if ((self.ship.center.x - laser.center.x) ** 2 + (
                        self.ship.center.y - laser.center.y) ** 2) ** .5 < too_close:
                    # its a hit!
                    laser.alive = False

                    # if the ship has not been hit in the
                    # past 30 frames then it can be hit
                    # INVICIBILITY!
                    if self.frame > 30:
                        hit_points = laser.hit_ship()
                        self.ship.health -= hit_points
                        self.frame = 0

    def clean_up_objects(self):
        """
        Goes through every object within the list
        and checks if they are dead and need to be removed
        Also checks to see if the player had died or won.
        """

        for laser in self.lasers:
            # checks to see if the lasers have passed their
            # 60 frames limit
            laser.check_alive()
            if laser.alive == False:
                self.lasers.remove(laser)

        for asteroid in self.asteroids:
            if asteroid.alive == False:
                self.asteroids.remove(asteroid)

        if self.ship.alive == False:
            self.current_state = GAME_DEATH
        elif not self.asteroids:
            self.current_state = GAME_WIN

    def on_key_press(self, key, key_modifiers):
        # ignite thrusters when space is pressed
        if key == arcade.key.SPACE:
            self.ship.ignite_thrusters()
            self.ship_thrusters.ignite_thrusters()

            # set draw_thrust to 1 so that the draw function is
            # given the okay to draw. It will be turned off after 10 frames
            self.draw_thrust = 1

        # if player has died or won the game and the mouse is pressed then call the restart function
        if key == arcade.key.RETURN and (self.current_state == GAME_DEATH or self.current_state == GAME_WIN):
            self.restart()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # tracks mouse motion
        # set the ship and laser angle in degrees
        self.ship.rotation = self.get_angle_degrees(x, y)
        self.ship_thrusters.rotation = self.get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!

        # grabs the current angle between the ship and mouse
        angle = self.get_angle_degrees(x, y) + 90

        # creates a laser object using information from the ship
        laser = Laser(angle, self.ship.center.x, self.ship.center.y, self.ship.velocity.dx, self.ship.velocity.dy)

        # adds it to the list
        self.lasers.append(laser)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            pass

        if arcade.key.RIGHT in self.held_keys:
            pass

        if arcade.key.UP in self.held_keys:
            pass

        if arcade.key.DOWN in self.held_keys:
            pass

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass

    def get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        """
        # get the angle in radians
        angle_radians = math.atan2(y - self.ship.center.y, x - self.ship.center.x)

        # convert to degrees
        # converted to degrees because the ship and laser class needs degrees
        angle_degrees = math.degrees(angle_radians) - 90

        return angle_degrees

    def restart(self):
        """
        This will restart the game when enter is pressed.
        """

        # clear asteroids
        self.asteroids.clear()

        # create a new ship
        self.ship = Ship()

        # create a new ship that has thrusters
        self.ship_thrusters = Ship_Thrusters()

        # reset to 0
        self.draw_thrust = 0

        # start at with 5 asteroids incoming
        self.create_asteroids()

        # clear list
        self.lasers.clear()

        # restart frame count
        self.frame = 0

        # restart time
        self.remember_time = 0

        # goes back to the game intro
        self.current_state = GAME_INTRO

    def draw_health(self):
        arcade.draw_rectangle_filled(400, 590, self.ship.health * 10, 10, arcade.color.FIREBRICK)
        arcade.draw_rectangle_outline(400, 590, 150, 10, arcade.color.WHITE)
        arcade.draw_text("Hull Integrity:", start_x=215, start_y=SCREEN_HEIGHT - 15, font_size=12,
                         color=arcade.color.WHITE)

    def draw_warning(self):
        """
        draws the warning screen
        """
        output2 = "WARNING!"
        output3 = "...Asteroids Incoming..."

        arcade.draw_text(output2, 240, 450, arcade.color.FIREBRICK, 54)
        arcade.draw_text(output3, 160, 350, arcade.color.FIREBRICK, 40)

    def draw_end(self):
        """
        draws the death screen
        """
        output4 = "ERROR!"
        output5 = "SYSTEM FAILURE"
        output6 = "You Died"
        output10 = "Try Again?\nPress Enter"

        arcade.draw_text(output4, 320, 400, arcade.color.FIREBRICK, 40)
        arcade.draw_text(output5, 310, 300, arcade.color.FIREBRICK, 20)
        arcade.draw_text(output6, 350, 200, arcade.color.FIREBRICK, 20)
        arcade.draw_text(output10, 340, 100, arcade.color.WHITE, 20)

    def draw_win(self):
        """
        draws the winning screen
        """
        output7 = "ASTEROIDS CLEARED!"
        output8 = "PROCEED TO YOUR MISSION"
        output9 = "You Win"
        output10 = "Try Again?\nPress Enter"

        arcade.draw_text(output7, 180, 400, arcade.color.FIREBRICK, 40)
        arcade.draw_text(output8, 175, 300, arcade.color.FIREBRICK, 30)
        arcade.draw_text(output9, 355, 200, arcade.color.FIREBRICK, 20)
        arcade.draw_text(output10, 340, 100, arcade.color.WHITE, 20)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()