import random

from timeit import default_timer as timer

#class system:

class Star:
  def __init__(self):
    self.temp = random.randint(-11000,11000) # Object temp in K
    self.coords = (0,0) # Coords inside the solar system
    self.mass = random.randint(100000,int(9.100044032093486e+38)) # Sun mass
    self.planets = random.randint(0,10)
    self.life_planets = 0 # Planets which can harbour life
    # Heat radiation
    self.heat_loss = 0.00030357407 # W/m^2 lost per meter
    self.planets_list = []

  def gen_planets(self):
    planet = Planet(self)
    self.planets_list.append(planet)
    return self.planets_list


class Planet:
  def __init__(self,star):
    self.star = star
    self.mass = random.randint(1,int(3.2658604127134476e+34)) # Mass
    #self.star_proximity = (((int(8.541838482747008e-21))(star.mass)(self.mass))) # Based on our worlds universal gravitational constant
    self.moon_count = random.randint(0,100)
    self.moons = []
    self.create_moons()

  def create_moons(self):
    for x in range(self.moon_count):
      moon = Moon(self)


  def test(self):
    self.create_moons()
    print(self.star_proximity) 
    quit()

class Moon:
  def __init__(self,planet):
    self.mass = (planet.mass*10)**-5



def build_systems(a):
  # Number of stars in a system
  star_count=random.randint(0,3)
  planet_count=random.randint(0,7)
  for x in range(a):
    star = Star()
    planets = star.gen_planets()
    for planet in planets:
      planet.create_moons()
    print("Star")

if __name__=="__main__":
  start = timer()
  build_systems(10)
  print("Build took:", timer()-start)
