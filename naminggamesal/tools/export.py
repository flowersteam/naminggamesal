import json
import os
import copy

from ..ngvoc import get_vocabulary
from ..ngpop import Population

def export_agent_past(xp,agent_number=0,file=None):
    if file is None:
        filename = xp.uuid+'.json'
    else:
        filename = file+'.json'
    if not os.path.exists('json_data'):
        os.makedirs('json_data')
    with open('json_data/'+filename,'w') as f:
        f.write(json.dumps(xp._poplist.get_last()._agentlist[agent_number]._memory['past_interactions_all']))

def get_agent_past(xp,agent_number=0):
    return xp._poplist.get_last()._agentlist[agent_number]._memory['past_interactions_all']

def reconstruct_ag(past_interactions,pop_cfg,replace_words=False):
    cfg = copy.deepcopy(pop_cfg)
    cfg['nbagent'] = 1
    pop = Population(**cfg)
    ag = pop._agentlist[0]
    if replace_words:
        pi_l = copy.deepcopy(past_interactions)
        w_l = set()
        for pi in pi_l:
            w_l.add(pi['w'])
        w_d = {w1:w2 for w1,w2 in zip(list(w_l),ag._vocabulary.accessible_words)}
        for pi in pi_l:
            pi['w'] = w_d[pi['w']]
    else:
        pi_l = past_interactions
    for pi in pi_l:
        ag.update_agent(**pi)
    return ag
