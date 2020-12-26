from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        if len(self.children) > 0:
            return 0
        else:
            return 1

# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # recursive function to build a game tree
    def build_tree(self, node=None, depth=0, ec=False):
        if node == None:
            node = self.root
        if depth == self.search_depth: 
            return 

        child_nodes = []
        self.simulator.reset(*(node.state))
        if not ec:
            if node.player_type == MAX_PLAYER:
                # TODO: find all children resulting from 
                # all possible moves (ignore "no-op" moves)

                # NOTE: the following calls may be useful:
                # self.simulator.reset(*(node.state))
                # self.simulator.get_state()
                # self.simulator.move(direction)
                for direction in MOVES:
                    if self.simulator.move(direction):
                        child_nodes.append((direction, self.simulator.get_state()))
                        self.simulator.reset(*(node.state))
                for child_node in child_nodes:
                    node.children.append( (child_node[0], Node(child_node[1], CHANCE_PLAYER)))

            elif node.player_type == CHANCE_PLAYER:
                # TODO: find all children resulting from 
                # all possible placements of '2's
                # NOTE: the following calls may be useful
                # (in addition to those mentioned above):
                # self.simulator.get_open_tiles():
                open_tiles = self.simulator.get_open_tiles()
                for open_tile in open_tiles:
                    self.simulator.reset(*(node.state))
                    self.simulator.tile_matrix[open_tile[0]][open_tile[1]] = 2
                    child_nodes.append(Node(self.simulator.get_state(), MAX_PLAYER))
                for child_node in child_nodes:
                    node.children.append( (-1 , child_node) )
            # TODO: build a tree for each child of this node
            for child in node.children:
                self.build_tree(child[1], (depth+1), ec)
        return


    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            return -1, node.state[1]
        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            best_direction = -1
            best_value = node.state[1]
            for ea in node.children:
                _ ,expected_MAX = self.expectimax(ea[1])
                if best_value <= (expected_MAX):
                    best_value = expected_MAX
                    best_direction = ea[0]
            # if best_direction == -1:
            #     return random.randint(0,3), best_value
            return best_direction, best_value
        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            value = 0
            for ea in node.children:
                direction,expected_best_value = self.expectimax(ea[1])
                value = value + ((float)(expected_best_value/len(node.children) ))

            return -1, value
    def decision_ec(self, node = None):
        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            return -1, state[0]
        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            best_direction = -1
            best_value = node.state[1]
            for ea in node.children:
                _ ,expected_MAX = self.decision_ec(ea[1])
                if best_value <= (expected_MAX):
                    best_value = expected_MAX
                    best_direction = ea[0]
            # if best_direction == -1:
            #     return random.randint(0,3), best_value
            return best_direction, best_value
        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            value = 0
            for ea in node.children:
                direction,expected_best_value = self.decision_ec(ea[1])
                value = value + ((float)(expected_best_value/len(node.children) ))

            return -1, value
    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # TODO delete this
        self.build_tree()
        direction,_ = self.decision_ec(self.root)
        return random.randint(0, 3)
