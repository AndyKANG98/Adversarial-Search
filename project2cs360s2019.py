def Read_file(filename):
    lines = open(filename + ".txt").read().splitlines()
    num_hero_pool = int(lines[0])
    algorithm = lines[1]
    heros_list = []
    for line in lines[2:]:
        heros_list.append(list(eval(line)))
    hero_id_list = list(heros_list[i][0]for i in range(num_hero_pool))
    hero_membership_list = list(heros_list[i][4]for i in range(num_hero_pool))
    
    heros_pool = {key: value for (key, value) in zip(hero_id_list, heros_list)}
    heros_membership = {key: value for (key, value) in zip(hero_id_list, hero_membership_list)}
    initial_level = 0
    for key in heros_membership:
        if heros_membership[key] != 0:
            initial_level += 1
    return algorithm, initial_level, heros_pool, heros_membership

def Write_output(best_hero):
    output_file = open("output.txt","w")
    output_file.write(str(best_hero))
    output_file.close()

class State:
    def __init__(self, level, player, heros_membership):
        self.level = level
        self.player = player
        self.heros_membership = heros_membership

    def next_state(self, hero_id):
        new_level = self.level + 1
        new_player = -self.player
        new_heros_membership = self.heros_membership.copy()
        
        if new_player == 1:
            new_heros_membership[hero_id] = 2
        else:
            new_heros_membership[hero_id] = 1
        
        return State(new_level, new_player, new_heros_membership)
    
    def cal_advantage(self, heros_pool):
        my_last_digit=[]
        my_synergy = 120
        my_power = 0
        opponent_last_digit=[]
        opponent_senergy = 120
        opponent_power = 0
        for hero in self.heros_membership:
            if self.heros_membership[hero] == 1:
                my_power += heros_pool[hero][1] * heros_pool[hero][2]
                if hero % 10 in my_last_digit:
                    my_synergy = 0
                else:
                    my_last_digit.append(hero % 10)
            elif self.heros_membership[hero] == 2:
                opponent_power += heros_pool[hero][1] * heros_pool[hero][3]
                if hero % 10 in opponent_last_digit:
                    opponent_senergy = 0
                else:
                    opponent_last_digit.append(hero % 10)
        
        return (my_synergy+my_power) - (opponent_senergy+opponent_power)

def Minmax(state):
    global heros_pool
    
    best_hero = None
    advantage = -float('inf')
    state_children = {}
    
    for hero_id in state.heros_membership:
        if state.heros_membership[hero_id] == 0:
            state_children[hero_id] = state.next_state(hero_id)
            
    for hero_id in state_children:
        new_advantage = Min_value(state_children[hero_id])
        if new_advantage > advantage or (new_advantage==advantage and hero_id<best_hero):
            advantage = new_advantage
            best_hero = hero_id

    return best_hero

def Max_value(state):
    global heros_pool
    
    if state.level >= 10:
        return state.cal_advantage(heros_pool)
    
    advantage = -float('inf')
    state_children = {}
    
    for hero_id in state.heros_membership:
        if state.heros_membership[hero_id] == 0:
            state_children[hero_id] = state.next_state(hero_id)
            
    for hero_id in state_children:
        new_advantage = Min_value(state_children[hero_id])
        advantage = max(advantage, new_advantage)
            
    return advantage

def Min_value(state):
    global heros_pool
    
    if state.level >= 10:
        return state.cal_advantage(heros_pool)
    
    advantage = float('inf')
    
    state_children = {}
    
    for hero_id in state.heros_membership:
        if state.heros_membership[hero_id] == 0:
            state_children[hero_id] = state.next_state(hero_id)

    for hero_id in state_children:
        new_advantage = Max_value(state_children[hero_id])
        advantage = min(advantage, new_advantage)

    return advantage

# Alpha_beta_pruning
def Alpha_beta_minmax(state):
    global heros_pool
    
    best_hero = None
    advantage = -float('inf')
    state_children = {}
    
    for hero_id in state.heros_membership:
        if state.heros_membership[hero_id] == 0:
            state_children[hero_id] = state.next_state(hero_id)
            
    for hero_id in state_children:
        new_advantage = Alpha_beta_min_value(state_children[hero_id], -float('inf'), float('inf'))
        if new_advantage > advantage or (new_advantage==advantage and hero_id<best_hero):
            advantage = new_advantage
            best_hero = hero_id

    return best_hero


def Alpha_beta_max_value(state, alpha, beta):
    global heros_pool
    
    if state.level >= 10:
        return state.cal_advantage(heros_pool)
    
    advantage = -float('inf')
    state_children = {}
    
    for hero_id in state.heros_membership:
        if state.heros_membership[hero_id] == 0:
            state_children[hero_id] = state.next_state(hero_id)
            
    for hero_id in state_children:
        new_advantage = Alpha_beta_min_value(state_children[hero_id], alpha, beta)
        advantage = max(advantage, new_advantage)
        if advantage >= beta:
            return advantage
        alpha = max(alpha, advantage)
            
    return advantage

def Alpha_beta_min_value(state, alpha, beta):
    global heros_pool
    
    if state.level >= 10:
        return state.cal_advantage(heros_pool)
    
    advantage = float('inf')
    
    state_children = {}
    
    for hero_id in state.heros_membership:
        if state.heros_membership[hero_id] == 0:
            state_children[hero_id] = state.next_state(hero_id)

    for hero_id in state_children:
        new_advantage = Alpha_beta_max_value(state_children[hero_id], alpha, beta)
        advantage = min(advantage, new_advantage)
        if advantage <= alpha:
            return advantage
        beta = min(beta, advantage)

    return advantage


if __name__== "__main__":
    filename = "input"
    algorithm, initial_level, heros_pool, membership = Read_file(filename)
    initial_state = State(initial_level,1,membership)

    if algorithm == "ab":
        best_hero = Alpha_beta_minmax(initial_state)
    elif algorithm == "minimax":
        best_hero = Minmax(initial_state)
    
    Write_output(best_hero)

