# 22 spring bot contest - Notes, todos, data, ...

## time spent
21.4. 15:45 - 16:05 - prepare
21.4. 2210 - 2310 basic structs, attack monster nearest base, enough for Wood 1 probably?
24.4. 1505 - 1740 IDE configuring, refactor, basic exploration, still bronze
24.4. 1910 - 1950 cast WIND as last resort (if not shielded) - good defense against just spiders
24.4. 2115 - 


ideas/todos:
how fast can hero get to the monster?
defend only w/ necessary num of heroes

when I can't WIND (I'm too far), try CONTROL SPELL
when I can select which monster to attack not nearest but nearest with threat_for = myself
when I kill 4 fun, don't target monster with threat_for == 2

when monster outside of my 5k radius and > 100 mana and monster.health > 20?, control to opp base (random select/switch between 2 extremes?)
if monster threat for=2, cast shield if mana > 150 and blabla?


seeds:
boss 3 has more wild mana 454 vs 118
seed=-5057810513120155600


saved code:
dist_to_attack_monster = hero.p.dist(monster.p) - HERO_DAMAGE_RADIUS
if dist_to_attack_monster > 0:
# # todo method - is it the most important feature now?
# # todo find n turns to first attack the monster + the vector for that
# hero_p = hero.p
# monster_p = monster.p
# for i_turn in range(monster.turns_to_base):
#     dist_to_attack_monster = hero_p.dist(monster_p) - HERO_DAMAGE_RADIUS
#     # todo plus i_turn!
#     turns_to_attack_m_if_still = dist_to_attack_monster/HERO_SPEED
#     # todo find best
#     # if not vector to base it will have weird numbers and results!
#     monster_p += monster.vp  # is vp reliable?
