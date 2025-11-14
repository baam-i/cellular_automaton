def sierpinski_rule90(n=32):
    size = 2*n+1
    row = [0]*size
    row[n] = 1  # initial cell on the center

    for _ in range(n):
        print("".join("█" if x else " " for x in row))
        new_row = [0]*size
        suma=0
        for i in range(1, size-1):
            actual = row[i]
            left = row[i-1]
            right = row[i+1]
            suma = left + actual + right
            if suma == 1: 
                new_row[i] = 1  # rule: exactly one
            else:
                new_row[i] = 0 

        row = new_row

sierpinski_rule90()
