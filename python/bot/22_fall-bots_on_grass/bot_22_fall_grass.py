width, height = [int(i) for i in input().split()]

while True:
    my_matter, opp_matter = [int(i) for i in input().split()]
    for i in range(height):
        for j in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]

    print("WAIT")
