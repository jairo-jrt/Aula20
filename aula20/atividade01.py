import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    print('\nObtendo dados...')
    
    link_dados = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(link_dados, sep=';', encoding= 'iso-8859-1')
    df_estelionato = df_ocorrencias[['mes_ano', 'estelionato']]
    df_estelionato = df_estelionato.groupby('mes_ano', as_index=False)['estelionato'].sum()
    df_estelionato = df_estelionato.sort_values(by= 'estelionato', ascending=False)
   
except Exception as e:
    print(f'\nErro ao obter dados: {e}')

try:
    print('\nCalculando medidas...')

    array_estelionato = np.array(df_estelionato['estelionato'])
    mean = np.mean(array_estelionato)
    median = np.median(array_estelionato)
    distancia = abs(((mean - median) / median) * 100)
    q1 = np.quantile(array_estelionato, .25)
    q3 = np.quantile(array_estelionato, .75)
    min = np.min(array_estelionato)
    max = np.max(array_estelionato)
    amplitude = max - min

    df_estelionato_menor = df_estelionato[df_estelionato['estelionato'] < q1] 
    df_estelionato_maior = df_estelionato[df_estelionato['estelionato'] > q3]

    df_estelionato_menor_srt = df_estelionato_menor.sort_values(by= 'mes_ano', ascending=False)
    df_estelionato_maior_srt = df_estelionato_maior.sort_values(by= 'mes_ano', ascending=False)

    print(f'\nMédia de estelionatos mês/ano: {mean:.2f}')
    print(f'\nMediana da distribuição de estelionatos por mês/ano: {median:.2f}')
    print(f'\nAssimetria da média: {distancia:.2f} %')
    print(f'\nPeríodos com menor índice de estelionato (com base em Q1): {df_estelionato_menor_srt}')
    print(f'\nPeríodos com maior índice de estelionato (com base em Q3): {df_estelionato_maior_srt}')

except Exception as e:
    print(f'\nErro ao calcular medidas: {e}')

try:
    print(f'\nCalculando outliers...')

    min = np.min(array_estelionato)
    max = np.max(array_estelionato)
    amp = max - min
    iqr = q3 - q1
    lim_inf = q1 - (1.5 * iqr)
    lim_sup = q3 + (1.5 * iqr)

    df_estelionato_out_inf = df_estelionato[df_estelionato['estelionato'] < lim_inf]
    df_estelionato_out_sup = df_estelionato[df_estelionato['estelionato'] > lim_sup]

    df_estelionato_out_inf_srt = df_estelionato_out_inf.sort_values(by= 'mes_ano', ascending=False)
    df_estelionato_out_sup_srt = df_estelionato_out_sup.sort_values(by= 'mes_ano', ascending=False)

    
    print(f'\nValor Mínimo: {min}')
    print(f'\nValor Máximo: {max}')
    print(f'\nAmplitude: {amp}')
    
    if len(df_estelionato_out_inf_srt) == 0:
        print('\nNão há outliers inferiores.')
    
    else:
        print(f'\nPeríodos de ocorrências extremamente reduzidas (outliers inferiores): {df_estelionato_out_inf_srt}')

    if len(df_estelionato_out_sup_srt) == 0:
        print('\nNão há outliers superiores.')
    
    else:
        print(f'\nPeríodos de ocorrências extremamente elevadas (outliers superiores): {df_estelionato_out_sup_srt}')

except Exception as e:
    print(f'\nErro ao calcular outliers: {e}')

try:
    print(f'\nExportando dados...')

    df_estelionato_maior.to_csv('estelionato maior.csv', sep='\t', encoding='utf-8', index=False, header=True)
    df_estelionato_menor.to_csv('estelionato menor.csv', sep='\t', encoding='utf-8', index=False, header=True)

except Exception as e:
    print(f'\nErro ao exportar dados: {e}')

try:
    print(f'\nGerando relatório...')
    
    print(f'\nO período iniciando em Janeiro de 2003 até Fevereiro de 2017 concentram as menores ocorrências de casos de estelionato, \
em paralelo, o período de outubro de 2019 até Abril de 2026 concentram os maiores índices dessa ocorrência. Estes períodos \
foram obtidos com o cálculo dos quartis Q1 ({q1}) e Q3 ({q3}), que delimitam respectivamente a faixa de valores abaixo de 25% e acima de 75% da mediana. \
A média dos dados ({mean:.2f}) apresenta assimetria de {distancia:.2f}%, indicando que valores extremos estão enviesando a média dos dados, \
assim a mediana se torna a melhor métrica para separar os dados em maiores e menores. Os valores com ocorrências acima do \
limite superior ({lim_sup:.2f}) representam outliers, que são os valores responsáveis por enviesar a média.')

except Exception as e:
    print(f'\nErro ao gerar relatório: {e}')

try:
    print(f'\nGerando gráfico...')

    plt.figure(figsize=(18, 8))
    plt.subplots (2, 1)
    plt.subplot(2, 1, 1)
    plt.boxplot(array_estelionato, vert=False, showmeans=True)
    plt.subplot(2, 1, 2)
    plt.text(0.1, 0.9, f'Média: {mean:.2f}')
    plt.text(0.1, 0.8, f'Mediana: {mean:.2f}')
    plt.text(0.1, 0.7, f'Assimetria: {distancia:.2f}')
    plt.text(0.1, 0.6, f'Mínimo: {min:.2f}')
    plt.text(0.1, 0.5, f'Máximo: {max:.2f}')
    plt.show()

except Exception as e:
    print(f'\nErro ao gerar gráfico: {e}')