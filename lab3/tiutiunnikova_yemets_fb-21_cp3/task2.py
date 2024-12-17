def bi_calc(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()    
    bi_count = {}
    total_bis = 0

    for i in range(0, len(text) - 1):
        bi = text[i:i+2]
        if len(bi) == 2:
            if bi in bi_count:
                bi_count[bi] += 1
            else:
                bi_count[bi] = 1
            total_bis += 1
            
    bi_fr = {bi: cnt / total_bis for bi, cnt in bi_count.items()}
    bis_5 = sorted(bi_fr.items(), key=lambda x: x[1], reverse=True)[:5]
    return bi_fr, bis_5

filename = '05.txt'
bi_fr, bis_5 = bi_calc(filename)

print("Частоти 5 найпоширеніших біграм:")
for bigram, freq in bis_5:
    print(f"'{bigram}': {freq:.2%}")
