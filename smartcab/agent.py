import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
       

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.availableAction = [None, 'forward', 'left', 'right']   
        self.lastReward      = 0
        self.lastAction      = None
        self.lastWaypoint    = None
        self.next_waypoint   = None

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        print "----------------------------------------------------------"
        print"RESET, Final state:\n", self.state
        print "----------------------------------------------------------"

    def update(self, t):
        # Gather inputs
        self.lastWaypoint = self.next_waypoint
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state=(deadline, inputs,self.next_waypoint,self.lastAction, self.lastWaypoint, self.lastReward)
          
        # TODO: Select action according to your policy

        if self.lastReward <0:
            action = self.availableAction[random.randint(0,3)]
        else:
            action = self.next_waypoint
            
        self.lastAction=action
    
        # Execute action and get reward
        reward = self.env.act(self, action)
        self.lastReward=reward
        # TODO: Learn policy based on state, action, reward

        print "LearningAgent.update(): self.state{}, action = {}, reward = {}, next_waypoint = {}".format(self.state, action, reward,self.next_waypoint, )  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
