import sys


def debug(text):
    print(text, file=sys.stderr, flush=True)

def signum(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0


# nbFloors: number of floors
# width: width of the area
# nbRounds: maximum number of rounds
# exitFloor: floor on which the exit is found
# exitPos: position of the exit on its floor
# nbTotalClones: number of generated clones
# nbAdditionalElevators: ignore (always zero)
# nbElevators: number of elevators
m={}

nbFloors, width, nbRounds, exitFloor, exitPos, nbTotalClones, nbAdditionalElevators, nbElevators = [int(i) for i in
                                                                                                    input().split()]
for i in range(nbElevators):
    # elevatorFloor: floor on which this elevator is found
    # elevatorPos: position of the elevator on its floor
    elevatorFloor, elevatorPos = [int(j) for j in input().split()]
    m[elevatorFloor]=elevatorPos
m[exitFloor]=exitPos

# game loop
while 1:
    # cloneFloor: floor of the leading clone
    # clonePos: position of the leading clone on its floor
    # direction: direction of the leading clone: LEFT or RIGHT
    cloneFloor, clonePos, direction = input().split()
    cloneFloor = int(cloneFloor)
    clonePos = int(clonePos)
    dir = -1 if direction == "LEFT" else 1

    debug(m)
    debug(cloneFloor)
    if cloneFloor == -1: # no leading clone yet -> wait
        print("WAIT")
        continue

    targetPos = m[cloneFloor]
    targetDir = targetPos - clonePos
    action = "WAIT" if signum(targetDir) == signum(dir) or targetDir == 0 else "BLOCK"

    debug(direction)
    debug(dir)
    debug(targetDir)

    print(action)  # action: WAIT or BLOCK

    # alternative solution (based on code golf)
    # targetPos = m[cloneFloor]
    # if dir*targetPos >= dir*clonePos: print("WAIT")
    # else:print("BLOCK")
