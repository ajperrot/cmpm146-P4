

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

#if we only have 1 planet
def lone_ally(state):
  return len(state.my_planets()) == 1

#enemy has only 1 planet
def lone_enemy(state):
  return len(state.enemy_planets()) == 1