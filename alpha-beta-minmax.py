
# coding: utf-8

# In[1]:


# Import file
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
    return initial_level, heros_pool, heros_membership

def Write_output(best_hero):
    output_file = open("output.txt","w")
    output_file.write(str(best_hero))
    output_file.close()


# In[2]:


import copy

class State:
    def __init__(self, level, player, heros_membership):
        self.level = level
        self.player = player
        self.heros_membership = heros_membership

    def next_state(self, hero_id):
        next_state = copy.deepcopy(self)
        if next_state.player == 1:
            next_state.heros_membership[hero_id] = 1
        else:
            next_state.heros_membership[hero_id] = 2
        next_state.level += 1
        next_state.player = -next_state.player
        return next_state
    
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


# In[3]:


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


# In[4]:


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
        if new_advantage > advantage:
            advantage = new_advantage
        if advantage >= beta:
            return advantage
        alpha = max(alpha, advantage)
            
    return advantage


# In[5]:


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
        if new_advantage < advantage:
            advantage = new_advantage
        if advantage <= alpha:
            return advantage
        beta = min(beta, advantage)

    return advantage


# In[17]:


if __name__== "__main__":
    import time
    start_time = time.time()
    filename = "test_case/input8"
    initial_level, heros_pool, membership = Read_file(filename)
    initial_state = State(initial_level,1,membership)
    
    best_hero = Alpha_beta_minmax(initial_state)
    Write_output(best_hero)
    
    print best_hero
    print time.time()-start_time, "seconds"

