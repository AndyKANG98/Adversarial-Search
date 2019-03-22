# Adversarial-Search
CSCI360 Project 2

> Project Goal: Given the current rosters and pool, choose the next hero that eventually maximizes
your advantage against your opponent. You are the captain of the Radiant in a DotA 2 tournament. You
and your opponent must choose from the same pool of N heroes, and each hero can only be picked once.
You will take turns choosing (Radiant ! Dire ! Radiant ! ... ! Dire),2 and you each must choose on
your turn (i.e., no skipping your turn). You will choose first. The process ends after your team and your
opponent team both have exactly 5 heroes (i.e., 10 distinct heroes are picked in total)

* Advantage Formula: A = Sradiant + Nradiant∑mi × pi− Sdire + Ndire∑ mj × pj

* Implemented "Minmax" method and "Minmax with alpha beta pruning" to select the best next action for Radiant
