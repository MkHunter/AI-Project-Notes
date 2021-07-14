Planteamiento
pseudo~peudocódigo de algoritmo A\*

    g(x)
    h(x)

    f(x) = g(x) + h(x)
    f(x) = estimated total cost of path

    Noxxo   = UNI al Oxxo + Distancia a catedral
    Nsimilares = UNI a similares + Distancia a catedral

    F(Noxxon,Nsimilares)

        NBena    =
        NEstadio =
        NParque =

    F(NBena,Nsimilares,NEstadio,NParque)

    Offspring = Expand(EA)
    Offspring = Evaluate(Offspring)
    Frontier  = Append(Frontier,Offspring)
    Frontier  = Sort(Frontier)

    A*(Frontier)
