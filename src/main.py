import pandas as pd
from datetime import datetime

from read_input import read_input
from tabu_list import algorithm

if __name__ == '__main__':
    test_data = pd.DataFrame(columns=['caso','tenure','max_iter','sol_ini','iter_sem_mod','tempo','custo', 'gap'])

    files = [ # A-nX-kY.vrp
             "A-n32-k5.vrp",
             "A-n54-k7.vrp",
             "A-n80-k10.vrp",

            #  # B-nX-kY.vrp
             "B-n31-k5.vrp",
             "B-n43-k6.vrp",
             "B-n68-k9.vrp",

            #  # F-nX-kY.vrp
             "F-n45-k4.vrp",
             "F-n72-k4.vrp",
             "F-n135-k7.vrp"
             ]
    
    opt = [# A-nX-kY.vrp
           784, 
           1167,
           1763,
           # B-nX-kY.vrp
           672,
           742,
           1272,
           # F-nX-kY.vrp 
           724,
           237, 
           1162
          ]
             

    print("Inicio do log:", datetime.now(), end='\n\n')
    for index_opt, file in enumerate(files):
        nodes, vehicles, clients, vehicle_capacity = read_input(f'input/{file}')
        tenure = [5, 10, 15, 25]
        num_iteration = [10, 100, 500, 1000]
        initial = [True, False]
        
        if int(clients/2) not in tenure:
            tenure.append(int(clients/2))


        for solution in initial:
            
            for t in tenure:

                for iter_ in num_iteration:

                    for i in range(5):
                        # Log message
                        print("*"*30)
                        print(f"Caso:{file} | Teste #{i + 1}")

                        if solution == True:
                            print('Solução inicial: Savings', end=" | ")
                        else:
                            print('Solução inicial: Aleatório', end=" | ")
                
                        print(f"Tenure: {t}", end=" | ")
                        print(f'Max iter: {iter_}', end='\n\n')

                        if solution:
                            aux_sol = 'Savings'
                        else:
                            aux_sol = 'Random'

                        tempo, alg_iter, best_sol_dist = algorithm(nodes, vehicles, clients, vehicle_capacity, t, iter_, solution)
                        
                        aux_data = {
                            'caso': file,
                            'tenure': t,
                            'max_iter': iter_,
                            'sol_ini': aux_sol,
                            'iter_sem_mod': alg_iter,
                            'tempo': tempo,
                            'custo': best_sol_dist,
                            'gap': round(((best_sol_dist - opt[index_opt]) / opt[index_opt]), 6)
                        }

                        test_data = test_data.append(aux_data, ignore_index=True)
                        print(f"Tempo: {round(tempo, 2)}s | Iter sem mudanças: {alg_iter} | Custo: {best_sol_dist} | Gap: {round(((best_sol_dist - opt[index_opt]) / opt[index_opt]), 6)}", end='\n\n')
    
    test_data.to_csv('log/teste1.csv', index_label='num_teste')    
    print("Fim do log:", datetime.now(), end='\n\n')
    