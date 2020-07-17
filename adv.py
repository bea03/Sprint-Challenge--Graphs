from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
#from util import Stack, Queue 

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

#previous visited rooms:
prev_rooms = []

'''
#dictionary of visited rooms
dictionary: 
    key = room id
    values = direction with its ? default then room num or none
'''
visited = {}

#reverse directions:
reverse_dir = {'n': 's', 'e': 'w', 'w': 'e', 's': 'n'}

#add the starting room the player is in to the visited dictionary:
visited[player.current_room.id] = player.current_room.get_exits()
#should look like: 
#{
#  0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
#}
#while there are still rooms to visit
#only move through the rooms while the length of visted is less than the len of rooms graph
while len(visited) < len(room_graph):
    #check if the room has been visited the key is the room id
    if player.current_room.id not in visited:
        #add the room to visited list
        visited[player.current_room.id] = player.current_room.get_exits()
        #get last room travelled
        last_room = prev_rooms[-1]
        #remove it from unexplored paths
        visited[player.current_room.id].remove(last_room)
    #check if all paths are explored, when all paths are 0, then it is a deadend
    if len(visited[player.current_room.id]) == 0:
        #go back until unexplored room
        last_room = prev_rooms[-1]
        prev_rooms.pop()
        #add where player went to traversal path because those moves count
        traversal_path.append(last_room)
        #move to the room
        player.travel(last_room)
    #explore where we havent gone yet
    else:
        #get the last exit, explore new room
        movement = visited[player.current_room.id][-1]
        visited[player.current_room.id].pop()
        #add movement to traversal path
        traversal_path.append(movement)
        #get backtrack path:
        prev_rooms.append(reverse_dir[movement])
        player.travel(movement)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

# #######
# # UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
