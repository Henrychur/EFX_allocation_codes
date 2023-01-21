"""
@Description :   We show that EFX allocations exist for interval-instances in which 
                 the values of each agent i are in some interval [xi, 2xi], xi ∈ R>0, 
                 by using a simple modification of the round-robin algorithm.
@Author      :   Henrychur 
@Time        :   2023/01/20 21:21:30
"""
import numpy as np

class ModifiedRoundRobin():
    def __init__(self):
        '''
        @Description :   Modified round-robin algorithm for solving the EFX allocation problem with
                         the values of each agent i in the range of [xi, 2xi].
        '''
        self.a, self.b = None, None # a, b are 2 value and a = 2b
        self.unallocated_goods = None # unallocated goods
        self.valuation_table = None # valuation table
        self.num_agents, self.num_goods = None, None
        self.ordered_list_of_agent = None # ordered list of agent
        self.EFX_allocation = None # match result

    def solve(self, valuation_table, x):
        '''
        @Description :   solve the interval-value with [x, 2x] EFX allocation.
        @Param       :   valuation_table - valuation table
        @Return      :   EFX_allocation - EFX allocation
        '''
        # ------------------------ #
        # init the parameters
        # ------------------------ #
        self.valuation_table = valuation_table
        self.num_agents, self.num_goods = valuation_table.shape
        self.a, self.b = 2 * x, x
        self.unallocated_goods = [i for i in range(self.num_goods)]
        self.EFX_allocation = [[] for _ in range(self.num_agents)]
        
        # ------------------------ # 
        # Round-robin algorithm 
        # ------------------------ #
        # for the complete rounds, we allocate the good to the agent in order
        for r in range(self.num_goods // self.num_agents):
            for agent in range(self.num_agents):
                self.allocate_agent_preferred_good(agent)

        # for the goods left, we allocate the good to the agent in reverse order
        for agent in range(self.num_goods % self.num_agents):
            # reverse the allocation order
            agent = self.num_agents - agent - 1
            self.allocate_agent_preferred_good(agent)
        return self.EFX_allocation

    def allocate_agent_preferred_good(self, agent):
        '''
        @Description :   allocate the agent preferred good.
        @Param       :   agent - agent index
        @Return      :   None
        '''
        # find the good that agent value it most
        max_value, prefered_good = -1, -1
        for good in self.unallocated_goods:
            if self.valuation_table[agent, good] > max_value:
                max_value, prefered_good = self.valuation_table[agent, good], good
        # allocate the good
        self.EFX_allocation[agent].append(prefered_good)
        self.unallocated_goods.remove(prefered_good)