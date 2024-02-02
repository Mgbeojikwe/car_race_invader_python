import random 
from car_part import *

PIXEL_SIZE=40
GAME_HEIGHT=20*PIXEL_SIZE
GAME_WIDTH=20*PIXEL_SIZE
BACK_GROUND_COLOR="#000000"

class Enemy:

        def __init__ (self):
                
                self.__enemy_cars=[]  # A 2D-list array, where each 1D-list array denotes
                
                self.__enemy_cars_color="#FF0000"


        def create_cars(self):
                """
                This method creates the five cars and returns a randomly selected number of the cars
                """
                
                start_x=PIXEL_SIZE
                start_y=10 

                max_num_of_cars = 5
                cars=[]

                for i in range(max_num_of_cars):
                        
                      
                       car_i =[ CarPart(start_x,start_y), CarPart(start_x+PIXEL_SIZE,start_y), CarPart(start_x+(2*PIXEL_SIZE),start_y), CarPart(start_x+PIXEL_SIZE ,start_y+PIXEL_SIZE)]
                       
                       cars.append(car_i)
                       
                       start_x += 2*PIXEL_SIZE    # increase "start_x" by "2*PIXEL_SIZE"  hence separating the five cars

                

                # select some random cars and assign them to "self.__enemy_cars"
               
                num_of_cars = random.randint(2, max_num_of_cars)   #randomly choose  number of cars
                
                range_of_cars=list(range(max_num_of_cars))   #i.e [0,1,2,3,4,5,...(max_num_of_cars - 1)]

                list_indexes_of_chosen_cars = random.choices(range_of_cars, k=num_of_cars)

                #use the randomly generated index to make selection
                for index  in list_indexes_of_chosen_cars:
                        
                      self.__enemy_cars.append(cars[index])

                return (self.__enemy_cars,self.__enemy_cars_color)
        

        def create_boss(self):
                
                """This method creates the boss

                """
                start_x = GAME_WIDTH//2
                start_y = 5 
                boss_color= "#FF0000"
                 
                boss=[CarPart(start_x,start_y), CarPart(start_x,start_y+PIXEL_SIZE), CarPart(start_x,start_y+(2*PIXEL_SIZE)),
                      CarPart(start_x+PIXEL_SIZE,start_y), CarPart(start_x+PIXEL_SIZE,start_y+PIXEL_SIZE),
                      CarPart(start_x+(2*PIXEL_SIZE), start_y), CarPart(start_x+(2*PIXEL_SIZE),start_y+PIXEL_SIZE), CarPart(start_x+(2*PIXEL_SIZE),start_y+(2*PIXEL_SIZE)),
                      CarPart(start_x+(3*PIXEL_SIZE),start_y),  CarPart(start_x+(3*PIXEL_SIZE),start_y+ PIXEL_SIZE),
                      CarPart(start_x+(4*PIXEL_SIZE),start_y), CarPart(start_x+(4*PIXEL_SIZE),start_y+PIXEL_SIZE ), CarPart(start_x+(4*PIXEL_SIZE) ,start_y+(2*PIXEL_SIZE) )
                      ]
                        #structure of boss
                """
                        |||||
                        |||||
                        | | |
                        
                """
                        
                return (boss,boss_color )
        
        

        
        def clear_enemy_cars(self):
                
                self.__enemy_cars.clear()    #needed to be called prior to creating new cars,
                                              #since "Enemy" obj is still alive and hence its instance are alive even though cars are destroyed