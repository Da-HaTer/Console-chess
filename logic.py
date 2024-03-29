class Logic:
    def __init__(self, ):
        pass
    def valid_move(self,position, move):
        pass

    def valid_syntax(self,move):
        # room for improvement
        print(move,end=' ')
        move=move.removesuffix('+').removesuffix('#') #remove suffixes for now
        if move in ['O-O','O-O-O']:
            return True
        def square(pos):
            return len(pos)==2 and pos[0] in 'abcdefgh'  and pos[1] in '12345678'
        def prefix(move):
            if move[0] in 'abcdefghNBRQK': #example Nx** , dx**
                return True
            elif len(move)==2 and move[0] in 'NBRQK' and move[1] in 'abcdefgh12345678': #example Ndx** , N3x**
                return True
            elif len(move)==3 and move[0] in 'QKB' and square(move[1:3]): #example Qd3 , Kf7
                return True
            return False
        move=move.split('x')
        if len(move)==2:# a capture move 
            #first half
            if prefix(move[0]) and square(move[1]): #example Nxd4 , dxd4
                return True
            if prefix(move[0]) and square(move[1][:2]) and move[1][2]=='=' and move[1][3] in 'NBRQK': #example  dxd4=Q
                return True
        
        else: # a normal move
            if len(move[0])==2 and square(move[0]): #example e4
                return True
            elif len(move[0])==3 and move[0][0] in 'NBRQK' and square(move[0][1:]): #example Nf3
                return True
            elif len(move[0])==4 and move[0][0] in 'NBRQK' and move[0][1] in 'abcdefgh12345678' and square(move[0][2:]): #example N2f3, Ngf3
                return True
            elif len(move[0])==4 and square(move[0][:2]) and move[0][2]=="="and move[0][3] in 'NBRQK': #promotion move example e1=Q
                return True
            elif len(move[0])==5 and move[0][0] in "QBK" and square(move[0][1:3]) and square(move[0][-2:]):
                return True
        return False
    
    def check(self,position,turn):
        pass

if __name__ == "__main__":
    # Creating an instance of the class
    logic = Logic()
    print(logic.valid_syntax('e4'))
    print(logic.valid_syntax('O-O')) 
    print(logic.valid_syntax('O-O+')) 
    print(logic.valid_syntax('O-O#')) 
    print(logic.valid_syntax('Nf3')) 
    print(logic.valid_syntax('Ngf3'))
    print(logic.valid_syntax('N2f3'))
    print(logic.valid_syntax('Ngxf3'))  
    print(logic.valid_syntax('Nxf3'))  
    print(logic.valid_syntax('R3d3'))  
    print(logic.valid_syntax('e1=Q'))  
    print(logic.valid_syntax('e1=Q+'))  
    print(logic.valid_syntax('e1=Q#'))  
    print(logic.valid_syntax('Rdxf3'))  
    print(logic.valid_syntax('fxe1=Q+'))  
    print(logic.valid_syntax('Qe4f5+'))
    print(logic.valid_syntax('Qe4xf5+'))

    