import pandas as pd
from datetime import datetime
import os.path

from math import ceil

from read_input import read_input
from tabu_list import algorithm

TEST = 8

def get_files():
        return [ # A-nX-kY.vrp
            # "A-n33-k5.vrp",
            # "A-n33-k6.vrp",
            # "A-n34-k5.vrp",
            # "A-n36-k5.vrp",
            # "A-n37-k5.vrp",
            # "A-n37-k6.vrp",
            # "A-n38-k5.vrp",
            # "A-n39-k5.vrp",
            # "A-n39-k6.vrp",
            # "A-n44-k7.vrp",
            # "A-n45-k6.vrp",
            # "A-n45-k7.vrp",
            # "A-n46-k7.vrp",
            # "A-n48-k7.vrp",
            # "A-n53-k7.vrp",
            # "A-n55-k9.vrp",
            # "A-n60-k9.vrp",
            "A-n61-k9.vrp",
            "A-n62-k8.vrp",
            "A-n63-k10.vrp",
            "A-n63-k10.vrp",
            "A-n64-k9.vrp",
            "A-n65-k9.vrp",
            "A-n69-k9.vrp",

             # B-nX-kY.vrp
            "B-n34-k5.vrp",
            "B-n35-k5.vrp",
            "B-n38-k6.vrp",
            "B-n39-k5.vrp",
            "B-n41-k6.vrp",
            "B-n44-k7.vrp",
            "B-n45-k5.vrp",
            "B-n50-k8.vrp",
            "B-n51-k7.vrp",
            "B-n52-k7.vrp",
            "B-n56-k7.vrp",
            "B-n57-k7.vrp",
            "B-n57-k9.vrp",
            "B-n63-k10.vrp",
            "B-n64-k9.vrp",
            "B-n66-k9.vrp",
            "B-n67-k10.vrp"
    ]

if __name__ == '__main__':
    
    # Arquivo existe
    if os.path.isfile(f'log/teste{TEST}.csv'):
        test_data = pd.read_csv(f'log/teste{TEST}.csv', index_col=0)
    else:
        test_data = pd.DataFrame(columns=['caso','tenure','max_iter','sol_ini','iter_sem_mod','tempo','custo', 'gap'])
    
    file_writer = open(f'log/teste{TEST}.txt', 'w')

    files = get_files()

    file_writer.write(f"Inicio do log: {datetime.now()}\n\n")

    num_testes = 2
    border = "*"*30 + "\n"
    for index_opt, file in enumerate(files):
        nodes, vehicles, clients, vehicle_capacity, optimal = read_input(f'input/{file}')
        tenure = [ceil(clients * 1.2)]
        num_iteration = [500]
        initial = [True]

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
                            'gap': round(((best_sol_dist - optimal) / optimal), 6),
                            'otimo_global': optimal
                        }

                        test_data = test_data.append(aux_data, ignore_index=True)
                        test_data.to_csv(f'log/teste{TEST}.csv', index_label='num_teste')
                        file_writer.write(f"Tempo: {round(tempo, 2)}s | Iter sem mudancas: {alg_iter} | Custo: {best_sol_dist} | Gap: {round(((best_sol_dist - optimal) / optimal), 6)}\n")
    
    file_writer.write(f"Fim do log: {datetime.now()}\n\n")
    file_writer.close()