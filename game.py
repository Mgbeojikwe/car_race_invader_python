import tkinter as Tk
from enemy import *
import keyboard

SCORE=0
GAME_SPEED= 7

class Game:

    start_x=GAME_WIDTH//2
    start_y=GAME_HEIGHT-PIXEL_SIZE-2

    def __init__ (self):

        self.__enemy= Enemy()

        #creting two 2D-list sequences and 1D-list sequnce
        self.__all_enemy_cars=[]                                                          # a 2D-list whose elemnts are of list of derived type "Carpart"
        self.__all_enemy_cars_colors=""

        (self.__all_enemy_cars, self.__all_enemy_cars_colors) = self.__enemy.create_cars()  #creating the first set of cars when Game object is created
        
        self.__player_car=[ CarPart(Game.start_x, Game.start_y), CarPart(Game.start_x+ 2*PIXEL_SIZE , Game.start_y),
                           CarPart(Game.start_x+PIXEL_SIZE,  Game.start_y - PIXEL_SIZE),
                           CarPart(Game.start_x, Game.start_y-(2*PIXEL_SIZE)), CarPart(Game.start_x+PIXEL_SIZE ,Game.start_y-(2*PIXEL_SIZE)), CarPart(Game.start_x+(2*PIXEL_SIZE), Game.start_y-(2*PIXEL_SIZE)),
                           CarPart(Game.start_x+PIXEL_SIZE, Game.start_y-(3*PIXEL_SIZE))     #   <== tip of player's car
                           ]
           
        self.__player_bullets=[]

        self.__player_car_color="#00FF00"
        self.__player_bullets_color = self.__player_car_color

        self.__direction="left"

        self.__movement_step = PIXEL_SIZE//10

        self.__num_of_enemy_cars_destroyed=0


        #boss instance attributes
        self.__boss=[]

        self.__boss_color=""
        self.__boss_is_created=False
        self.__boss_lifetime=0
        self.__boss_bullets=[]
        
        self.__game_over= False
        
        #sort the parts of "player's car", "boss car" and "all enemy's car" based on the value of their x_axis. This is important in placing boundary condition for the side of the canvas.
        #thus no need to utilize the "min()"  and "max()" functions 
        self.__player_car.sort()
        self.__boss.sort()

        for index, enemy_car in enumerate(self.__all_enemy_cars):
                enemy_car.sort()

                self.__all_enemy_cars[index] = enemy_car      #updating the "self.__all_enemy_car" container


    def sort_enemy_cars(self):
            """
                  This method is import because it heps sort the parts of each enemy car. The parts are
                  sorted based on their x-axis value; The "sort()" method utilizes the __lt__ method 
                  defined in the "CarPart" class
           """
            for index, enemy_car  in enumerate(self.__all_enemy_cars):
                   
                   enemy_car.sort()

                   self.__all_enemy_cars[index] = enemy_car   #updating the value of the container
    

    def sort_boss_car(self):
      """
            This method sorts the part of boss' car based on their x-axis value
      """
      self.__boss.sort()

    def generate_enemy_cars(self):
          """
            This method generates new enemy car's cars. It emptys the "self.__enemy.enemy_cars" sequence
            prioir to creating new once. Enemy cars are created if the boss is not created
          """

          if self.__boss_is_created == False:
                
                (self.__all_enemy_cars, self.__all_enemy_cars_colors)= self.__enemy.create_cars()
          
          self.sort_enemy_cars()  # sort enemy's car


    def create_boss(self):
       """
              A boss is created if 12 enemies car have been destroyed. 

            N:B: There will be scenario where is twelfth (12th) to be destroyed appears along side
            2 or more cars. In such scenario, we need to delete all the other cars from the canvas

            N:B: A boss is created if 12 enemy's cars have been destroyed and "self.__boss_is_created == False", "self.__boss_is_created"
                 value also need to be set so as to prevent the creation of another new boss. creation of another new boss overides
                 the previous
            
              """
          
          
       if self.__num_of_enemy_cars_destroyed == 12 and self.__boss_is_created ==  False:
          
                (self.__boss, self.__boss_color)=self.__enemy.create_boss()
                 
                self.sort_boss_car()                                      #sorting the boss is import               
                self.__boss_is_created = True                           #to ease "placing boundary condition"
                self.__boss_lifetime =5                                  #assign lifetime to boss

                #delete leftover enemy cars from canvas, in scenarios where we still have leftover cars
                # on the canvas after the 12th car has been shot

                if (len(self.__all_enemy_cars) >0 ):
                       
                       self.__all_enemy_cars.clear()
                       

    @staticmethod
    def place_boundary_for_side_direction(temporary, car ):

        """
            This method ensures that no car leaves the canvas either by the left or right-handside
            It is suitable for the player's car, enemy car and the boss
        """
          
        car_part_far_left  = car[0]
        car_part_far_right = car[-1]
        
        if (car_part_far_left.x <0  or car_part_far_right.x >= GAME_WIDTH):
              car= temporary
        else:
               pass 
        
        return car


    def move_player_bullets(self):
        """
            This method moves the player_bullets shot by the player's car. The player_bullets are moved upward
        """
        canvas_top=3

        self.__player_bullets=list(map(lambda bullet:  CarPart(bullet.x, bullet.y - self.__movement_step),self.__player_bullets))
        self.__player_bullets = [ bullet for bullet in self.__player_bullets  if bullet.y > canvas_top ]

    
    def move_enemies_cars(self):
        """
            This method moves the enemy's cars; each can move either left, right or downward.
                An enemy car is destroyed from canvas if it covers a vertical distance of "GAME_HEIGHT - PIXEL_SIZE"
        """
        
        #check if there are still enemy's car on canvas. if False, then create new ones
              
        if (len(self.__all_enemy_cars) ==0 ):
                  self.generate_enemy_cars()               
            
      
        for index, enemy_car in enumerate(self.__all_enemy_cars):

                 direction = random.choice(["left","right","forward"])

                 temporary_position = enemy_car
                 
                 side_step=random.choice([self.__movement_step, self.__movement_step//2, self.__movement_step//3])
                 
                 match (direction):
                        
                        case "left" :
                              
                              enemy_car = list(map(lambda part:CarPart(part.x -side_step, part.y)   , enemy_car))
                              enemy_car=self.place_boundary_for_side_direction(temporary_position,enemy_car)

                        case "right":
                              
                              #enemy_car = list(map(lambda  part: CarPart(part.x +self.__movement_step, part.y)  , enemy_car))
                              enemy_car = list(map(lambda  part: CarPart(part.x + side_step, part.y)  , enemy_car))
                              
                              enemy_car=self.place_boundary_for_side_direction(temporary_position, enemy_car)

                        case "forward":
                              enemy_car = list(map(lambda part: CarPart(part.x, part.y+self.__movement_step) , enemy_car))
                              
                  #check if enemy_car "i" reached game bottom
                 tip=max(enemy_car)
                 
                 if (tip.y > (GAME_HEIGHT-PIXEL_SIZE)):
                        self.__all_enemy_cars.pop(index)

                 else:
                        self.__all_enemy_cars[index] =enemy_car
        

    
    def move_player_car(self):

        """ This method moves the player car left or right, and also enables the palyer shoot player_bullets.
            boundary condition is placed to ensure the player's cardoesn't leave the canvas 

        """
        
        initial_position = self.__player_car

        match (self.__direction):
               
               case "left":
                      
                      self.__player_car=list(map(lambda  part: CarPart( part.x -PIXEL_SIZE, part.y) , self.__player_car))
                      self.__player_car=self.place_boundary_for_side_direction(initial_position, self.__player_car)
        
               case "right":
                             self.__player_car= list(map(lambda part: CarPart(part.x + PIXEL_SIZE, part.y)  , self.__player_car))       
                             self.__player_car= self.place_boundary_for_side_direction(initial_position, self.__player_car)
               
               case "s":

                     bullet = self.__player_car[-1] 
                     self.__player_bullets.append(bullet)
          
               
         
        self.__direction="down"   # thus imaginary default value is given to player so that car doesn't move continuously


    def check_if_player_bullet_hit_enemy_car(self):
          
          """
            This method checkes if an enemy car has been shot. It start by looping through
            the available player_bullets, then check if the bullet has touch a part of an enemy car. If True, the car is deleted

            N:B: The third inner loop is import because we want to compare the position of bullet "j"
                  each part of enemy_car "i"

            """
          global SCORE 

          for index1, bullet in enumerate(self.__player_bullets):
                 
                 for index2, enemy_car in enumerate(self.__all_enemy_cars):
                          
                        for part in enemy_car:
                               
                               if ( part.x <= bullet.x <= (part.x+PIXEL_SIZE)  and ( part.y <= bullet.y<=(part.y +PIXEL_SIZE)) and len(self.__player_bullets)>=1):
                                      
                                      self.__player_bullets.pop(index1)
                                      self.__all_enemy_cars.pop(index2)
                                      SCORE += 5
                                      label.config(text=f"Score = {SCORE}")
                                      self.__num_of_enemy_cars_destroyed +=1
                                      
                                      break
                              
                               else: 
                                    continue                            #check if bullet "i" touch other parts of same car "j"
          
         
    def boss_shoots_bullet(self):
           
           """
              This method handles the shooting property of Boss. To ensure that 
              Boss doesn;t shot continuously, as a result of the continual running of the while loop, 
              this method is called conditionally in the "self.play()" method.

              N:B: Since Boss is created conditionally, and this method is always called (though also conditionally), to prevent
              code creashing, the statements in this method are ran only when boss is created
           
           """

           if self.__boss_is_created == True:
              selected_gun_index=7#random.choice([2,7,11])
            
              bullet =self.__boss[selected_gun_index]
              self.__boss_bullets.append(bullet)
           
           else:
                  pass


    def move_boss(self):
          
          """
            This method moves the boss. Boss can only move left or right, and also posesses shooting ability
            The boss has three positions it randomly shoots from, and it shoots one bullet at a time; thus utilizes only one position
            at a time
                   """

          self.create_boss()   # N:B: This is created under a given condtion
          
          if self.__boss_is_created == True:
                
                
                initial_position = self.__boss

                direction= random.choice(list(range(150)))   # random selection for a large sized sequence significantly lowers 
                                                               #the speed at which the enemy car moves 

                match (direction) :
                       
                       
                        case 1:      
                              self.__boss = list(map(lambda part: CarPart(part.x - PIXEL_SIZE, part.y) , self.__boss))
                              self.__boss =self.place_boundary_for_side_direction(initial_position, self.__boss)
                       
                        case 7:      
                             self.__boss = list(map(lambda  part:  CarPart(part.x + PIXEL_SIZE, part.y)   , self.__boss))
                             self.__boss=self.place_boundary_for_side_direction(initial_position, self.__boss)
                       
          else:
                 pass
          
    
    def move_boss_bullets(self):
            """
            
                  This method handles the movement of the boss bullet, with bullets moving vertically downwards. It also checks if the bullets have 
                  covered a distance of "GAME_HEIGHT -10", If True, the bullet is erased from the sequence
                  and thus deleted from the canvas
            
            """

            self.__boss_bullets = list(map(lambda  bullet: CarPart(bullet.x, bullet.y+self.__movement_step) , self.__boss_bullets))

            #check if bullet reaches bottom of Canvas 
            for index, bullet in enumerate(self.__boss_bullets):
                   
                   if (bullet.y >= (GAME_WIDTH- PIXEL_SIZE)):
                          self.__boss_bullets.pop(index)
                   
                   else:
                          pass 
    
      
    def check_if_boss_bullets_hit_player_car(self):
          """
            This method monitors each of the boss bullets whether it hits the player's car, and if True that the player was shot, then player score is reduced and the bullet deleted.
            A bullet is also deleted from canvas if it coveres a vertical distance of "GAME_HEIGHT  - PIXEL_SIZE"

          """
          global SCORE

          for index, bullet in enumerate(self.__boss_bullets):
                 
                 for part in self.__player_car:
                        
                        if ( bullet.x <= part.x <= (bullet.x + PIXEL_SIZE)  and ( bullet.y <= part.y <=  (bullet.y +PIXEL_SIZE))):

                                    SCORE -= 15                          #reduce player's score
                                    label.config(text=f"Score = {SCORE} \n boss life time ={self.__boss_lifetime}")                                                                                 
                                    self.__boss_bullets.pop(index)       #delete the bullet
                                    break                                #since a part of player's car has been shot, obviously player has been shot
                                                                         # thus no need to check if bullet "i" touched other part
                        else:
                               continue                                  #If bullet "i" does not touch part "k", check if it touches other parts     
          
      
    def check_if_player_bullet_hits_boss_centre(self):
          
          """
          This method monitors each player's bullet to know if the boss is shot at the center.
          if True that boss is shot at centre, then the boss lifetime, which is nine, is reduced by one. The boss is destroyed if its lifetime
          becomes zero; If such condition is reached, boss variables are returned to start state, and new enemy's cars are generated

          
          """
          global SCORE
          
          if self.__boss_is_created == True:
                 boss_center = self.__boss[7]
          
          #loop through the total bullets shot by player, and check if any hit the centre of boss
                 for index, bullet in enumerate(self.__player_bullets):
                 
                        if ( boss_center.x <= bullet.x <=(boss_center.x + PIXEL_SIZE)  and ( boss_center.y <= bullet.y <= (boss_center.y + PIXEL_SIZE)) ) :
                        
                               self.__player_bullets.pop(index)                      #delete the bullet
                               SCORE +=5  
                               label.config(text=f"Score = {SCORE} \n boss life time ={self.__boss_lifetime}")                                         #increase the player's score 
                               self.__boss_lifetime -=1                              # reduce the boss lifetime

                        else:
                            continue                                         #i.e move to next bullet "i+1" and check if it hits boss Centre       
    
    def check_if_boss_has_been_killed(self):

            if self.__boss_lifetime == 0  and self.__boss_is_created == True:

                   # clear the boss container to allow for a new boss                                   
                   self.__boss_bullets.clear()
                   self.__boss_is_created = False
                   self.__num_of_enemy_cars_destroyed=0    #returning this value to "0" to enable "self.generate_enemy_cars()" and not "self.create_boss()"
                   self.__boss.clear()                     #deleting boss from canvas 

                   label.config(text=f"Score = {SCORE}")                 
    
    def print_player_car_to_canvas(self):
           
           for part in self.__player_car:
                  x=part.x
                  y=part.y
                  canvas.create_rectangle(x,y, x+PIXEL_SIZE, y+PIXEL_SIZE, fill=self.__player_car_color, tag="player")
           
          
    def print_player_bullets_to_canvas(self):
           
          for bullet in self.__player_bullets:
                  x = bullet.x
                  y = bullet.y
                  
                  canvas.create_rectangle(x,y, x+PIXEL_SIZE, y+PIXEL_SIZE, fill = self.__player_bullets_color, tag="player_bullet")
    
    def print_enemy_cars_to_canvas(self):

            for enemy_car in self.__all_enemy_cars:
                    for part in enemy_car:
                           x = part.x
                           y = part.y

                           canvas.create_rectangle(x,y,x+PIXEL_SIZE, y+PIXEL_SIZE, fill = self.__all_enemy_cars_colors, tag="enemy_car")

    def print_boss_to_canvas(self):
            
            for part in self.__boss:
                  x = part.x
                  y= part.y
                  canvas.create_rectangle(x,y,x+PIXEL_SIZE, y+PIXEL_SIZE, fill = self.__boss_color, tag="boss")
    

    def print_boss_bullets_to_canvas(self):
           
           for bullet in self.__boss_bullets:
                 x = bullet.x
                 y = bullet.y
                 canvas.create_rectangle(x,y, x + PIXEL_SIZE, y+PIXEL_SIZE, fill= self.__boss_color, tag="boss_bullets")


    def check_if_any_enemy_car_bypass_player_car(self):
            
            """
                  This method checks if any of the available enemy's cars bypass the player's car
                  If True, then game ends
            
            """
            player_tip_index=-1
            player_car_tip = self.__player_car[player_tip_index]

            for enemy_car in self.__all_enemy_cars:

                  enemy_car_tip = max(enemy_car)

                  if (enemy_car_tip.y > player_car_tip.y):
                                                 
                        self.__game_over=True         
                        break                                   #game ends no need checking if other enemy's car bypass player

                  else:
                         continue                  
                  
    
    def check_if_player_has_been_killed_by_boss(self):
           global SCORE
           
           if SCORE < 0 :
                 self.__game_over = True


    def game_over(self):

           if self.__game_over == True:  
                         
                  canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("consolas",70), text="GAME  OVER", fill="red")
                  canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()-4*PIXEL_SIZE, font=("consolas",PIXEL_SIZE), text="Press q to restart game", fill="WHITE")
       

    def change_direction(self,input_direction):
          self.__direction = input_direction              
    

    def restart_key(self):
           
           if self.__game_over == True  and self.__direction == "q":
                  self.__game_over=False
                  self.reset_game()
    
    def reset_game(self):
           global SCORE

           self.__boss_bullets.clear()
           self.__all_enemy_cars.clear()
           self.__num_of_enemy_cars_destroyed = 0  #This needs to be cleared due to scenarios when boss isn't formed yet, but
                                                   # one of the enemy's cars by-pass the palyer's car. Thus supporting the "self.check_if_boss_is_killed()"
           self.__player_bullets.clear()

           self.__boss_is_created=False            #since we are restarting the game 
           self.__boss_lifetime = 5
           self.__boss.clear()
           SCORE=0


    def bind(self):
                 
       
           
              window.bind("<Left>", lambda x: self.change_direction("left"))    

              window.bind("<Right>", lambda x: self.change_direction("right"))

              window.bind("<s>", lambda x: self.change_direction("s"))

              window.bind("<q>", lambda key: self.change_direction("q"))
                          
         
         
          

    
    def play(self):
           
           canvas.delete("all")    #clear canvas prior to printing next state of game object on canvas 

           if (self.__game_over == False):
                     self.move_player_car()
                     self.move_enemies_cars()
                     self.move_boss()

                     self.move_player_bullets()
                     self.move_boss_bullets()

                     self.check_if_player_bullet_hit_enemy_car()
                     self.check_if_boss_bullets_hit_player_car()
                     self.check_if_player_bullet_hits_boss_centre()
                     self.check_if_any_enemy_car_bypass_player_car()

                     self.check_if_boss_has_been_killed()


                     self.print_player_car_to_canvas()
                     self.print_enemy_cars_to_canvas()
                     self.print_boss_to_canvas()

                     self.print_player_bullets_to_canvas()
                     self.print_boss_bullets_to_canvas()

                     self.check_if_player_has_been_killed_by_boss()
              #       self.game_over()

                     self.bind()

               #placing a condition to control the rate at which boss shots bullets

                     boss_bullet_control_points = list(range(150))
                     gun_trigger =random.choice(boss_bullet_control_points)
           
                     if gun_trigger ==3:
                            self.boss_shoots_bullet()
           
           else:
                     self.print_player_car_to_canvas()
                     self.print_enemy_cars_to_canvas()
                     self.print_boss_to_canvas()

                     self.print_player_bullets_to_canvas()
                     self.print_boss_bullets_to_canvas()
                     self.game_over()
                     self.restart_key()       
                     self.bind()

           canvas.after(GAME_SPEED,self.play)


window=Tk.Tk()
window.title("Shooter car race")
window.resizable(False,False)
label=Tk.Label(window, text=f"score={SCORE}", font=("consolas",40))
label.pack()

canvas = Tk.Canvas(window,bg=BACK_GROUND_COLOR, height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()
window.update()

