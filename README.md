This game is built with the aid of the tkinter library inorder to improve user interaction.
To run this source code on linux OS, type:
        $ sudo python3 main.py

This source code is built with the aid of three derived classes viz: "CarPart", "Enemy" and "Game" present in the car_part.py, enemy.py and game.py modules respectively. The three classes are linked by composition and are  discussed below:


1) ..............CarPart.............
        This class was designed to hold the (x,y) axis of each part of the cars built in the game. Two special methods __lt__ and __gt__ are overloaed; both methods are called in scenarios that require knowing the lesser or greater of two "Carpart" objects in terms of their x-axis and y-axis values respectively.
         __lt__ method is also called when sort() instrinsic method and min() fucntion are applied to a sequence of "CarPart" objects while __gt__ is called when max() is applied to a sequence of "CarPart" objects.


2) ............................Enemy.......................

This class has three  methods and they are discussed below:

2.1 create_cars()
        This method creates a minimum and maximum of 1 and 5 enemy cars. it acheives its objectives using the steps:

        step 1 => with the help of a for-loop, create five cars appending each to the list sequence "cars"
        step 2 => randomly select one of more cars, maximum of five, and append them to "self.__enemy_cars". The cars, are randomly added to "self.__enemy_cars" to enable the possibility of having largely separated enemy's cars
        step 3: return the results of step2 along with the cars' color.

2.2. create_boss
        This method create the boss car. the boss car appears after 12 enemy's cars have been shot.

2.3 clear_enemy_cars
        These method ensures that "self.__enemy_cars" is empty prior to appending new cars. This action is necessary since the "Enemy" object is still alive though the cars have been shot by the player; to enable new set of cars to be generated, the "self.__enemy_cars" list sequence must be cleared.


3).................Game....................................

This derived class has 28 methods, and some are discussed below:

3.1)    generate_enemy_cars()
        This method utilize the "Enemy" object, "self.__enemy" in creating the enemy's cars. Enemy cars are created only when boss is destroyed or not yet creted

3.2     create_boss()

        This method also utilizes the "Enemy" object, "self.__enemy" in creating the boss. The boss is created only when 12 enemy car's has been shoot and when "self.__boss_is_created" is False. This method also ensures no enemy car remain on the canvas once twelve enemy have already been shot.

3.3     place_boundary_for_side_direction()

        This static method ensures that none of the cars(enemy, player and boss) leaves the canvas. It accepts two arguements viz: the initial of the car prior to movement and the current position of the car after movement. It acheives its objective through the following steps:

        step 1 => the car's part is sorted in terms of their x-axis value
        step 2 => the first and last "CarPart" objects denote the parts closest the left-side and right-side of the canvas respectively.
        step 3 => If the leftmost part of the has an x-axiz value less than zero or the rightmost part of the car has an x-axis value greater or equals GAME_WIDTH, resign the initial position of the car to its current state. i.e return the car back to its initial psotion

3.4  move_enemies_cars()

This method moves enemy's car downward i.e towards the player's car. Each cars direction is independent on others. "self.move_enemies_cars()"  acheives its objective through the following step:
        step 1 => loop through all the enemies cars
        step 2 => randomly select the car "i" direction
        step 3 => have a record of the car "i"  position prior to movement
        step 4 => randomly select the stepwise movement and assign it to "side_step
        step 4 => if direction is "left", substract "side_step" from the x-axis value of each part of the car, if "right" , add "side_step" to the x-axis value of the car, and if "forward", add "self.__movement_step" to the y-axis value of each car part.


3.5 move_player_car()
        This method controls the movement of the player. The player can only move left or right, and it has a default direction of "down" to prevent continual movement of the player in one direction; the direction of the player is controlled by "self.__direction". The method acheives the said objectives via the following steps:
        step 1 => get the initial position of the player prior to movement

        step 2 => if self.__direction is "left", then substract "PIXEL_SIZE" from the x-axis component of all parts of the player car , but keeping the y-components constant.

        step 3 => if "self.__direction" is "right", then add "PIXEL_SIZE" to the x-axis of all parts of the player's car, but keeping the y-component constant.

        step 4 => place boundary condition on the resulting so as to prevent the car from leaving the canvas.

        step 5 => If "self.__direction" is "s", assign the current state of the last part of the player car as "bullet", and append "bullet" self.__player_bullets which is a list sequence of bullets.


3.6   check_if_player_bullet_hit_enemy_car()

        These method checks if any of the enemy's cars have been shot. It acheives this objective as described by the steps:

        step 1 => loop through all the available player bullets in "self.__player_bullets
        step 2 => as a nested loop of step 1, loop through all the available enemy's cars
        step 3 => as an additional nexted loop, loop through all the parts in enemy car "i".
        step 4 => for a given part "j" obtained in step 3 for an enemy_car "i", check if its x-axis lies within a range covered by bullet "k" from step 1, and also check if the y-axis of same car part "j" lies within vertical area coverd by the bullet.

        step 5 => If step 4 returns "True", then enemy_car "i" has been shot, else check same bullet "k" on the next  part "j+1".
        step 6 => If step 5 returns "True" , delete the bullet from "self.__player_bullet" and also delete the shot enemy_car "i" from "self.__enemy_cars".

        step 7 => Repeat entire step 1 to 6, for the next bullet on the enemy_cars.
        N:B: If a bullet shots an enemy_car "i", the bullet is prevented from shooting another car by deleting it from "self.__player_bullets", an the shot car is also deleted from the canvas.

