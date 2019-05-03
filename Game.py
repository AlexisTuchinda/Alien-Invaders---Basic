# Alien Invaders Group Session FINISHED VERSION
from random import randint
from processing import *
from time import *

WIDTH = 400
HEIGHT =400
bullets = []
enemies = []
levels = 0
killed = 0
goal = 10
delay = 0
speed = 7
motherHealth = 100
overallBullets = 0
overallKills = 0
inGame = False
bulletDelay = 0
bulletLimit = 100
end = False

def setup():
  frameRate(40)
  size(WIDTH, HEIGHT)
  
class Entity:
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.isLeft = False
    self.isRight = True
    
  def draw(self, shape):
    if shape == "rect":
      return rect(self.x, self.y, self.width, self.height)
    else:
      return ellipse(self.x, self.y, self.width, self.height)

def mouseClicked():
  global bullets,overallBullets, inGame, end, bulletLimit
  amount = 2
  if not end:
    inGame = True
    end = True
  if overallBullets < bulletLimit:
    if len(bullets) < amount:
      bullets.append(Entity(player.x, player.y, 10, 10))
      overallBullets += 1
  
def drawAll(items, shape):
  for i in range(len(items)):
    items[i].draw(shape)
    
def moveAll(items, amount, isUp):
  for i in range(len(items)):
    if isUp:
      items[i].y -= amount
    else:
      items[i].y += amount
      
def enemyAI(items,down, side, a):
  global motherHealth
  for i in range(len(items)):
    if items[i].isRight: 
      items[i].x += side
      if items[i].x >= WIDTH-items[i].width:
        items[i].y +=down
        items[i].isLeft = True
        items[i].isRight = False
    if collision(a, items[i]):
      items.remove(items[i])
      motherHealth -= 5
      return

     
    if items[i].isLeft:
      items[i].x -= side
      if items[i].x <= 0:
        items[i].y += down
        items[i].isLeft = False
        items[i].isRight = True
        
    if collision(a, items[i]):
      items.remove(items[i])
      motherHealth -= 5
      return

    

def addText(string, x, y, size, r, g, b):
  textSize(size)
  fill(r, g, b)
  return text(string, x, y)


def genEnemies(amount):
  for i in range(amount):
   enemies.append(Entity(randint(0, WIDTH), 10, 35, 35))
    
    
def timedEnemies(delayAmount):
  global delay
  if delay < delayAmount:
    delay += 1
  else:
    enemies.append(Entity(randint(0, WIDTH), 10, 35, 35))
    delay = 0

  
def collision(shape1, shape2):
  if shape1.x < shape2.x + shape2.width and shape1.x + shape1.width > shape2.x and shape1.y < shape2.y + shape2.height and shape1.height + shape1.y > shape2.y:
    return True
  else:
    return False

def timedBulletPacks(items):
  global bulletDelay
  if bulletDelay > 300:
    items.append(Entity(randint(0, WIDTH), 0, 20, 45))
    bulletDelay = 0
  else:
    bulletDelay += 1

    
def healthBar(x, y, amount):
  global inGame
  if amount < 1:
    inGame = False
  else:
    return rect(x, y, amount, 10)
    
def bulletCollide(items):
  global killed, overallKills
  for i in range(len(items)):
    for each in bullets:
      if collision(each, items[i]):
        items.remove(items[i])
        bullets.remove(each)
        killed += 1
        overallKills += 1
        return 
      
def deleteBullet():
  for i in range(len(bullets)):
    if bullets[i].y <= 0:
      bullets.remove(bullets[i])
      return
    
def level(counter, amount):
  global levels,speed
  if counter > amount:
    amount += 15
    counter = 0
    levels += 1
    speed += 0.1
  return 
  
def bulletPackAI(items, items2):
  global overallBullets
  amount = randint(5, 10)
  for i in range(len(items)):
    items[i].y += 1
    for j in range(len(items2)):
      if collision(items[i], items2[j]):
        items.remove(items[i])
        overallBullets -=amount
        
        return 
        
 
  
bulletPack = [Entity(randint(0, WIDTH), 0, 20, 45)]
player = Entity(WIDTH/2-50, 300, 50, 50)
mothership = Entity(WIDTH/2, 400, WIDTH, 50)
healthBar2 = Entity(0, 350, 100, 10)

def update():
  background(0, 0, 0)
  
  if inGame:
    fill(150, 150, 150)
    mothership.draw("ellipse")
    fill(160, 215, 255)
    player.draw("ellipse")
    fill(0, 70, 200)
    healthBar2.draw("rect")
    fill(0, 200, 70)
    healthBar(0, 350, motherHealth)
    fill(200, 0, 100)
    drawAll(bullets, "ellipse")
    fill(255, 0, 0)
    drawAll(enemies, "rect")
    fill(255, 153, 0)
    drawAll(bulletPack, "rect")
    enemyAI(enemies, randint(20, 45), 15, mothership) 
    bulletPackAI(bulletPack, bullets)
    player.x = mouse.x
    bulletCollide(enemies)
    moveAll(bullets, 15, True)
    timedEnemies(20)
    timedBulletPacks(bulletPack)
    deleteBullet()
    level(killed, goal)
    addText("Kills: "+str(overallKills), 10, 340, 10,61, 255, 61)
    addText("Bullets: "+str(abs(bulletLimit-overallBullets)), 340, 340, 10, 61, 255, 61)
  else:
    if end:
      if overallKills > 100:
        addText("You Win!", 150, 200, 25, 255, 255, 255)
        addText("You killed "+str(overallKills)+" aliens!", 60, 275, 30, 254, 0, 39)
        addText("Thank you for playing Alien Invaders", 85, 350, 15, 255, 255, 255)
      else:
        addText("You Lose!", 145, 200, 25, 255, 255, 255)
        addText("You killed "+str(overallKills)+" aliens!", 60, 275, 30, 254, 0, 39)
        addText("Try Again!", 175, 350, 15, 255, 255, 255)
    else:
      addText("GOAL: Protect the Mothership from the enemies!", 35, 25, 15, 0, 80, 255)
      addText("Shoot bullets by clicking the mouse", 75, 50, 15, 7, 233, 155)
      addText("CREATED BY POPCORN PANDICORN", 50, 150, 15, 255, 255, 255)
      addText("Alien Invaders!", 25, 200, 50, 56, 233, 45)
      addText("Click Mouse to Start!", 70, 250, 25, 255, 255, 255)
      addText("Red represents enemies", 115, 350, 15, 255, 0, 0)
      addText("Yellow represents bullet packs", 100, 375, 15, 255, 155, 25)
  #mothershipHealth(mothership, healthBar, enemies):
  #addText("Level:", 300, 200, 10, 10, 0, 0)
  
  
draw = update
run()
