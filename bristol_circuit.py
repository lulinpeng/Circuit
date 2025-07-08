class BristolCircuit: 
    ''' refer to https://nigelsmart.github.io/MPC-Circuits/ '''
    def __init__(self, circuit_file:str, circuit_name:str=None):
        print(f'circuit_file = {circuit_file}')
        self.circuit_file = circuit_file # circuit file path
        self.circuit_name = circuit_name # circuit name
        self.n = 0 # number of total gates
        self.m = 0 # number of total wires (including input wires)
        self.niv = 0 # number of input variables
        self.niv_wires = [] # array of numbers of wires of each input variables 
        self.nov = 0 # number of output variables
        self.nov_wires = [] # array of numbers of wires of each output variables 
        self.circuit = [] # gates sequence
        self.circuit_dag = None # Directed Acyclic Graph (DAG) of the circuit
        self.two_fan_in_gate = {'AND', 'XOR'}
        self.one_fan_in_gate = {'INV'}
        
        return
    
    def load_circuit(self):
        with open(self.circuit_file) as f: 
            lines = f.readlines()
            self.n = eval(lines[0].split()[0])
            self.m = eval(lines[0].split()[0])
            self.niv = eval(lines[1].split()[0])
            for i in range(self.niv):
                self.niv_wires.append(eval(lines[1].split()[1+i]))
                self.m += self.niv_wires[i]
            self.nov = eval(lines[2].split()[0])
            for i in range(self.nov):
                self.nov_wires.append(eval(lines[2].split()[1+i]))
            circuit_lines = lines[4:]
            self.circuit = [line.strip() for line in circuit_lines if line.strip() != '']
        return
    
    def load_circuit_as_dag(self):
        edges = []
        for gate in self.circuit:
            gate = gate.split()
            gate_type = gate[-1]
            if gate_type in self.one_fan_in_gate:
                gi_node = gate[2] # gate input node
                go_node = gate[3] # gate output node
                edges.append((gi_node, go_node))
            elif gate_type in self.two_fan_in_gate:
                gi_0_node = gate[2]
                gi_1_node = gate[3]
                go_node = gate[4]
                edges.append((gi_0_node, go_node))
                edges.append((gi_1_node, go_node))
            else:
                raise 'unexpected gate appears: ' + gate_type
        import networkx
        self.circuit_dag = networkx.DiGraph()
        self.circuit_dag.add_edges_from(edges)
        return
    
    def is_directed_acyclic_graph(self):
        import networkx
        return networkx.is_directed_acyclic_graph(self.circuit_dag)
    
    def brief(self):
        print(f'#(total gates) = {self.n}\n#(total wires) = {self.m}')
        print(f'#(input variables) = {self.niv}, bit length of each vairable {self.niv_wires}')
        print(f'#(output variables) = {self.nov}, bit length of each variable {self.nov_wires}')
        print(f'circuit depth = {self.depth()}')
        and_depth = self.depth('AND')
        print(f'circuit logic AND gate depth = {and_depth}')
        xor_depth = self.depth('XOR')
        print(f'circuit logic XOR gate depth = {xor_depth}')
        inv_depth = self.depth('INV')
        print(f'circuit logic INV gate depth = {inv_depth}')
        print()
        return
    
    def execute_circuit(self, circuit_input:list):
        # create wires
        wires = [False] * self.m # store all wire values (input, internal and output)
        
        # set input wires
        wires[:len(circuit_input)] = circuit_input

        # execute the circuit
        for gate in self.circuit:
            gate = gate.split()
            gate_type = gate[-1]
            if gate_type in self.one_fan_in_gate:
                in_id = eval(gate[2]) # input wire id
                out_id = eval(gate[3]) # output wire id
                if gate_type == 'INV':
                    wires[out_id] = not wires[in_id] # compute
                else:
                    raise 'unexpected gate appears: ' + gate_type
            elif gate_type in self.two_fan_in_gate:
                in0_id = eval(gate[2]) # input wire id
                in1_id = eval(gate[3]) # input wire id
                out_id = eval(gate[4]) # output wire id
                if gate_type == 'AND':
                    wires[out_id] = wires[in0_id] and wires[in1_id] # compute
                elif gate_type == 'XOR':
                    wires[out_id] = wires[in0_id] ^ wires[in1_id] # compute
                else:
                    raise 'unexpected gate appears: ' + gate_type
            else:
                raise 'unexpected gate appears: ' + gate_type

        num_of_circuit_output_wires = sum(self.nov_wires)
        circuit_output = wires[-num_of_circuit_output_wires:]
        
        return circuit_output
    
    # circuit gate depth
    def depth(self, specific_gate:str=None):
        depths = [0] * self.m
        for gate in self.circuit:
            gate = gate.split()
            gate_type = gate[-1]
            if gate_type in self.one_fan_in_gate:
                in_id = eval(gate[2]) # input wire id
                out_id = eval(gate[3]) # output wire id
                depths[out_id] = depths[in_id]
                if specific_gate == None or specific_gate == gate_type:
                    depths[out_id] += 1                 
            elif gate_type in self.two_fan_in_gate:
                in0_id = eval(gate[2]) # input wire id
                in1_id = eval(gate[3]) # input wire id
                out_id = eval(gate[4]) # output wire id
                depths[out_id] = max(depths[in0_id], depths[in1_id])
                if specific_gate == None or specific_gate == gate_type:
                    depths[out_id] += 1
        return max(depths)
    
    def draw_circuit(self, graph_file:str=None):
        graph = ''
        iv_node = 0 # input variable node
        for n in self.niv_wires:
            for j in range(n):
                graph += f'{iv_node} [shape=polygon, sides=4, label="IN", color="red"]\n'
                iv_node += 1

        for gate in self.circuit:
            gate = gate.strip().split()
            gate_type = gate[-1]
            if gate_type in self.one_fan_in_gate:
                gi_node = gate[2] # gate input node
                go_node = gate[3] # gate output node
                graph += f'{go_node} [shape=polygon, sides=4, label="{gate_type}", color="black"]\n'
                graph += f'{gi_node}->{go_node} [label = "{gi_node}"]\n'
            elif gate_type in self.two_fan_in_gate:
                gi_0_node = gate[2]
                gi_1_node = gate[3]
                go_node = gate[4]
                graph += f'{go_node} [shape=polygon, sides=4, label="{gate_type}", color="black"]\n'
                graph += f'{gi_0_node}->{go_node} [label = "{gi_0_node}"]\n'
                graph += f'{gi_1_node}->{go_node} [label = "{gi_1_node}"]\n'
            else:
                raise 'unexpected gate appears: ' + gate_type
        
        ov_node = self.m # output variable node
        offset = sum(self.nov_wires)
        for n in self.nov_wires:
            for j in range(n):
                graph += f'{ov_node} [shape=polygon, sides=4, label="OUT", color="blue"]\n'
                graph += f'{ov_node - offset} -> {ov_node} [label="{ov_node - offset}"]\n'
                ov_node += 1
        
        graph = 'digraph G {\n' + graph + '\n}'

        graph_file = 'graph.txt' if graph_file is None else graph_file
        graph_file = f'graph_{self.circuit_name}.txt' if graph_file == 'graph.txt' else graph_file
        with open('graph.txt', 'w') as f:
            f.write(graph)
        return

def bools_to_bins(bools:list):
    out = ''
    for v in bools:
        out += str(int(v))
    return out

if __name__ == '__main__':
    # aes-128 circuit
    circuit_file = 'circuits/aes_128.txt'
    circuit = BristolCircuit(circuit_file)
    circuit.load_circuit()
    circuit.brief()

    aes_key = [False] * 128 # aes key as 000...0
    aes_msg = [True] * 128  # aes msg as 111...1
    circuit_input = aes_key + aes_msg
    print(f'circuit input: {bools_to_bins(circuit_input)}')
    circuit_output = circuit.execute_circuit(circuit_input)
    print(f'circuit output: {bools_to_bins(circuit_output)}\n')

    # zero equal circuit
    circuit_file = 'circuits/zero_equal.txt'
    circuit = BristolCircuit(circuit_file, circuit_name='zero_equal')
    circuit.load_circuit()
    circuit.brief()
    circuit.draw_circuit()
    circuit.load_circuit_as_dag()
    print(f'Is the circuit a directed acyclic graph (DAG) ? {circuit.is_directed_acyclic_graph()}')
