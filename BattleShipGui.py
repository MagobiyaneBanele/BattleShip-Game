# Banele Magobhiyane and Bonani Tshwane
# programme of the battleship gui game
# Extra features indicated by initials

import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from GameClient import *
from PyQt5.QtMultimedia import *

# Start dialog (BM)
class StartDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Battleship game")
        self.setWindowIcon(QIcon("ship.png"))
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Set the fixed size of the dialog to (700, 500) pixels
        self.setFixedSize(700, 500)
        self.pic_label = QLabel(self)
        self.pixmap = QPixmap("battleship.gif") 
        self.scaled_pixmap = self.pixmap.scaled(700,500)
        self.pic_label.setPixmap(self.scaled_pixmap)

        layout = QVBoxLayout(self)
        self.message_label = QLabel("Welcome to the Battleship!")
        self.message_label.setStyleSheet("padding-left: 180px;")
        self.message_label.setFont(QFont("Bernard MT Condensed",20,10))
        layout.addWidget(self.message_label)
        layout.addWidget(self.pic_label)

        start_button = QPushButton("Start")
        start_button.setFont(QFont("Bernard MT Condensed",12,10))
        start_button.clicked.connect(self.accept)
        layout.addWidget(start_button)
        
        
class LoopThread(QThread):
    bsg_signal = pyqtSignal(str) # creates a signal that gets emitted when a message is received from the server
    
    def __init__(self):
        QThread.__init__(self)
        
    def run(self):
        while True:
            # everything in this run method is essentially everything that was in our play_loop method
            msg = bsg.receive_message() # receive messages from the server
            if len(msg): self.bsg_signal.emit(msg) # will execute if the message has a length and it will emit the message as a signal
            else: break # if message has no length, the connection between the server and the client will be ended 
       
class BattleShipGame(QWidget, GameClient):
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        GameClient.__init__(self)
        self.setGeometry(200, 100, 700, 500)          # x, y, width, height based on screen
        self.setWindowTitle('Ten Eleven Games')   # creating the window title
        # Disable maximizing window
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint)        
        self.setPalette(QPalette(QColor('light blue')))
        self.role = None
        self.gen_score = 0   
        self.cap_score = 0   
        
        # game icon (BM)
        self.setWindowIcon(QIcon("ship.png"))
        
        #combo box for background color (BT & BM)
        self.combo_color = QComboBox(self)
        self.combo_color.setFont(QFont("Bernard MT Condensed",10,10))
        self.combo_color.addItem("Light Blue")
        self.combo_color.addItem("Beige")
        self.combo_color.addItem("Grey") 
        self.combo_color.addItem("Dark Khaki")
        self.combo_color.addItem("Dark Olive Green")
        self.combo_color.addItem("Orange Red")        
 
        self.loop_thread = LoopThread()  # creates a loop thread
        self.loop_thread.bsg_signal.connect(self.handle_message)  # once a signal is emitted, connection of the loopthread to the handle message slot is needed
        
        #changing color
        self.change_b = QPushButton("Change")
        self.change_b.setFont(QFont("Bernard MT Condensed",10,10))
        self.change_b.clicked.connect(self.change)
        
        # intructions button (BT)
        self.instructions_b = QPushButton("Game Instructions")
        self.instructions_b.setFont(QFont("Bernard MT Condensed",10,10))
        self.instructions_b.clicked.connect(self.instructions)
        
        # heading label
        self.heading  = QLabel("BATTLESHIP")
        # set font of the heading label
        self.heading.setFont(QFont("Bernard MT Condensed",20,10))
        # set the heading label to center
        self.heading.setAlignment(Qt.AlignCenter)
        
        # server label
        self.server_label = QLabel("Server:")
        self.server_label.setFont(QFont("Bernard MT Condensed",10,10))
        self.edit = QLineEdit() 
        # allow a button to clear all the text at once (BM)
        self.edit.setClearButtonEnabled(True)          
        self.edit.setPlaceholderText('enter server name')
        # connect button
        self.connect_b = QPushButton("Connect")
        self.connect_b.setFont(QFont("Bernard MT Condensed",10,10))
        # exit button
        self.exit_b = QPushButton("Exit")
        self.exit_b.setFont(QFont("Bernard MT Condensed",10,10))
        self.exit_b.setFixedSize(300,40)
        
        # captain and general score labels
        self.captain_score_label = QLabel("Captain:")
        self.general_score_label = QLabel("General:")
        self.captain_score_label.setFont(QFont("Bernard MT Condensed",10,10))
        self.general_score_label.setFont(QFont("Bernard MT Condensed",10,10))
        self.cap_score_label = QLabel("")
        self.gen_score_label = QLabel("")
        
        # connecting buttons to their methods so that when clicked they can do their respective actions
        self.connect_b.clicked.connect(self.server)
        self.exit_b.clicked.connect(self.exit)
        
        # messages from the server 
        self.server_messages_edit = QTextEdit("")
        self.server_messages_edit.setFixedWidth(300)
        self.server_messages_edit.setFixedHeight(300)
        # disable editing the textedit 
        self.server_messages_edit.setReadOnly(True)  

        # the button to place the character
        self.character = QPushButton() 
        self.character.setIcon(QIcon("b.gif"))
        # set the size of the icon to 45 heigth and 45 widgth
        self.character.setIconSize(QSize(45, 45))
        # set the size of the button to 45 height and 45 widgth
        self.character.setFixedSize(45, 45)
        self.character.setEnabled(True)
        
        # creating buttons from 1 to 36
        self.button1 = QPushButton()
        self.button2 = QPushButton()
        self.button3 = QPushButton()
        self.button4 = QPushButton()
        self.button5 = QPushButton()
        self.button6 = QPushButton()
        self.button7 = QPushButton()
        self.button8 = QPushButton()
        self.button9 = QPushButton()
        self.button10 = QPushButton()
        self.button11 = QPushButton()
        self.button12 = QPushButton()
        self.button13 = QPushButton()
        self.button14 = QPushButton()
        self.button15 = QPushButton()
        self.button16 = QPushButton()
        self.button17 = QPushButton()
        self.button18 = QPushButton()
        self.button19 = QPushButton()
        self.button20 = QPushButton()
        self.button21 = QPushButton()
        self.button22 = QPushButton()
        self.button23 = QPushButton()
        self.button24 = QPushButton()
        self.button25 = QPushButton()
        self.button26 = QPushButton()
        self.button27 = QPushButton()
        self.button28 = QPushButton()
        self.button29 = QPushButton()
        self.button30 = QPushButton()
        self.button31 = QPushButton()
        self.button32 = QPushButton()
        self.button33 = QPushButton()
        self.button34 = QPushButton()        
        self.button35 = QPushButton()        
        self.button36 = QPushButton()
        
        # setting a fixed size for buttons
        self.button1.setFixedSize(50,50)
        self.button2.setFixedSize(50,50)
        self.button3.setFixedSize(50,50)
        self.button4.setFixedSize(50,50)
        self.button5.setFixedSize(50,50)
        self.button6.setFixedSize(50,50)
        self.button7.setFixedSize(50,50)
        self.button8.setFixedSize(50,50)
        self.button9.setFixedSize(50,50)
        self.button10.setFixedSize(50,50)
        self.button11.setFixedSize(50,50)
        self.button12.setFixedSize(50,50)
        self.button13.setFixedSize(50,50)
        self.button14.setFixedSize(50,50)
        self.button15.setFixedSize(50,50)
        self.button16.setFixedSize(50,50)
        self.button17.setFixedSize(50,50)
        self.button18.setFixedSize(50,50)
        self.button19.setFixedSize(50,50)
        self.button20.setFixedSize(50,50)
        self.button21.setFixedSize(50,50)
        self.button22.setFixedSize(50,50)
        self.button23.setFixedSize(50,50)
        self.button24.setFixedSize(50,50)
        self.button25.setFixedSize(50,50)
        self.button26.setFixedSize(50,50)
        self.button27.setFixedSize(50,50)
        self.button28.setFixedSize(50,50)
        self.button29.setFixedSize(50,50)
        self.button30.setFixedSize(50,50)
        self.button31.setFixedSize(50,50)
        self.button32.setFixedSize(50,50)        
        self.button33.setFixedSize(50,50)
        self.button34.setFixedSize(50,50)
        self.button35.setFixedSize(50,50)
        self.button36.setFixedSize(50,50)
        
        # button_list 
        self.button_list = [[self.button1, self.button2, self.button3, self.button4, self.button5, self.button6],
                       [self.button7, self.button8, self.button9, self.button10, self.button11, self.button12],
                       [self.button13, self.button14, self.button15, self.button16, self.button17, self.button18],
                       [self.button19, self.button20, self.button21, self.button22, self.button23, self.button24],
                       [self.button25, self.button26, self.button27, self.button28, self.button29, self.button30],
                       [self.button31, self.button32, self.button33, self.button34, self.button35, self.button36]]
        
        # board buttons, creating the group box and layout for the buttons and also connecting them to their functions
        self.button1.clicked.connect(self.button_1)
        self.button2.clicked.connect(self.button_2)
        self.button3.clicked.connect(self.button_3)
        self.button4.clicked.connect(self.button_4)
        self.button5.clicked.connect(self.button_5) 
        self.button6.clicked.connect(self.button_6)
        self.button7.clicked.connect(self.button_7)
        self.button8.clicked.connect(self.button_8)
        self.button9.clicked.connect(self.button_9)
        self.button10.clicked.connect(self.button_10)
        self.button11.clicked.connect(self.button_11)
        self.button12.clicked.connect(self.button_12)
        self.button13.clicked.connect(self.button_13)
        self.button14.clicked.connect(self.button_14)
        self.button15.clicked.connect(self.button_15)
        self.button16.clicked.connect(self.button_16)
        self.button17.clicked.connect(self.button_17)
        self.button18.clicked.connect(self.button_18)
        self.button19.clicked.connect(self.button_19)
        self.button20.clicked.connect(self.button_20)
        self.button21.clicked.connect(self.button_21)
        self.button22.clicked.connect(self.button_22)
        self.button23.clicked.connect(self.button_23)
        self.button24.clicked.connect(self.button_24)
        self.button25.clicked.connect(self.button_25)
        self.button26.clicked.connect(self.button_26)
        self.button27.clicked.connect(self.button_27)
        self.button28.clicked.connect(self.button_28)
        self.button29.clicked.connect(self.button_29)
        self.button30.clicked.connect(self.button_30)
        self.button31.clicked.connect(self.button_31)
        self.button32.clicked.connect(self.button_32)
        self.button33.clicked.connect(self.button_33)
        self.button34.clicked.connect(self.button_34)
        self.button35.clicked.connect(self.button_35)
        self.button36.clicked.connect(self.button_36)
        
        #layout of buttons created inside a group box
        self.main_game_groupbox = QGroupBox("THE GAME")
        self.main_game_groupbox.setFont(QFont("Bernard MT Condensed",10,10))
        self.board = QGridLayout()
        self.board.addWidget(self.button1,0,0)
        self.board.addWidget(self.button2,0,1)
        self.board.addWidget(self.button3,0,2)
        self.board.addWidget(self.button4,0,3)
        self.board.addWidget(self.button5,0,4)
        self.board.addWidget(self.button6,0,5)
        self.board.addWidget(self.button7,1,0)
        self.board.addWidget(self.button8,1,1)
        self.board.addWidget(self.button9,1,2)
        self.board.addWidget(self.button10,1,3)
        self.board.addWidget(self.button11,1,4)
        self.board.addWidget(self.button12,1,5)
        self.board.addWidget(self.button13,2,0)
        self.board.addWidget(self.button14,2,1)
        self.board.addWidget(self.button15,2,2)
        self.board.addWidget(self.button16,2,3)
        self.board.addWidget(self.button17,2,4)
        self.board.addWidget(self.button18,2,5)
        self.board.addWidget(self.button19,3,0)
        self.board.addWidget(self.button20,3,1)
        self.board.addWidget(self.button21,3,2)
        self.board.addWidget(self.button22,3,3)
        self.board.addWidget(self.button23,3,4)
        self.board.addWidget(self.button24,3,5)
        self.board.addWidget(self.button25,4,0)
        self.board.addWidget(self.button26,4,1)
        self.board.addWidget(self.button27,4,2)
        self.board.addWidget(self.button28,4,3)
        self.board.addWidget(self.button29,4,4)
        self.board.addWidget(self.button30,4,5)
        self.board.addWidget(self.button31,5,0)
        self.board.addWidget(self.button32,5,1)
        self.board.addWidget(self.button33,5,2)
        self.board.addWidget(self.button34,5,3)
        self.board.addWidget(self.button35,5,4)
        self.board.addWidget(self.button36,5,5)
        self.board_widget = QWidget()
        self.board_widget.setLayout(self.board)
        self.main_game_groupbox.setLayout(self.board)
       
        # input info grid
        self.server_heading_grid = QGridLayout()
        self.server_heading_grid.addWidget(self.heading, 0, 1, 1, 1)
        self.server_heading_grid.addWidget(self.server_label, 1, 0)
        self.server_heading_grid.addWidget(self.edit, 1, 1)
        self.server_heading_grid.addWidget(self.connect_b, 1, 2)
        self.server_heading_grid_widget = QWidget()
        self.server_heading_grid_widget.setLayout(self.server_heading_grid)       

        # grid layout for player information inside a groupbox
        self.message_groupbox = QGroupBox("BATTLESHIP SERVER MESSAGES")
        self.message_groupbox.setFont(QFont("Bernard MT Condensed",10,10))
        self.character_grid = QGridLayout()
        self.character_grid.addWidget(self.server_messages_edit, 3, 0)
        self.character_grid_widget = QWidget()
        self.character_grid_widget.setLayout(self.character_grid)
        self.message_groupbox.setLayout(self.character_grid)
        self.message_groupbox.setFixedSize(350,350)
        
        # creating a group box and layout for a character label
        self.character_label_groupbox = QGroupBox("ROLE")
        self.character_label_groupbox.setFont(QFont("Bernard MT Condensed",10,10))
        self.role_grid = QGridLayout()
        self.role_grid.addWidget(self.character,1,0)
        self.role_grid_widget = QWidget()
        self.role_grid_widget.setLayout(self.role_grid)
        self.character_label_groupbox.setLayout(self.role_grid)
        self.character_label_groupbox.setFixedSize(80,80)
        
        # creating a group box and layout for character scores
        self.character_score_groupbox = QGroupBox("SCORES")
        self.character_score_groupbox.setFont(QFont("Bernard MT Condensed",10,10))
        self.score_grid = QGridLayout()
        self.score_grid.addWidget(self.captain_score_label,1,0)
        self.score_grid.addWidget(self.general_score_label,2,0)
        self.score_grid.addWidget(self.cap_score_label,1,1)
        self.score_grid.addWidget(self.gen_score_label,2,1)        
        self.score_grid_widget = QWidget()
        self.score_grid_widget.setLayout(self.score_grid)
        self.character_score_groupbox.setLayout(self.score_grid)
        self.character_score_groupbox.setFixedSize(80,80)
        
        # vbox for role and scores
        self.role_score = QVBoxLayout()
        self.role_score.addWidget(self.character_label_groupbox)
        self.role_score.addWidget(self.character_score_groupbox)
        self.role_score_widget = QWidget()
        self.role_score_widget.setLayout(self.role_score)
        
        # the exit button layout 
        self.exit_button = QGridLayout()
        self.exit_button.addWidget(self.combo_color,0,0)
        self.exit_button.addWidget(self.change_b,0,1)
        self.exit_button.addWidget(self.exit_b,1,0)
        self.exit_button_widget = QWidget()
        self.exit_button_widget.setLayout(self.exit_button) 
        
        # merging the left hand side widgets
        self.right_vbox = QVBoxLayout()
        self.right_vbox.addWidget(self.server_heading_grid_widget)
        self.right_vbox.addWidget(self.message_groupbox)
        self.right_vbox.addWidget(self.instructions_b)
        self.right_vbox_widget  = QWidget()
        self.right_vbox_widget.setLayout(self.right_vbox)        
        
        # merging the right hand side widgets
        self.game_vbox = QVBoxLayout()
        self.game_vbox.addWidget(self.main_game_groupbox)
        self.game_vbox.addWidget(self.exit_button_widget)
        self.game_vbox_widget  = QWidget()
        self.game_vbox_widget.setLayout(self.game_vbox)
        
        # meging all both the left and right hand side V boxes
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.right_vbox_widget)
        self.main_layout.addWidget(self.role_score_widget)
        self.main_layout.addWidget(self.game_vbox_widget)
        self.main_layout_widget = QWidget()
        self.setLayout(self.main_layout)
    
    # method for connect to server button    
    def server(self):
        self.server_name = self.edit.displayText() 
        try:        
            bsg.connect_to_server(self.server_name) # to connect user to the server
            self.server_messages_edit.append("Connected to server!")
            self.loop_thread.start()   # starts the loopthread once the client has been connected
        except:
            self.server_messages_edit.append("Error connecting to server!")
        
    # method for handling messages from the server
    def handle_message(self, msg): 
        self.message = msg.split(',')  
        
        # NEW GAME
        if self.message[0] == "new game":
            if self.message[1] == "C":
                self.character.setIcon(QIcon("c.gif"))
            else:
                self.character.setIcon(QIcon("g.gif"))
                
            self.server_messages_edit.append(msg)
            for i, button_row in enumerate(self.button_list):
                for j, button_column in enumerate(button_row):
                    self.button_list[i][j].setIcon(QIcon("b.gif"))
                    self.button_list[i][j].setIconSize(QSize(50, 50))
                    
        # YOUR MOVE   
        if self.message[0] == "your move":
            self.server_messages_edit.append(msg)
            for i, button_row in enumerate(self.button_list):
                for j, button_column in enumerate(button_row):
                    self.button_list[i][j].setEnabled(True) # Enables all buttons
                    
        # OPPONENTS MOVE   
        if self.message[0] == "opponents move":
            self.server_messages_edit.append(msg)
            for i, button_row in enumerate(self.button_list):
                for j, button_column in enumerate(button_row):
                    self.button_list[i][j].setDisabled(True) # Disables all buttons
   
        # VALID MOVE    
        if self.message[0] == "valid move":
            self.server_messages_edit.append(msg)
            
            self.role = self.message[1]
            self.x = int(self.message[2])
            self.y = int(self.message[3])            
           
            captain_score = int(self.message[4])
            general_score = int(self.message[5])
            
            self.cap_score_label.setText(str(captain_score))
            self.gen_score_label.setText(str(general_score))
            
            # updating character label
            if self.cap_score == captain_score and self.role == "C":
                self.button_list[self.x][self.y].setIcon(QIcon("lc.gif"))
                
            elif self.cap_score != captain_score and self.role =="C":
                self.button_list[self.x][self.y].setIcon(QIcon("c.gif"))
                
            if self.gen_score == general_score and self.role == "G":
                self.button_list[self.x][self.y].setIcon(QIcon("lg.gif"))
                
            elif self.gen_score != general_score and self.role =="G":
                self.button_list[self.x][self.y].setIcon(QIcon("g.gif"))
                
            self.gen_score = general_score
            self.cap_score = captain_score
            
        # INVALID MOVE   
        if self.message[0] == "invalid move":
            self.server_messages_edit.append(msg)
            
        # GAME OVER
        #if self.message[0] == "game over":     
            #self.server_messages_edit.append("Game over")
            #self.server_messages_edit.append("Winner:",self.role)
    
        #PLAY AGAIN
        if self.message[0] == "play again": 
            # end dialog box (BT)
            self.endDialog = QDialog()
            self.endDialog.setWindowTitle("Battleship game")
            self.endDialog.setWindowIcon(QIcon("ship.png"))
            self.endDialog.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            # Set the fixed size of the dialog to (700, 500) pixels
            self.endDialog.setFixedSize(700, 500)
            game_over_label = QLabel("Game Over")
            game_over_label.setAlignment(Qt.AlignCenter)
            
            if self.role == "G":
                self.r = "General"
            else:
                self.r = "Captain"
                
            self.endDialog.setStyleSheet("background-image: url('tp.gif');")
    
            layout3 = QVBoxLayout(self.endDialog)
            message_label3 = QLabel("")
            message_label3.setText("Game Over\n"+"Winner: "+self.r+"\n"+"Do you want to play again?")
            message_label3.setFont(QFont("Bernard MT Condensed",20,10))
            message_label3.setStyleSheet("padding-left: 180px;")
            #layout3.addWidget(game_over_label)
            #layout3.addWidget(message_label2)
            layout3.addWidget(message_label3)
            
            layout4 = QHBoxLayout()
            y_button = QPushButton("Yes")
            n_button = QPushButton("No")
            y_button.setFont(QFont("Bernard MT Condensed",12,10))
            n_button.setFont(QFont("Bernard MT Condensed",12,10))
            y_button.clicked.connect(self.yes_button)
            n_button.clicked.connect(self.no_button)
            layout4.addWidget(y_button)
            layout4.addWidget(n_button)
            layout3.addLayout(layout4)
            self.endDialog.exec_() 
            
        # EXIT
        if self.message[0] == "exit":
            self.server_messages_edit.append("Your opponent exited the game.")
    
    def yes_button(self):
        self.send_message("y")
        self.endDialog.close()
        
    def no_button(self):
        self.send_message("n")
        self.close()
        self.endDialog.close()
        
    # method for game board buttons    
    def button_1(self):
        self.send_message("0,0")
        
    def button_2(self):
        self.send_message("0,1")
        
    def button_3(self):
        self.send_message("0,2")
        
    def button_4(self):
        self.send_message("0,3")
        
    def button_5(self):
        self.send_message("0,4")
        
    def button_6(self):
        self.send_message("0,5")
        
    def button_7(self):
        self.send_message("1,0")
        
    def button_8(self):
        self.send_message("1,1")
        
    def button_9(self):
        self.send_message("1,2")
        
    def button_10(self):
        self.send_message("1,3")
        
    def button_11(self):
        self.send_message("1,4")
        
    def button_12(self):
        self.send_message("1,5")
        
    def button_13(self):
        self.send_message("2,0")
        
    def button_14(self):
        self.send_message("2,1")
        
    def button_15(self):
        self.send_message("2,2")
        
    def button_16(self):
        self.send_message("2,3")
        
    def button_17(self):
        self.send_message("2,4")
        
    def button_18(self):
        self.send_message("2,5")
        
    def button_19(self):
        self.send_message("3,0")
        
    def button_20(self):
        self.send_message("3,1")
        
    def button_21(self):
        self.send_message("3,2")
        
    def button_22(self):
        self.send_message("3,3")
        
    def button_23(self):
        self.send_message("3,4")
        
    def button_24(self):
        self.send_message("3,5")
        
    def button_25(self):
        self.send_message("4,0")
        
    def button_26(self):
        self.send_message("4,1")
        
    def button_27(self):
        self.send_message("4,2")
        
    def button_28(self):
        self.send_message("4,3")
        
    def button_29(self):
        self.send_message("4,4")
        
    def button_30(self):
        self.send_message("4,5")
        
    def button_31(self):
        self.send_message("5,0")
        
    def button_32(self):
        self.send_message("5,1")
        
    def button_33(self):
        self.send_message("5,2")
        
    def button_34(self):
        self.send_message("5,3")
        
    def button_35(self):
        self.send_message("5,4")
    
    def button_36(self):
        self.send_message("5,5")

    # method for displaying instructions to players through a dialog box (BT)  
    def instructions(self):
        self.messageBox = QMessageBox()
        self.messageBox.setWindowTitle("Game Instructions")
        self.messageBox.setText("~ Connect to the server and choose a background color of your choice for the game. \n~ You will recieve a message indicating that a new game is about to start and your respective role, then wait for your move. \n~ Click on the board to indicate your move. \n~ If it's a hit your score will change (+1) otherwise it will remain the same. \n~ If you have click a position that has been played, you will enter your move again. \n~ When all ships are finished, the winner of the game will be announced. \n~ Once the game is over, you will be asked if you want to play again or not. \n~ You can exit the game anytime by clicking the exit button.")
        self.messageBox.exec_()
        
    # method for changing background colour    
    def change(self):
        colour = self.combo_color.currentText()
        self.setPalette(QPalette(QColor(colour)))
        self.setAutoFillBackground(True)
        
    # method for exit button  
    def exit(self):
        self.close()
        
        
    def play_loop(self):
        while True:
            msg = self.receive_message()
            if len(msg): 
                self.handle_message(msg)
            else: 
                break
        
app = QApplication(sys.argv)
start_dialog = StartDialog()
if start_dialog.exec_() == QDialog.Accepted:
    bsg = BattleShipGame()                 
    bsg.show()
    sys.exit(app.exec())   