def findComponents(V, E):
    # zgradi slovar sosedov
    neighbors = {}
    for v in V:
        neighbors[v] = set([])

    for (e1, e2) in E:
        neighbors[e1].add(e2)
        neighbors[e2].add(e1)

    visited = set([])  # visited je set ze obiskanih vozlisc
    components = []  # v components shranimo ze najdene komponente
    for v in V:
        if v not in visited:
            visited.add(v)
            components.append(dfs(v, neighbors, visited))

    return components


# rekurzivno vrne se neobiskana vozlisca iz iste komponente kot je podano vozlisce
def dfs(v, neighbors, visited):
    ret = [v]
    for u in neighbors[v]:
        if u not in visited:
            visited.add(u)
            ret += dfs(u, neighbors, visited)

    return ret