# project-10

**Remember that this project cannot be submitted late.**

In this project, you are going to write an Ant class to simulate Langton’s Ant. You can see the brief explanation [here](https://en.wikipedia.org/wiki/Langton%27s_ant).

In this simulation, a virtual "ant" moves about a two-dimensional square matrix, whose spaces can be designated white or black, according to the rules below:

1. If the ant is on a white space, it will turn right 90 degrees relative to the directions it is facing, move forward one step, and change the space it left to black.
2. If the ant is on a black space, it will turn left 90 degrees relative to the directions it is facing, move forward one step, and change the space it left to white.
3. When the ant hits the edge of the board and is going to go out of the bounds, wrap the board around so the ant will appear on the other side.

The matrix is initially composed of all white spaces. The user will specify the size of the square matrix. The user will also specify the number of steps that the ant will move and the starting location and direction of the ant. After the simulation, the final board with the ant position will be displayed to the console. In this display, the ant is represented by number "8", a black space is represented by the number sign ("#"), and a white space is represented by an underscore ("\_").

**Simulation flow:**

Your program’s main method will collect the user input for the information needed to initialize the simulation.  The information to be collected will include:

1. The number of rows/columns for the square board matrix.  
2. The ant's starting location.  This will be collected via user input to ask users to enter an integer number for row and an integer number for the column as the starting position of the ant.  For example, if the board is 9X9, and you choose "4,4" as ant’s starting location, then the ant will start from the center of the board.
3. The ant's starting direction, which can be 0 for up, 1 for right, 2 for down, 3 for left.  
 
Main will use the information collected to initialize an Ant object that will be used to run the simulation.

Once the Ant object is initialized, main will collect user input for the number of steps that the simulation will run.  When testing, don’t choose a very large number when you do the test.  

After all the information described above is collected from the user, a method called run_simulation will start the simulation of the Ant movement.  For each step, it will...

* Increment the step counter;
* Use Ant object to store the Ant object’s current position and direction on the board;
* Move the Ant based on the movement rule;
* Change the color of the space on the board the Ant just left.

Once the simulation is finished, display the board by printing it to the console using the print_board method. Here, for the space that is dominated by the Ant, you don't need to display the color.  If the step number is 0, print the initial board.

During the development of your program, you could test your code by choosing the step number as 0, 1, 2, 3, etc. to see the results.

The file must be named: **LangtonAnt.py**

Case won't matter for all the messages that your methods return.

Feel free to add whatever other classes, methods, or data members you want. All data members must be private. All methods must have no more than 20-25 lines of code - don't try to get around this by making really long or complicated lines of code. 

Here's a very simple example of how your program could be used by the autograder or a TA:

```
Welcome to Langton’s ant simulation! 
First, please enter a number no larger than 100 for the size of the square board:
5
Choose the ant’s starting location, please enter a number as the starting row number (where 0 is the first row from the top):
0
Please enter a number as the starting column number (where 0 is the first column from the left):
0
Please choose the ant’s starting orientation, 0 for up, 1 for right, 2 for down, 3 for left:
2
Please enter the number of steps for the simulation:
3

#___#
_____
_____
_____
8___#
```
