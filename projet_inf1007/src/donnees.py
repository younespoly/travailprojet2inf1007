def dose_moyenne(doses):
    total = 0
    for i in range(1, len(doses)):
        total = total + doses[i]
    return total / len(doses)

