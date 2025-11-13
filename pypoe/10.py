# program for class, object and constructor using suitable data 

class Monster:
    def __init__(self):
        self.health = 100
        self.damage = 10
    

    def attack(self):
        print("Attacked with damage of : ",self.damage)
        print("Damage dealt of 5")
        self.health -=5
        print("Current health is : ",self.health)
        print()

    def upgrade(self):
        print("Damage upgraded by : 5")
        self.damage += 5
        print("Current damage is : ",self.damage)
        print()

    def heal(self):
        print("Healed to full health")
        self.health = 100
        print("Current Health : ",self.health)
        print()


monster_one = Monster()
monster_one.attack()
monster_one.upgrade()
monster_one.attack()
monster_one.heal()
