# José Lucas Sousa - 93019
# Francisca Barros - 93102
# Carolina Araújo - 93248
# Margarida Martins - 93169

from tree_search import *
from cidades import *
from strips import *

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth'): 
        super().__init__(problem,strategy)
        self.root = MyNode(problem.initial, None, 0, 0)
        self.open_nodes = [self.root]
        self.offsets_per_depth = {}
        self.to_goal = None
        self.from_init = None

    def hybrid1_add_to_open(self,lnewnodes):
        # Para cada node do lnewnode insere no início se estiver num index par, se não mete no fim 
        [self.open_nodes.insert(0, node) if index % 2 == 0 else self.open_nodes.extend([node]) for index,node in enumerate(lnewnodes)]

        # OU
        # Típico ciclo for 
        # i = 0
        # for node in lnewnodes:
        #     if i%2==0:
        #         self.open_nodes.insert(0, node)
        #     else:
        #         self.open_nodes.extend([node])

    def hybrid2_add_to_open(self,lnewnodes):
        # adiciona ao fim do open_nodes
        self.open_nodes.extend(lnewnodes)
        # e dá sort pelo depth - offset
        self.open_nodes.sort(key=lambda node: node.depth - node.offset)

    def search2(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)

            if self.problem.goal_test(node.state):
                self.terminal = len(self.open_nodes)+1
                self.solution = node
                return self.get_path(node)

            self.non_terminal+=1

            node.children = []

            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    
                    if self.offsets_per_depth.get(node.depth + 1):
                        offset = self.offsets_per_depth.get(node.depth + 1)
                    else:
                        self.offsets_per_depth[node.depth + 1], offset = 0, 0

                    newnode = MyNode(newstate,
                        node, 
                        node.depth + 1, 
                        offset
                    )

                    self.offsets_per_depth[node.depth + 1] +=1
                    node.children.append(newnode)
            
            self.add_to_open(node.children)

        return None


    def search_from_middle(self):

        # Calcula a cidade intermédia entre incial e a goal
        middle = self.problem.domain.middle(self.problem.initial, self.problem.goal)

        # Previne não encontrar o middle
        if not middle: 
            return self.search2()

        # Dividir o problema em dois:
        # Calcula da cidade inicial -> intermédia
        self.from_init = MyTree(SearchProblem(self.problem.domain, self.problem.initial, middle), self.strategy)
        solve1 = self.from_init.search2()

        # Calcula da intermédia -> cidade goal
        self.to_goal = MyTree(SearchProblem(self.problem.domain, middle, self.problem.goal), self.strategy)
        solve2 = self.to_goal.search2()

        # Concatena e corta de uma das listas a cidade intermédia se não ficava repetida
        return solve1[:-1] + solve2 
        
class MyNode(SearchNode):
    def __init__(self,state, parent, depth, offset): 
        super().__init__(state, parent)
        self.depth = depth
        self.offset = offset
    
class MinhasCidades(Cidades):
    # state that minimizes heuristic(state1,middle) + heuristic(middle,state2) 
    def middle(self, city1, city2):
        # o min() recebe como argumento uma função que lhe diz porque valores ordenar (que é, neste caso, a heuristica somada)
        return min([st for st in self.coordinates if st != city1 and st != city2], key=lambda st: self.heuristic(city1, st) + self.heuristic(st, city2))
        
class MySTRIPS(STRIPS):
    def result(self, state, action):
        
        if not all(p in state for p in action.pc): return None
        
        newstate = [p for p in state if p not in action.neg]
        newstate.extend(action.pos)
        
        return newstate

        # OU
        # Como não tenho ideia de qual é a solução mais elegante/eficiente, deixo em comentário a minha adaptação com filter da versão acima do professor Diogo que foi feita numa aula prática
        # Talvez o filter seja menos legível
        #
        # if not all([pc in state for pc  in action.pc]): 
        #     return None
        # state = list(filter(lambda state: state not in action.neg, state))
        # state.extend(action.pos)
        # return state

    def sort(self,state):
        state.sort(key=lambda st: str(st))
        return state
        
        # OU 
        # Se quisermos numa linha poderá ser este o return, mas como temos que iterar os estados com uma list comprehension considero a solução acima mais eficiente
        # return sorted([st for st in state], key=lambda st: str(st))



