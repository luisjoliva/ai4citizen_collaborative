import json, copy

def simple_interaction(state_of_the_world, basic_feedback):
    ''' We remove those assignments whose students have all accepted it. '''
    res = copy.deepcopy(state_of_the_world)
    feedback = json.loads(basic_feedback)
    accepted = feedback['accepted']
    for project in state_of_the_world:
        people = state_of_the_world[project]
        if(all(x in accepted for x in people)):
            del(res[project])
    return res



def is_assigned(person, project, state_of_the_world):
    ''' Returns if person is assigned to a given project in given state_of_the_world'''
    return person in state_of_the_world[project]