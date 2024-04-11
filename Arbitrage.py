liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}
tokens = ["tokenA", "tokenB", "tokenC", "tokenD", "tokenE"]
path=[]
def checkforArbitrage(liquidity, tokens, base_Token):
    for i in range(len(tokens) - 1):
        if i == base_Token:
            continue
        for j in range(len(tokens) - 1):
            if j == i or j == base_Token:
                continue
            R0, R1 = liquidity[base_Token][i]
            R_1, R2 = liquidity[i][j]
            M0 = R0*R_1/(R_1+R1)
            M2 = R1*R2/(R_1+R1)
            R_2, R_0 = liquidity[j][1]
            E_before = M0*R_2/(M2+R_2)
            E_after = M2*R_0/(M2+R_2)
            amount = (E_before*E_after)**0.5-E_before
            if E_after>E_before and amount >0.5:
                return (i,j,amount)
    return (-1,-1);

def trade(liquidity, amount, M1, M2):
    ##print(amount, M1, M2)
    amount_M1, amount_M2 = liquidity[M1][M2]
    amount_aM2 = amount_M1*amount_M2/(amount_M1+amount)
    liquidity[M1][M2]= (amount_M1+amount, amount_aM2)
    liquidity[M2][M1]= (amount_aM2, amount_M1+amount)
    amount = amount_M2-amount_aM2
    return amount

def arbitrage(liquidity, amount, base_Token, M1, M2):
    amount = trade(liquidity, amount, base_Token, M1)
    amount = trade(liquidity, amount, M1, M2)
    amount = trade(liquidity, amount, M2, base_Token)
    return amount

def Arbitrage(graph, start):
    # Initialize liquidity pool
    amount_In = 5
    tokens = ["tokenA", "tokenB", "tokenC", "tokenD", "tokenE"]
    liquidity = [[() for _ in range(len(tokens))] for _ in range(len(tokens))]
    base_Token = tokens.index(start)
    # Fill the 2D array with the tuples from the liquidity dictionary
    for token1, token2, (a_1, a_2) in graph:
        liquidity[tokens.index(token1)][tokens.index(token2)] = (a_1, a_2)
        liquidity[tokens.index(token2)][tokens.index(token1)] = (a_2, a_1)
    # Relax edges repeatedly
    while(amount_In<20):
        result = checkforArbitrage(liquidity, tokens, base_Token)
        if result == (-1, -1):
            print("fail")
            return amount_In
        else:
            M1, M2, amount = result
        path.append([M1,M2,amount]) 
        amount = min(amount, amount_In)
        amount_In -= amount
        amount = arbitrage(liquidity, amount, base_Token, M1, M2)
        amount_In += amount
    return amount_In, path
    

# Construct the graph from the liquidity dictionary
graph = [(token1, token2, liquidity[(token1, token2)]) for (token1, token2) in liquidity]
# Find the profitable path starting from tokenB
result,path = Arbitrage(graph, "tokenB")
for i in range(len(path)-1):
    print("tokenB->",end=" ")
    for j in range(len(path[i])-1):
        print(tokens[path[i][j]], end=" ")
        print("->", end=" ")
print(f"tokenB, tokenB balance={result}")