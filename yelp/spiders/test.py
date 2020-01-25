def test():
    for i in range(10):
        yield {"a":i}

    yield ["RRRrrrrr"]

print(list(test()))