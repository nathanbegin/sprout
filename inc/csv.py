
def load_csv(myfile, header=True):
    """
    loads a CSV to a dict of dict
    """
    import collections
    with open(myfile, "r") as f:
        r = 0
        ret = collections.defaultdict(collections.OrderedDict)
        for row in f.readlines():
            if r == 0 and header is True:
                keys = list(map(lambda x: x.strip("\n"), row.split(",")))
                r = -1
                header = False
            else:
                rsplit = row.split(",")
                for i, k in enumerate(keys):
                    ret[r][k] = rsplit[i].strip("\n")

            r += 1

    return ret

def load_csv2(myfile, header=True):
    """
    loads a CSV to a dict of dict
    """
    import collections
    with open(myfile, "r") as f:
        r = 0
        ret = collections.defaultdict(list)
        for row in f.readlines():
            if r == 0 and header is True:
                keys = list(map(lambda x: x.strip("\n"), row.split(",")))
                r = -1
                header = False
            else:
                rsplit = row.split(",")
                for i, k in enumerate(keys):
                    ret[k].append(rsplit[i].strip("\n"))

            r += 1

    return ret

def save_csv(filename, d, header=True):
    if header:
        hrow = []

        for k in d[0].keys():
            hrow.append(str(k))

        with open(filename, 'w') as f:
            f.write(",".join(hrow) + "\n")

    for row in d:
        newrow = []

        for k in d[row].keys():
            newrow.append(str(d[row][k]))

        with open(filename, 'a+') as f:
            f.write(",".join(newrow) + "\n")