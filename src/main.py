import pandas as pd
from datetime import datetime
import os.path


from read_input import read_input
from tabu_list import algorithm

TEST = 2

if __name__ == '__main__':
    
    # Arquivo existe
    if os.path.isfile(f'log/teste{TEST}.csv'):
        test_data = pd.read_csv(f'log/teste{TEST}.csv', index_col=0)
    else:
        test_data = pd.DataFrame(columns=['caso','tenure','max_iter','sol_ini','iter_sem_mod','tempo','custo', 'gap'])
    
    file_writer = open(f'log/teste{TEST}.txt', 'w')

    files = [ # A-nX-kY.vrp
             "A-n32-k5.vrp",
             "A-n54-k7.vrp",
             "A-n80-k10.vrp",

             # B-nX-kY.vrp
             "B-n31-k5.vrp",
             "B-n43-k6.vrp",
             "B-n68-k9.vrp",

             # F-nX-kY.vrp
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
             

    file_writer.write(f"Inicio do log: {datetime.now()}\n\n")

    num_testes = 5
    border = "*"*30 + "\n"
    for index_opt, file in enumerate(files):
        nodes, vehicles, clients, vehicle_capacity = read_input(f'input/{file}')
        tenure = [5, 15, 25, 45]
        num_iteration = [10, 100, 500]
        initial = [True, False]


        for solution in initial:
            
            for t in tenure:

                for iter_ in num_iteration:

                    for i in range(num_testes):
                        # Log message
                        file_writer.write(border)
                        file_writer.write(f"Caso:{file} | Teste #{i + 1}\n")
                        
                        header1 = ""
                        if solution == True:
                            header1 += 'Solucao inicial: Savings | '
                        else:
                            header1 += 'Solucao inicial: Aleatorio | '
                
                        header1 += f"Tenure: {t} | Max iter: {iter_}\n\n"
                        file_writer.write(header1)

                        if solution:
                            aux_sol = 'Savings'
                        else:
                            aux_sol = 'Random'

                        tempo, alg_iter, best_sol_dist = algorithm(nodes, vehicles, clients, vehicle_capacity, t, iter_max=iter_,savings=solution, file_writer=file_writer)

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
                        test_data.to_csv(f'log/teste{TEST}.csv', index_label='num_teste')
                        file_writer.write(f"Tempo: {round(tempo, 2)}s | Iter sem mudancas: {alg_iter} | Custo: {best_sol_dist} | Gap: {round(((best_sol_dist - opt[index_opt]) / opt[index_opt]), 6)}\n")
    
    file_writer.write(f"Fim do log: {datetime.now()}\n\n")
    file_writer.close()