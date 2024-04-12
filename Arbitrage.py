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
            for k in range(len(tokens) - 1):
                if k == i or k ==j or k ==base_Token:
                    continue
                R0, R1 = liquidity[base_Token][i]
                R_1, R2 = liquidity[i][j]
                R_2, R3 = liquidity[j][k]
                R_3, R_0 = liquidity[k][base_Token]
                M0 = R0*R_1/(R_1+R1*0.997)
                M2 = 0.997*R1*R2/(R_1+R1*0.997)
                M_2 = R2*R3/(R_3+R3*0.997)
                M_0 = 0.997*R3*R_0/(R_3+R3*0.997)
                E_before = M0*M_2/(M2+M_2*0.997)
                E_after = 0.997*M2*M_0/(M2+M_2*0.997)
                amount = (E_before*E_after*0.997)**0.5-E_before
                if E_after>E_before and amount >1:
                    return (i,j,k,amount)
    for i in range(len(tokens) - 1):
        if i == base_Token:
            continue
        for j in range(len(tokens) - 1):
            if j == i or j == base_Token:
                continue
            R0, R1 = liquidity[base_Token][i]
            R_1, R2 = liquidity[i][j]
            R_2, R_0 = liquidity[j][base_Token]
            M0 = R0*R_1/(R_1+R1*0.997)
            M2 = 0.997*R1*R2/(R_1+R1*0.997)
            E_before = M0*R_2/(M2+R_2*0.997)
            E_after = 0.997*M2*R_0/(M2+R_2*0.997)
            amount = (E_before*E_after*0.997)**0.5-E_before
            if E_after>E_before and amount >1:
                return (i,j,amount)
    return (-1,-1)


def trade(liquidity, amount, M1, M2):
    ##print(amount, M1, M2)
    amount_M1, amount_M2 = liquidity[M1][M2]
    amount_aM2 = amount_M1*amount_M2/(amount_M1+amount)
    liquidity[M1][M2]= (amount_M1+amount, amount_aM2)
    liquidity[M2][M1]= (amount_aM2, amount_M1+amount)
    amount = amount_M2-amount_aM2
    return amount

def arbitrage(liquidity, amount, base_Token, M1, M2, M3):
    ##print(f"input:{amount}")
    amount = trade(liquidity, amount, base_Token, M1)
    ##print(f"M1:{amount}")
    amount = trade(liquidity, amount, M1, M2)
    ##print(f"M2:{amount}")
    if M3 == -1:
        amount = trade(liquidity, amount, M2, base_Token)
        ##print(f"output:{amount}")
        return amount
    amount = trade(liquidity, amount, M2, M3)
    ##print(f"M3:{amount}")
    amount = trade(liquidity, amount, M3, base_Token)
    ##print(f"output:{amount}")
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
    while(amount_In<20.5):
        result = checkforArbitrage(liquidity, tokens, base_Token)
        if result == (-1, -1):
            print("fail")
            return amount_In, path
        if len(result)==4:
            M1, M2, M3, amount = result
            ##print(M1,M2,M3,f"amountIn={amount}")
            path.append([M1,M2,M3,amount]) 
            amount_In -= amount
            ##print(f"amountIn={amount}")
            amount = arbitrage(liquidity, amount, base_Token, M1, M2, M3)
            amount_In += amount
        if len(result)==3:
            M1, M2, amount = result
            path.append([M1,M2,amount])
            ##print(M1,M2,f"amountIn={amount}") 
            amount = min(amount, amount_In)
            amount_In -= amount
            amount = arbitrage(liquidity, amount, base_Token, M1, M2, -1)
            amount_In += amount
    return amount_In, path
    

# Construct the graph from the liquidity dictionary
graph = [(token1, token2, liquidity[(token1, token2)]) for (token1, token2) in liquidity]
# Find the profitable path starting from tokenB
result,path = Arbitrage(graph, "tokenB")
print("path: ", end=" ")
for i in range(len(path)):
    print("tokenB->",end=" ")
    for j in range(len(path[i])-1):
        print(tokens[path[i][j]], end=" ")
        print("->", end=" ")
print(f"tokenB, tokenB balance={result}")