def sortedUniforms(N):
    """yields N iid uniforms [0.0, 1.0), sorted in ascending order. 
    Note: for most practical purposes, it might be faster to generate N uniforms and sort them.
    Source: http://repository.cmu.edu/cgi/viewcontent.cgi?article=3483&context=compsci
    """
    currentMax = 1.0
    for k in range(N,0,-1):
        currentMax *= (1-random.random())**(1.0/k)
        yield 1.0-currentMax