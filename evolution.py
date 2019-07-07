import numpy as np
import matplotlib.pyplot as plt

grid_size = 16
grid = np.zeros((grid_size, grid_size))
start_number = 20
num_of_organisms = []

class Organism(object):
    def __init__(self, x, y, size=1, efficiency=.1):
        self.energy = 1
        self.x = x
        self.y = y
        self.size = size
        self.efficiency = efficiency
        
    def move(self, x, y):
        self.x += x
        self.y += y
        
    def feed_veg(self, grid):
        if self.x >= 0 and self.x < grid_size and self.y >= 0 and self.y < grid_size:
            self.energy += grid[self.x, self.y] * (1-np.exp(-self.efficiency))
            grid[self.x, self.y] *= np.exp(-self.efficiency)
    
    def maintain(self):
        self.energy -= (self.efficiency/10+ 1) * 0.6 * self.size**1.2
    
    def alive(self):
        return self.energy > 0
        
    def give_birth(self):
        if self.energy > 20:
            self.energy -= 8
            return 1
        else:
            return 0
            
    def pos(self):
        return (self.x, self.y)

organisms = []
for i in range(start_number):
    x = np.random.randint(0, grid_size)
    y = np.random.randint(0, grid_size)
    organism = Organism(x, y)
    organisms.append(organism)

organism_eaten = []

for i in range(500):
    in_this_round_eaten = 0
    grid += 2
    for org_i, org in enumerate(organisms):
        x = np.random.randint(-1, 2)
        y = np.random.randint(-1, 2)   
        org.move(x, y)
        org.feed_veg(grid)
        # check if eatable organisms is in same field
        positions = np.array([o.pos() for o in organisms]) # array mit Positionen als Tupel
        coincide = np.all(positions == org.pos(), axis=1) # Array mit allen gleichen Positionen alsTrue
        coincide = np.nonzero(coincide)
        prey = [organisms[i] for i in coincide[0]]
        for victim in prey: # iterates through indices of eatable prey
			if org.size > 2 * victim.size: # disqualifies eating itself
				org.energy += 0.8 * victim.energy
				organisms.remove(victim)
				in_this_round_eaten += 1
        org.maintain()
        if not org.alive(): 
            organisms.remove(org)
        if org.give_birth():
            parent_size=org.size
            parent_effi=org.efficiency
            child_size = parent_size + (np.random.random_sample() - 0.5)/3
            child_effi = parent_effi + (np.random.random_sample() - 0.5)/3            
            child = Organism(org.x, org.y, child_size, child_effi)
            organisms.append(child)

    num_of_organisms.append(len(organisms))
    organism_eaten.append(in_this_round_eaten)
    
s = [i.size for i in organisms]
e = [i.efficiency for i in organisms]


fig, ax1 = plt.subplots()
ax1.set_ylabel('Population')
ax1.plot(num_of_organisms, 'g')

ax2 = ax1.twinx()
ax2.set_ylabel('carnivor activity')
ax2.plot(organism_eaten, 'r')
plt.show()

#plt.hist(s, bins=30)
#plt.show()
plt.plot(s, e, 'bo')
plt.show()