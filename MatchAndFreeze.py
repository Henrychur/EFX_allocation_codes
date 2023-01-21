"""
@Description :   For any 2-value instance, Match&Freeze computes an EFX0 allocation in polynomial time.
@Author      :   Henrychur 
@Time        :   2023/01/20 17:03:20
"""
import numpy as np

class Hungary():
    def __init__(self):
        '''
        @Description :   Hungarian algorithm for solving the assignment problem with DFS.
        '''
        self.graph = None # bipartite graph(num_agents, num_goods)
        self.num_agents, self.num_goods = None, None
        self.match = None # match result, represent for a good's belonger
        self.visit = None # visit flag for dfs
    
    def solve(self, graph):
        '''
        @Description :   solve the bipartite match problem.
        @Param       :   graph - bipartite graph
        @Return      :   match - match result
        '''
        self.graph = np.array(graph)
        self.num_agents, self.num_goods = graph.shape
        self.match = np.zeros(self.num_goods, dtype=int) - 1
        for agent in range(self.num_agents):
            self.visit = np.zeros(self.num_goods, dtype=bool)
            self.__dfs(agent)
        return self.match

    def __dfs(self, agent):
        '''
        @Description :   dfs for finding augmenting path.
        @Param       :   agent - current agent
        @Return      :   bool - whether find a augmenting path
        '''
        for good in range(self.num_goods):
            if self.graph[agent, good] and not self.visit[good]:
                self.visit[good] = True
                if self.match[good] == -1 or self.dfs(self.match[good]):
                    self.match[good] = agent
                    return True
        return False


class MatchAndFreeze():
    def __init__(self):
        self.bipartiteMatching = Hungary()
        self.a, self.b = None, None # a, b are 2 value and a > b
        self.ab_ratio = None
        self.active_agents = None # active agents
        self.unallocated_goods = None # unallocated goods
        self.valuation_table = None # valuation table
        self.num_agents, self.num_goods = None, None
        self.ordered_list_of_agent = None # ordered list of agent
        self.EFX_allocation = None # match result

    def solve(self, valuation_table, a, b):
        '''
        @Description :   solve the 2-value EFX allocation.
        @Param       :   valuation_table - valuation table
        @Return      :   match - match result
        '''
        self.a, self.b = a, b
        self.ab_ratio = np.floor(a/b-1) if b > 0 else 9999999
        self.valuation_table = valuation_table
        self.num_agents, self.num_goods = valuation_table.shape
        self.active_agents = [i for i in range(self.num_agents)]
        self.unallocated_goods = [i for i in range(self.num_goods)]
        self.ordered_list_of_agent = [i for i in range(self.num_agents)]
        self.EFX_allocation = [[] for _ in range(self.num_agents)]
        self.freezed_agents = np.zeros(self.num_agents) - 1 # rounds that an agent is freezed

        while len(self.unallocated_goods) > 0:
            bipartite_graph = self.construct_bipartite_graph()
            match_results = self.bipartiteMatching.solve(bipartite_graph)
            
            round_allocated_good = [-1 for _ in range(len(self.active_agents))]
            # -------------------------------- # 
            # matched case
            # -------------------------------- # 
            tmp_allocated_goods = []
            candidate_agents = [0 for _ in range(len(self.active_agents))]
            for idx, match_result in enumerate(match_results):
                if match_result != -1:
                    # 由于match_result没有考虑agent的order，需要进行转换
                    candidate_agents[match_result] += 1
                    round_allocated_good[match_result] = self.unallocated_goods[idx]
                    self.EFX_allocation[self.ordered_list_of_agent[match_result]].append(self.unallocated_goods[idx])
                    tmp_allocated_goods.append(self.unallocated_goods[idx])
            # remove allocated goods
            self.unallocated_goods = [good for good in self.unallocated_goods if good not in tmp_allocated_goods]
            # -------------------------------- #
            # unmatched case
            # -------------------------------- #
            tmp_allocated_goods = []
            cnt = 0
            for idx, agent_flag in enumerate(candidate_agents):
                if agent_flag == 0:
                    if len(self.unallocated_goods) > cnt:
                        # no good match with the agent, allocated one arbitrary unallocated good
                        self.EFX_allocation[self.ordered_list_of_agent[idx]].append(self.unallocated_goods[cnt])
                        tmp_allocated_goods.append(self.unallocated_goods[cnt])
                        round_allocated_good[idx] = self.unallocated_goods[cnt]
                        cnt += 1
                    else:
                        return self.EFX_allocation
            # remove allocated goods
            self.unallocated_goods = [good for good in self.unallocated_goods if good not in tmp_allocated_goods]
            # -------------------------------- #
            # Construct the freeze set
            # -------------------------------- #
            for i in range(len(self.freezed_agents)):
                if self.freezed_agents[i] > -1 :
                    self.freezed_agents[i] -= 1
            
            round_freeze_list = []
            for i in range(len(self.active_agents)):
                freeze = False
                for j in range(len(self.active_agents)):
                    if i == j :
                        continue
                    if self.valuation_table[self.ordered_list_of_agent[j], round_allocated_good[i]] == self.a\
                        and self.valuation_table[self.ordered_list_of_agent[j], round_allocated_good[j]] == self.b:
                        freeze = True
                        break
                if freeze:
                    round_freeze_list.append(self.ordered_list_of_agent[i])
            
            for agent in round_freeze_list:
                self.active_agents.remove(agent)
                self.ordered_list_of_agent.remove(agent)
                self.freezed_agents[agent] = self.ab_ratio

            self.ordered_list_of_agent.extend(round_freeze_list)
            # -------------------------------- # 
            # recover the agent after freezed
            # -------------------------------- # 
            for agent, freeze_rounds in enumerate(self.freezed_agents):
                if freeze_rounds == 0:
                    self.active_agents.append(agent)
        return self.EFX_allocation

    def construct_bipartite_graph(self):
        '''
        @Description :   construct bipartite graph.
        @Param       :   None
        @Return      :   graph - bipartite graph
        '''
        graph = np.zeros((len(self.active_agents), len(self.unallocated_goods)))
        for agent in self.active_agents:
            for good in self.unallocated_goods:
                if self.valuation_table[agent, good] == self.a:
                    graph[agent, good] = 1
        return graph