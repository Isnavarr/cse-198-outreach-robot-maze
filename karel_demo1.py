import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Set room size
vSize = 11 
hSize = 11

# Initialize position and object locations, then display.
loc = np.array([[0, 0]])


def haveIBeenHereBefore(nextStep):
    ''' 
    This function can be used to determine if the robot has previously been 
    to the location specified in nextStep.
    loc is the set of previous locations traversed by the robot
    nextStep is the new location for which the test is to be performed
    out is a boolean value, True if nextStep has been previosuly
    visited
    '''
    return nextStep.tolist() in loc.tolist()

def displayRoom(loc,obj,vSize,hSize):
    # Create empty room
    room = np.zeros((vSize,hSize))
    
    # Represent objects with gray
    for ob in obj:
        room[ob[0],ob[1]] = 127
    
    # Represent past locations with light gray
    for lo in loc[:-1]:
        room[lo[0], lo[1]] = 191
    
    # Represent current location with white
    room[loc[-1][0], loc[-1][1]] = 255
    

    plt.imshow(room, cmap='gray')
    plt.title('Press \'q\' to continue. Ctrl+C (or Cmd+C) to stop simulation.')
    plt.show()

# def detectObject(loc, obj, dir):
#     # Check for object in specified direction
#     if dir == 'N':
#         dirLoc = loc[-1] + np.array([-1, 0])
#     elif dir == 'E':
#         dirLoc = loc[-1] + np.array([0, 1])
#     elif dir == 'S':
#         dirLoc = loc[-1] + np.array([1, 0])
#     else:
#         dirLoc = loc[-1] + np.array([0, -1])
#     objectDetected = dirLoc.tolist() in obj.tolist()
#     return objectDetected
def detectObject(dir):
    # Check for object in specified direction
    if dir == 'N':
        dirLoc = loc[-1] + np.array([-1, 0])
    elif dir == 'E':
        dirLoc = loc[-1] + np.array([0, 1])
    elif dir == 'S':
        dirLoc = loc[-1] + np.array([1, 0])
    else:
        dirLoc = loc[-1] + np.array([0, -1])
    objectDetected = dirLoc.tolist() in obj.tolist()
    return objectDetected

def load_map(filename):
    global obj
    global loc
    global vSize
    global hSize
    df = pd.read_csv(filename,header=None)
    hSize = len(df.index) + 1
    vSize = len(df.columns)
    for i in df.index:
        for j in df.columns:
            if(df.iloc[i,j] == 1):
                obj.append([i,j])
                #obj = np.insert(arr=obj, obj=0,values=np.array([i,j]),axis=0)
    obj = np.asarray(obj)
    for i in df.columns:
        if(df.iloc[0,i] == 0):
            loc = np.array([[0, i]])
            break
    #print(obj)
    displayRoom(loc, obj, vSize, hSize)
    return filename,obj


def forward():
    return loc[-1] + np.array([1, 0])

def left():
    return loc[-1] + np.array([0, -1])

def right():
    return loc[-1] + np.array([0, 1])

def backward():
    return loc[-1] + np.array([-1, 0])

    # Add additional obstacles to this array per instructions:
    # Add obstacles
#obj = np.array([[0, 3], [2, 7], [3, 8], [5, 5], [2, 0], [1, 2], [7, 1]]) 

#displayRoom(loc, obj, vSize, hSize)

if __name__ == '__main__':
    IN = False
    obj = []
    count = 0 
    while(True):
        if(IN == False):
            data = input("Please enter the message:\n")
            load_map(data)
            IN = True


        # Make the robot move a certain direction
        # nextStep = loc[-1] + np.array([1, 0])

        '''
        MAZE SOLVE DEMONSTRATION

        Use 'map1.csv' or 'map2.csv' to demonstrate
        
        Uncomment Code for Use
        '''
        if not detectObject('S') and not haveIBeenHereBefore(forward()):
            nextStep = forward()
        elif not detectObject('E') and not haveIBeenHereBefore(right()):
            nextStep = right()
        elif not detectObject('W') and not haveIBeenHereBefore(left()):
            nextStep = left()
        else:
            nextStep = backward()
        '''
        DEMO ENDS HERE
        '''

        '''
        MOVEMENT DEMONSTRATION
        
        Use 'empty.csv' to demonstrate

        Uncomment Code for Use
        '''
        # if count == 0:
        #     nextStep = forward()
        # elif count == 1:
        #     nextStep = left()
        # elif count == 2:
        #     nextStep = right()
        # else: 
        #     nextStep = backward()
        
        # count += 1
        '''
        DEMO ENDS HERE
        '''
        
        # Update location if no object is in the way and within bounds
        if (nextStep.tolist() not in obj.tolist()) and nextStep[0] >= 0 and nextStep[0] <= (vSize - 1) and nextStep[1] >= 0:
            loc = np.vstack([loc, nextStep])
        
        # Show new position
        displayRoom(loc, obj, vSize, hSize)
        
        # Check if the South side of the image has been reached
        if loc[-1][0] == vSize-1:
            print("Success!")
            break
        