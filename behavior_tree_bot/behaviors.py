import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
from math import inf


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 1)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

#send larger fleet to planet enemy is sending a fleet to overtake
def counter_fleet(state):
    #find enemy fleet not already being countered
    target = None
    for enemy_fleet in state.enemy_fleets():
        if enemy_fleet.num_ships > state.planets[enemy_fleet.destination_planet].num_ships:
            covered = False
            for my_fleet in state.my_fleets():
                if enemy_fleet.destination_planet == my_fleet.destination_planet:
                    #fleet already being countered
                    covered = True
                    break
            if covered == False:
                #eligible fleet found
                size = enemy_fleet.num_ships
                target = enemy_fleet.destination_planet
                break
    if not target:
        return False
    
    #find planet capable of countering the enemy fleet
    best_planet = state.my_planets()[0]
    best_dist = state.distance(best_planet.ID, target)
    planet_found = False
    for planet in state.my_planets():
        if planet.num_ships > size + 1:
            possible_dist = state.distance(planet.ID, target)
            if possible_dist < best_dist:
                best_planet = planet
                best_dist = possible_dist
                planet_found = True

    #send counterfleet
    if not planet_found:
        return False
    else:
        return issue_order(state, best_planet.ID, target, size + 1)

#capture largest growth planet from closest eligible planet
def take_high_growth(state):
    target = max(state.planets, key=lambda p: p.growth_rate, default=None)
    best_dist = inf
    best_source = None
    best_size = None #fleet_size
    for planet in state.my_planets():
        this_dist = state.distance(planet.ID, target.ID)
        #this should work for a lot of cases as the # of ships needed to capture
        required_ships = target.num_ships + (this_dist * target.growth_rate) + 1
        if planet.num_ships > required_ships and this_dist < best_dist:
            best_source = planet
            best_dist = this_dist
            best_size = required_ships
    if not best_source:
        return False
    else:
        return issue_order(state, best_source.ID, target.ID, best_size)

#send massive force to first enemy spotted
def rush_first_target(state):
    target = state.enemy_planets()[0]
    best_dist = inf
    best_source = None
    for planet in state.my_planets():
        this_dist = state.distance(planet.ID, target.ID)
        #this should work for a lot of cases as the # of ships needed to capture
        required_ships = target.num_ships + (this_dist * target.growth_rate) + 1
        if planet.num_ships > required_ships and this_dist < best_dist:
            best_source = planet
            best_dist = this_dist
    if not best_source:
        return False
    else:
        return issue_order(state, best_source.ID, target.ID, best_source.num_ships - 1)

    
