import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    print('\nObtendo dados...')
    endereco_dados = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(endereco_dados, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencias.head())

    # delimitando as variáveis
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]

    # totalizando as ocorrências por municípios
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()
    
    # ordenando o dataframe
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by= 'roubo_veiculo', ascending=False)

except Exception as e:
    print(f'\nErro ao obter dados: {e}')

try:
    print('\nCalculando as medidas...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    mean_roubo_veiculo = np.mean(array_roubo_veiculo)
    median_roubo_veiculo = np.median(array_roubo_veiculo)

    # até 10%, simetria; até 25%, assimetria moderada; acima de 25%, assimetria acentuada
    distancia = abs(((mean_roubo_veiculo - median_roubo_veiculo) / median_roubo_veiculo) * 100)

    print('\nMedidas de tendência central')
    print(30 * "=")
    print(f'Média: {mean_roubo_veiculo:.2f}')
    print(f'Mediana: {median_roubo_veiculo:.2f}')
    print(f'Distância: {distancia:.2f}')

except Exception as e:
    print(f'\nErro ao calcular medidas: {e}')

# obtendo a distribuição
try:
    print('\nProcessando os quartis')

    q1 = np.quantile(array_roubo_veiculo, .25)
    q3 = np.quantile(array_roubo_veiculo, .75)
    print('\nQuartis')
    print(30 * "=")
    print(f'Q1: {q1:.2f}')
    print(f'Mediana: {median_roubo_veiculo:.2f}')
    print(f'Q3: {q3:.2f}')

    df_roubo_veiculo_menor = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    df_roubo_veiculo_maior = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    print('\nLista de municípios com menor número de ocorrências de roubo de veículo')
    print(30 * "=")
    print(df_roubo_veiculo_menor.sort_values(by='roubo_veiculo', ascending=True))
    print('\nLista de municípios com maior número de ocorrências de roubo de veículo')
    print(30 * "=")
    print(df_roubo_veiculo_maior)

except Exception as e:
    print(f'\nErro ao obter a distribuição: {e}')

# medidas de dispersão
try:

    # se mais próximo do mínimo, baixa dispersão; do máximo, alta dispersão
    min = np.min(array_roubo_veiculo)
    max = np.max(array_roubo_veiculo)
    amplitude = max - min

    print('\nMedidas de dispersão')
    print(30 * "=")
    print(f'\nMínimo: {min}')
    print(f'Máximo: {max}')
    print(f'Amplitude total: {amplitude}')

except Exception as e:
    print(f'\nErro ao obter medidas de dispersão: {e}')

# calculando outliers
try:
    # amplitude de q2
    iqr = q3 - q1
    lim_inf = q1 - (1.5 * iqr)
    lim_sup = q3 + (1.5 * iqr)
    
    print('\nParâmetros de outliers')
    print(30 * "=")
    print(f'\nIQR: {iqr}')
    print(f'Limite inferior: {lim_inf}')
    print(f'limite superior: {lim_sup}')


except Exception as e:
    print(f'\nErro ao calcular parâmetros: {e}')

try:

    df_roubo_veiculo_out_inf = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < lim_inf]
    df_roubo_veiculo_out_sup = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > lim_sup]

    print('\nMunícipios outliers inferiores em roubo de veículos')
    print(30 * "=")
    
    if len(df_roubo_veiculo_out_inf) == 0:
        print('Não existem outliers inferiores')
    else:
        print(df_roubo_veiculo_out_inf.sort_values(by='roubo_veiculo', ascending=True))
    
    print('\nMunícipios outliers superiores em roubo de veículos')
    print(30 * "=")
    
    if len(df_roubo_veiculo_out_sup) == 0:
        print('Não existem outliers superiores')
    else:
        print(df_roubo_veiculo_out_sup.sort_values(by='roubo_veiculo', ascending=False))
    
except Exception as e:
    print(f'\nErro ao exibir outliers: {e}')

try:
    # plotando gráficos

    plt.figure(figsize=(16, 8))
    df_roubo_veiculo_maior = df_roubo_veiculo_maior.sort_values(by='roubo_veiculo', ascending=False).head(10)

    plt.bar(df_roubo_veiculo_maior['munic'], df_roubo_veiculo_maior['roubo_veiculo'])
    plt.title('Municípios com maiores roubos de veículo')
    plt.show()


except Exception as e:
    print(f'\nErro ao plotar: {e}')