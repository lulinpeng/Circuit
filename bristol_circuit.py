class BristolCircuit: 
    ''' refer to https://nigelsmart.github.io/MPC-Circuits/ '''
    circuit_file:str # circuit file path
    n:int = 0 # number of total gates
    m:int = 0 # number of total wires (including input wires)
    niv:int = 0 # number of input variables
    niv_wires:list = [] # array of numbers of wires of each input variables 
    nov:int = 0 # number of output variables
    nov_wires:list = [] # array of numbers of wires of each output variables 
    circuit:list = [] # gates sequence
    def __init__(self, circuit_file:str):
        self.circuit_file = circuit_file
        return
    
    def load_circuit(self):
        with open(self.circuit_file) as f: 
            lines = f.readlines()
            self.circuit = lines[4:]
            self.n = eval(lines[0].split()[0])
            self.m = eval(lines[0].split()[0])
            self.niv = eval(lines[1].split()[0])
            for i in range(self.niv):
                self.niv_wires.append(eval(lines[1].split()[1+i]))
                self.m += self.niv_wires[i]
            self.nov = eval(lines[2].split()[0])
            for i in range(self.nov):
                self.nov_wires.append(eval(lines[2].split()[1+i]))
        return
    
    def brief(self):
        print(f'#(total gates) = {self.n}\n#(total wires) = {self.m}')
        print(f'#(input variables) = {self.niv}, bit length of each vairable {self.niv_wires}')
        print(f'#(output variables) = {self.nov}, bit length of each variable {self.nov_wires}')
        return
    
    def execute_circuit(self, circuit_input:list):
        # create wires
        wires = [False] * self.m # store all wire values (input, internal and output)
        
        # set input wires
        wires[:len(circuit_input)] = circuit_input

        # execute the circuit
        for i in range(self.n):
            r = self.circuit[i].split()
            gate = r[-1]
            if gate not in {'AND', 'XOR', 'INV'}:
                raise 'unexpected gate appears: ' + gate
            elif gate == 'INV':
                in_id = eval(r[2]) # input wire id
                out_id = eval(r[3]) # output wire id
                wires[out_id] = not wires[in_id] # compute
            elif gate == 'AND':
                in0_id = eval(r[2]) # input wire id
                in1_id = eval(r[3]) # input wire id
                out_id = eval(r[4]) # output wire id
                wires[out_id] = wires[in0_id] and wires[in1_id] # compute
            elif gate == 'XOR':
                in0_id = eval(r[2]) # input wire id
                in1_id = eval(r[3]) # input wire id
                out_id = eval(r[4]) # output wire id
                wires[out_id] = wires[in0_id] ^ wires[in1_id] # compute

        num_of_circuit_output_wires = sum(self.nov_wires)
        circuit_output = wires[-num_of_circuit_output_wires:]
        
        return circuit_output

def bools_to_bins(bools:list):
    out = ''
    for v in bools:
        out += str(int(v))
    return out

if __name__ == '__main__':
    circuit = BristolCircuit('aes_128.txt')
    circuit.load_circuit()

    circuit.brief()

    aes_key = [False] * 128 # aes key as 000...0
    aes_msg = [True] * 128  # aes msg as 111...1
    circuit_input = aes_key + aes_msg
    print(f'circuit input: {bools_to_bins(circuit_input)}')

    circuit_output = circuit.execute_circuit(circuit_input)
    print(f'circuit output: {bools_to_bins(circuit_output)}')
