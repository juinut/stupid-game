import arcade.key
from random import *


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
        self.endd = ""
        self.time = 0



        self.stupid = Stupid(self, 65, 100)
        self.coin = Coin(self,width/2,height/2)

        self.obstacleLeft = Obstacle(self,65,height,randint(2,10))
        self.obstacleRight = Obstacle(self,width-65,height,randint(2,10))
        self.bonus_list = []


    def update(self, delta):
        self.stupid.update(delta)
        self.coin.update(delta)
        self.obstacleRight.update(delta)
        self.obstacleLeft.update(delta)

        self.time+=delta
        if(self.time>randint(2,5)):
            self.bonus_list.append(Bonus(self,randint(100,self.width-100),self.height,randint(5,15)))
            self.time = 0

        for index,b in enumerate(self.bonus_list):
            b.update(delta)
            if self.stupid.hit(b,35):
                self.score+=5
                del self.bonus_list[index]
                
            if(b.is_out_of_screen()):
                del self.bonus_list[index]

        print(self.bonus_list)
        if self.stupid.hit(self.coin, 25):
            self.coin.random_location()
            self.score+=1
        if self.stupid.hit(self.obstacleLeft, 35) or self.stupid.hit(self.obstacleRight, 35):
            self.endd = "GAME OVER"



    def on_key_press(self, key, key_modifiers):
        if self.stupid.x ==65 or self.stupid.x == self.width-65:
            if key == arcade.key.SPACE:
                self.stupid.switch_direction()

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)

class Stupid(World):
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = -20


    def update(self, delta):
        if self.x >= self.world.width-65:
            pass
        elif self.x > 65 and self.x <= self.world.width/2 and self.vx > 0:
            self.x+=self.vx
            self.y+=2
        elif self.x > self.world.width/2 and self.x < self.world.width-65 and self.vx > 0:
            self.x+=self.vx
            self.y-=2
        elif self.x > self.world.width/2 and self.x< self.world.width-65 and self.vx <0:
            self.x+=self.vx
            self.y+=2
        elif self.x > 65 and self.x <= self.world.width/2 and self.vx < 0:
            self.x+=self.vx
            self.y-=2


    def switch_direction(self):
        self.vx *= -1
        self.x += self.vx

class Coin:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def update(self, delta):
        if self.y < 0:
            self.y = self.world.height
            self.x = randint(65, self.world.width-65)
        self.y-=5

    def random_location(self):
        self.x = randint(65, self.world.width-65)
        self.y = self.world.height

class Obstacle:
    def __init__(self, world , x, y, vy):
        self.world = world
        self.x = x
        self.y = y
        self.vy = vy

    def update(self, delta):
        if self.y <0:
            self.y = self.world.height
            self.vy = randint(2,10)
        self.y-=self.vy

class Bonus:
    def __init__(self, world, x, y, vy):
        self.world = world
        self.x = x
        self.y = y
        self.vy = vy

    def __repr__(self):
        return "Bonus[{},{}]->{}".format(self.x,self.y,self.vy)


    def is_out_of_screen(self):
        if self.y < 0:
            return True
        return False

    def movement(self):
        self.y-=self.vy

    def update(self, delta):
        self.movement()
