# 2406_olymbits

Time spent programming:
17.6. 2212 - 2220 - basic code structure
19.6. 833 - 848 - optimal 1 hurdle + inheritance
19.6. 2250 - 2258 - multi game ideas
20.6. 831 - 845 - multi game ideas
20.6. 2250 - 2325 - parse code, wood II completed
22.6. 2154 - 2227 - optimal for lowest score game - doesn't work for boss
22.6. 2227 - 2320 - trying most common preferred action - to little success
23.6. 1149 - 1203 - when 4+ spaces from hurdle, abstain from decision, it works, Wood I. completed!
23.6. 2050 - 2111 - refactor of game inputs, diving game
23.6. 2258 - 003 - diving and archery game implemented

TODO:
* when 3 spaces to hurdle - abstain?
* ignore first few archery turns?
* ignore first/last few diving turns?

# multiple hurdles games ideas:
* take leading dist into account and ignore totally won and lost games
* if draw for most common, prefer UP if present
* then try return preference number with prefered action (or each action)
* then take leading dist and score for final weighting
