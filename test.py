file = './freqs/bernstein18a-supp.pdf.txt'

sum = 0.0
with open(file,'r') as f:
    line = f.readline()
    while line:
        tokens = line.split()
        word = tokens[0]
        prob = float(tokens[1])
        line = f.readline()
        sum += prob
print(sum)