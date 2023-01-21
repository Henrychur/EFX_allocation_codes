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
        self.valuation_table = valuation_table
        self.num_agents, self.num_goods = valuation_table.shape
        self.a, self.b = 2 * x, x
        self.unallocated_goods = [i for i in range(self.num_goods)]
        self.EFX_allocation = [[] for _ in range(self.num_agents)]
        
        # ------------------------ # 
        # Round-robin algorithm 
        # ------------------------ #
        for r in range(self.num_goods // self.num_agents):
            for agent in range(self.num_agents):
                # find the good that agent value it most
                max_value, prefered_good = -1, -1
                for good in self.unallocated_goods:
                    if self.valuation_table[agent, good] > max_value:
                        max_value, prefered_good = self.valuation_table[agent, good], good
                # allocate the good
                self.EFX_allocation[agent].append(prefered_good)
                self.unallocated_goods.remove(prefered_good)

        for agent in range(self.num_goods % self.num_agents):
            # for the last round, we need to reverse the allocation order
            agent = self.num_agents - agent - 1
            # find the good that agent value it most
            max_value, prefered_good = -1, -1
            for good in self.unallocated_goods:
                if self.valuation_table[agent, good] > max_value:
                    max_value, prefered_good = self.valuation_table[agent, good], good
            # allocate the good
            self.EFX_allocation[agent].append(prefered_good)
            self.unallocated_goods.remove(prefered_good)
        return self.EFX_allocation