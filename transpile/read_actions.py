with open("Actions.txt") as f:
    print(f)
    lines = f.readlines()
    trim_list = list(map(lambda line: line.strip(), lines))

    sig = "-- HERE --"
    sig_indx = trim_list.index(sig)

    pure_inst = trim_list[sig_indx:]
    print(pure_inst)
    res = []
    for p in pure_inst:
        split = p.split(" ", 1)
        if split[0].isdigit():
            res.append(split[1])
    print(res)
