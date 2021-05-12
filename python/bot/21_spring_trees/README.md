# Trees

ideas:
mozna slots na dataclasses

catboss
seed
-7665273193536899100
15:139  # wood algorithm (cut down tree on the richest soil)
--
33:125  # grow if you can, keep both
35:119  # grow if you can, chop if you can
103:106 # grow if you can, seed if you can, cut down everything on the last day
102,1:102,6 # grow if you can (prefer rich soil), seed if you can, cut down everything on the last day
111:102 # + only grow if the tree is not dormant
116:97 # + only seed if the tree is not dormant
123:100 # + only have max 6 trees, then cut
114:101 # + only have max 7 trees, then cut
127:104 # + only have max 7 trees of size 1+, then cut

vs. SIHUSIA
105:136 cut when more than 9 trees
104:135 cut when more than 10 trees

vs. Bossoot
seed=0
68:167 cut when more than 10 trees
75:151 + seed only if tree size is 1+
76:151 + seed can also go many cells from tree in one dir
77:159 + seed can also go many cells from tree in the area
97:148 + seed only not neighbouring the original tree (can neigh others) (202:249)
88:143 + seed only not neighbouring any tree of mine (270:235 cum sun sum)


time spent: 
15min? for wood alg
1h30m 2000 to 2130 for heur for bronze (plant, ignore shadow)
2h 22:30 to 00:30 for the same, finally in silver! 
We
 1950 - 