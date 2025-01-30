# BONANI TSHWANE 
# BANELE MAGOBIYANE
# This code is about BattleShip text-based game played by general and captain.

from GameClient import *

class BattleShipTextClient(GameClient):

    def __init__(self):
        GameClient.__init__(self)
        self.board = [x[:] for x in [[' ']*6]*6] # creates 6x6 game board
        self.role = None # role C (for captain) or G (for general)
        self.gen_score = 0          # setting the initial scores for the general
        self.cap_score = 0          # and captain
        
    def clear_board(self):
        self.board = [x[:] for x in [[' ']*6]*6]       
    
    def input_server(self):
        return input('enter server:')
     
    def input_move(self):
        return input('enter move(0-5,0-5):')
     
    def input_play_again(self):
        return input('play again(y/n):')

    def display_board(self):     # a method that displays the 
        for i in self.board:
            print("_|_".join(i))
            
    def handle_message(self,msg):   # a method that handles all the messages from the server
        
        self.message = msg.split(',')   # taking and separating the message from the server
        
        if self.message[0] == "new game":  # extracting "new game" from the message sent by the server
            
            print("Welcome to Battleship!\nNew game"+", "+ self.message[1])
            self.display_board()      # displays an empty board
        
        if self.message[0] == "your move":    # extracting "your move" from the message sent by the server
            print("It's your turn to play, choose your position on the board.")
            move = self.input_move()    
            self.send_message(move)     # sends the message back to the server after a player inputs a move
            
        if self.message[0] == "valid move":    # extracting "valid move" from the message sent by the server
            player = self.message[1]       
            row = int(self.message[2])
            col = int(self.message[3])
            captain_score = int(self.message[4])
            general_score = int(self.message[5])
            print(player,"played the move",row,",",col)
            print("Captain's score is ",captain_score)
            print("General's score is ",general_score)
          
            #Updating the board with the users move
            if self.gen_score == general_score and player == "G":
                self.board[row][col] = player.lower()
            elif self.gen_score != general_score and player =="G":
                self.board[row][col] = player
                
            if self.cap_score == captain_score and player == "C":
                self.board[row][col] = player.lower()
            elif self.cap_score != captain_score and player =="C":
                self.board[row][col] = player                        # Updating the board with the users move

            self.gen_score = general_score
            self.cap_score = captain_score 
            self.display_board()           #displaying the current board

        elif self.message[0] == "invalid move":        # extracting "invalid move" from the message sent by the server
            print("Invalid move")
            self.display_board()                #displaying the current board
        
        elif self.message[0] == "opponents move":    # extracting "opponents move" from the message sent by the server
            print("It's your opponents turn to play.")
        
        elif self.message[0] == "game over":      # extracting "game over" from the message sent by the server
            self.role = self.message[1]
            print("Game over")
            print("Winner:",self.role)
            
        elif self.message[0] == "play again":     # extracting "play again" from the message sent by the server
            y_n = self.input_play_again()
            self.send_message(y_n)                # sends message to the server 
           
        elif self.message[0] == "exit":          # extracting "exit" from the message sent by the server
            self.__del__()                       # closes the game after the other player has exited the game
            print("Your opponent exited the game")
            
    def play_loop(self):
        while True:
            msg = self.receive_message()
            if len(msg): 
                self.handle_message(msg)
            else: 
                break
            
def main():
    
    bstc = BattleShipTextClient()
    while True:
        try:
            bstc.connect_to_server(bstc.input_server())
            break            
        except:
            print('Error connecting to server!')       
    bstc.play_loop()
    input('Press enter to exit.')
        
main()