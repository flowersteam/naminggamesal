import json
import os
import copy

def export_agent_past(xp,agent_number=0,file=None):
    if file is None:
        filename = xp.uuid+'.json'
    else:
        filename = file+'.json'
    if not os.path.exists('json_data'):
        os.makedirs('json_data')
    with open('json_data/'+filename,'w') as f:
        try:
            f.write(json.dumps(xp._poplist.get_last()._agentlist[agent_number]._memory['past_interactions_all']))
        except TypeError:
            new_dict_list = copy.deepcopy(xp._poplist.get_last()._agentlist[agent_number]._memory['past_interactions_all'])
            for elt in new_dict_list:
                for k in elt.keys():
                    elt[k] = str(elt[k])
            f.write(json.dumps(new_dict_list))