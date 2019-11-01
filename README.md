# MAIC2019
Third edition of the Mify Artificial Intelligence Contest #MIFY #AAAIBenin



## The Game

The game chosen for this edition is Yote. It is played by 2 players on a board generally either 6 squares out of 5 or 5
squares out of 5. Each player has 12 pieces of different colours. The object of the game is to capture all the opposing 
pieces. More information on the rules of the game is available [here](http://www.lecomptoirdesjeux.com/yote.htm).

##Setup

The game was written in **Python** and works with versions greater than or equal to **3.6+**.

### Get Python and dependencies


You can download the **3.8** version of Python [here](https://www.python.org/downloads/).
(Don't forget to add python to the path if you are on Windows)

After the installation you need to install **PyQt5** the main dependence of the game.
For that just run the following command (Note that you may replace *pip* by *pip3* if you have different versions of python).


```bash
pip install pyqt5
```

### Run the code

Firstly, just clone this repository or download the zip to get everything you need to work and just run by following the instructions.


Usage: 

      python game_cli.py -ai0 ia_0.py -ai1 ia_1.py -s 0.5
      
      
      -ai0 
          path to the ai that will play as player 0
      -ai1 
           path to the ai that will play as player 1
      -s 
           time(in second) to show the board(or a move)


**Example**
        
        git clone https://github.com/Machine-Intelligence-For-You/MAIC2019.git
        cd MAIC2019/
        python game_cli.py -ai0 ia0.py -ai1 ia1.py -s 0.5
        

		   
		   
To use timeout you have to add just above function play of AI the decorator @timeout(seconds=time), 
time is the given timeout time (Eg: @timeout(seconds=0.1)).