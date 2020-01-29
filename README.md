# American Sign Language Virtual Teacher
Project developed at The University of Vermont

Running this program requires a Leap Motion device to capture infrared images of one hand at a time.  This program analyzes the data to detect bones, and will map the coordinates of each joint in a pygame window with lines drawn between the points to create a virtual hand.

# Teaching the User
The code will teach the user the first ten (0-9) ASL digits by displaying images of each sign in a random order, while comparing coordinates of the hand to datasets corresponding to the proper digit.  With each correct signing, the program will become more difficult.  The user can also elect to learn through basic mathematical equations, which will also grow more difficult as the user signs digits faster and at a higher success rate.
