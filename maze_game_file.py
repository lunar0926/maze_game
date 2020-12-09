'''
201600372 언어학과 박재형 텀 프로젝트 2
거북이가 적들을 피해 미로를 탈출해야 합니다!!
거북이는 3의 생명력을 가지고 시작합니다.
화면 오른쪽 아래에 현재 생명력을 표시합니다.
적 거북이는 6마리가 있으며 적과 부딪히면 적은 소멸하지만 생명력이 1 감소합니다.
적 거북이들은 정해진 범위를 이동하며 순찰합니다. (순찰하는 스케줄은 규칙적입니다)
미로에는 아이템들이 있습니다. 아이템을 획득하면 생명력 1이 추가됩니다.
미로에는 적 거북이들 뿐만 아니라 함정도 길을 가로막고 있습니다.
생명력이 모두 소모되면  게임 오버
생명력이 모두 소모되지 않고 미로를 탈출하면 게임 클리어!
팁) 적 거북이들을 피해갈 때는 타이밍에 맞춰 최대한 빠르게 이동해야 합니다.

아래 난이도 조절용 수치들을 통해 난이도 조절도 가능합니다.
(2020.12.09) 게임 클리어, 게임 오버 시에 이동했던 경로가 나오고
자동 종료 됩니다.
'''


import turtle
import math

win = turtle.Screen()
t1 = turtle.Turtle("turtle")

width = 555 + 50
height = 548 + 50
win.setup(width, height)
win.bgpic("11.maze.gif")

# 경로를 텍스트 파일에 저장
fin = open('maze_game.txt', 'w')
fin.close()

# 파일에서 경로를 읽기
def readCoords(fileName):
    mydata = list()
    with open(fileName) as f:
        for line in f:
            line = line.strip()
            nums = line.split(',')
            coord = list()
            for num in nums:
                coord.append(float(num))
            mydata.append(coord)
        return mydata
# 이동 경로를 보여주는 함수(게임 오버, 게임 클리어 시에 선언)
def showCoords(fileName):
    coords = readCoords(fileName)
    t1.goto(-90, -270)
    t1.speed(1)
    t1.pencolor('Blue')
    for coord in coords:
        t1.pendown()
        t1.goto(coord[0], coord[1])
    turtle.bye() # 이동 경로를 보여주고 자동 종료



# 난이도 조절용 
turtle.tracer(1, 5) # 두 번째 인자가 커질수록 적 거북이들의 속도가 느려짐
HP = 3 # 거북이의 초기 생명력

distance = 15 # 한 번에 움직이는 거리
t1.shapesize(1.2, 1.2, 1)
# 거북이 로봇을 미로 입구에 위치시킴
t1.penup() # 이동할 때 펜을 쓰지않고 거북이만 보이게
t1.goto(-90, -270)

# 함정의 위치 (함정 4개)
traps = [
    [-50, 270, 0, 220],
    [160, 170, 210, 120],
    [50, 0, 100, -50],
    [-220, -100, -170, -150]
]
# 적 거북이 리스트 [거북이 객체][이동 방향][이동 거리]
enemies = []

# 아이템 리스트
items = []

# 적 거북이
for i in range(0, 6) :
    enemy = turtle.Turtle("turtle")
    enemy.ht()
    enemy.penup()
    enemy.color("Red")
    enemy.speed(1)
    heading = None
    count = None
    enemies.append([enemy,heading, count])

# 적 거북이들의 시작 위치   
enemies[0][0].goto(-145, 25)
enemies[0][0].st()    
enemies[1][0].goto(25, 145)
enemies[1][0].st()
enemies[2][0].goto(135, 245)
enemies[2][0].st()
enemies[3][0].goto(-35, 35)
enemies[3][0].st()
enemies[4][0].goto(-35, -185)
enemies[4][0].st()
enemies[5][0].goto(-35, 185)
enemies[5][0].st()

# 적 거북이들의 이동 방향(enemyMove함수에서 사용)
# 동 = 0, 서 = 180, 남 = 270, 북 = 90
enemies[0][1] = 0
enemies[1][1] = 90
enemies[2][1] = 0
enemies[3][1] = 0
enemies[4][1] = 270
enemies[5][1] = 180

# 적 거북이들의 이동 거리(enemyMove함수에서 사용)
# x * 50 만큼 이동함.  ex) 1 * 50, 2* 50
enemies[0][2] = 1
enemies[1][2] = 1
enemies[2][2] = 2
enemies[3][2] = 1
enemies[4][2] = 1
enemies[5][2] = 1

# 아이템
for i in range(0, 4) :
    item = turtle.Turtle("circle")
    item.ht()
    item.penup()
    item.color("Green")
    items.append(item)
items[0].goto(-195, 245)
items[0].st()
items[1].goto(-195, 150)
items[1].st()
items[2].goto(185, 85)
items[2].st()
items[3].goto(-245, 25)
items[3].st()
    

# 상태창
display = turtle.Turtle()
display.ht()
display.penup()
display.color("Black")
display.goto(230, -290)
display.write("HP: "+str(HP))

# v1과 v2 중에서 작은 값을 반환하는 함수
def getMinValue(v1, v2):
    if v1 < v2:
        return v1
    return v2
# v1과 v2 중에서 큰 값을 반환하는 함수
def getMaxValue(v1, v2):
    if v1 > v2:
        return v1
    return v2

def moveTo(x, y):
    t1.penup()
    t1.goto(x, y)
    t1.pendown()

def writeGameOver(): # HP가 모두 소모되었을 때 이 함수를 사용함.
    t1.penup()
    t1.home()
    t1.pendown()
    t1.write("Game over")
    showCoords('maze_game.txt')

# 도착 지점에 오면 성공 표시를 나타내주는 함수 선언하기. 각 이동에서 확인
def writeGameClear(x, y):
    if x >= 0 and x <= 50 and y >= 270 :
        t1.clear()
        t1.pendown()
        t1.write("미로 탈출 성공!!")
        showCoords('maze_game.txt')

''' 거북이의 위치가 x, y이고 함정의 위치가 x1, y1, x2, y2일 때 min, max를 구해서
함정에 들어갔는지 확인. 함정을 리스트로 받음'''
def isInTrap(x, y, trap):
    minX = getMinValue(trap[0], trap[2]) # x1, x2
    maxX = getMaxValue(trap[0], trap[2]) # x1, x2
    minY = getMinValue(trap[1], trap[3]) # y1, y2
    maxY = getMaxValue(trap[1], trap[3]) # y1, y2
    if x >= minX and x <= maxX and y >= minY and y <= maxY:
        return True
    else:
        return False
# 함정에 해당하는 여러 리스트들에 대하여 반복문으로 확인해주는 함수
def isInTraps(x, y, traps):
    for trap in traps:
        if isInTrap(x, y, trap):
            return trap
    return None
def showTrapInRed(trap):
    t1.fillcolor("red")
    t1.begin_fill()
    moveTo(trap[0], trap[1])
    t1.goto(trap[2], trap[1])
    t1.goto(trap[2], trap[3])
    t1.goto(trap[0], trap[3])
    t1.goto(trap[0], trap[1])
    t1.end_fill()
    moveTo(trap[2] + distance, trap[3] + distance)
    t1.fillcolor("black")

# 거북이의 생명력을 확인해주는 함수
def checkHP() :
    if (HP == 0) :
        writeGameOver()

# 플레이어의 거북이와 적 거북이가 만나는 경우의 함수
def encounterEnemy (x, y, enemy) :
    global HP
    ePosition = enemy.pos()
    if math.sqrt(((x - ePosition[0]) * (x - ePosition[0]))
    + ((y - ePosition[1]) * (y - ePosition[1]))) <= 22 :
        HP -= 1
        display.clear()
        display.write("HP: "+str(HP))
        enemy.ht()
        enemy.goto(-320, 290) # 적 거북이가 부딪힐 수 없는 위치로 이동
        
        
def encounterEnemies (x, y, enemies) :
    for eList in enemies :
        enemy = eList[0]
        encounterEnemy (x, y, enemy)
      
# 적 거북이들의 이동
def enemyMove(enemy, heading, count) :
    enemy.setheading(heading)
    for i in range(0, count) :
        enemy.forward(50)
    enemy.setheading(heading + 180)
    for i in range(0, count) :
        enemy.forward(50)
    

# 아이템 획득
def encounterItem (x, y, item) :
    global HP
    iPosition = item.pos()
    if math.sqrt(((x - iPosition[0]) * (x - iPosition[0]))
    + ((y - iPosition[1]) * (y - iPosition[1]))) <= 20 :
        HP += 1
        display.clear()
        display.write("HP: "+str(HP))
        item.ht()
        item.goto(-500, 500)

def encounterItems (x, y, items) :
    for item in items :
        encounterItem(x, y, item)
            
        
# 이동
def keyeast():
    t1.penup()
    t1.setheading(0)
    position = t1.pos()
    t1.goto(position[0] + distance, position[1])
    # 좌표를 텍스트 파일에 저장
    fin = open('maze_game.txt', 'a')
    fin.write("{0}, {1}\n".format(t1.xcor(), t1.ycor()))
    fin.close()
    trap = isInTraps(position[0] + distance, position[1], traps) # 함정 확인
    if trap != None:
        showTrapInRed(trap)
    encounterEnemies (position[0] + distance, position[1], enemies) # 적과 마주쳤는지 확인
    encounterItems (position[0] + distance, position[1], items) # 아이템 획득 확인
    checkHP()
    writeGameClear(position[0] + distance, position[1]) # 탈출 성공 확인
def keywest():
    t1.penup()
    t1.setheading(180)
    position = t1.pos()
    t1.goto(position[0] - distance, position[1])
    # 좌표를 텍스트 파일에 저장
    fin = open('maze_game.txt', 'a')
    fin.write("{0}, {1}\n".format(t1.xcor(), t1.ycor()))
    fin.close()
    trap = isInTraps(position[0] - distance, position[1], traps) # 함정 확인
    if trap != None:
        showTrapInRed(trap)
    encounterEnemies (position[0] - distance, position[1], enemies) # 적과 마주쳤는지 확인
    encounterItems (position[0] - distance, position[1], items) # 아이템 획득 확인
    checkHP()
    writeGameClear(position[0] - distance, position[1]) # 탈출 성공 확인
def keysouth():
    t1.penup()
    t1.setheading(270)
    position = t1.pos()
    t1.goto(position[0], position[1] - distance)
    # 좌표를 텍스트 파일에 저장
    fin = open('maze_game.txt', 'a')
    fin.write("{0}, {1}\n".format(t1.xcor(), t1.ycor()))
    fin.close()
    trap = isInTraps(position[0], position[1] - distance, traps) # 함정 확인
    if trap != None:
        showTrapInRed(trap)
    encounterEnemies (position[0], position[1] - distance, enemies) # 적과 마주쳤는지 확인
    encounterItems (position[0], position[1] - distance, items) # 아이템 획득 확인
    checkHP()
    writeGameClear(position[0], position[1] - distance) # 탈출 성공 확인
def keynorth():
    t1.penup()
    t1.setheading(90)
    position = t1.pos()
    t1.goto(position[0], position[1] + distance)
    # 좌표를 텍스트 파일에 저장
    fin = open('maze_game.txt', 'a')
    fin.write("{0}, {1}\n".format(t1.xcor(), t1.ycor()))
    fin.close()
    trap = isInTraps(position[0], position[1] + distance, traps) # 함정 확인
    if trap != None:
        showTrapInRed(trap)
    encounterEnemies (position[0], position[1] + distance, enemies) # 적과 마주쳤는지 확인
    encounterItems (position[0], position[1] + distance, items) # 아이템 획득 확인
    checkHP()
    writeGameClear(position[0], position[1] + distance) # 탈출 성공 확인
    
# 이벤트 처리 함수 등록
win.onkey(keyeast, 'Right')
win.onkey(keywest, 'Left')
win.onkey(keysouth, 'Down')
win.onkey(keynorth, 'Up')

win.listen()

# 적 거북이들의 이동
while True :
    for eList in enemies :
        enemy = eList[0]
        heading = eList[1]
        count = eList[2]
        enemyMove(eList[0], eList[1], eList[2])
turtle.mainloop()












