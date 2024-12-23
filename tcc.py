# -*- coding: utf-8 -*-
"""TCC.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AeIE5tbZ0owCgvtW5xphtam91Hk3rpJT
"""

# importar os pacotes necess�rios
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report, accuracy_score, f1_score
from imblearn.under_sampling import RandomUnderSampler
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression

# filtrar mensagens de warning
import warnings
warnings.filterwarnings('ignore')

rand = 40

#Importando os dados
df = pd.read_csv(r"/content/DatasetAntigo.csv")

#Imprimindos a dimensão das linhas e variáveis da base de dados
print("Quantidade de dados: ", df.shape[0])
print("Quantidade de variáveis: ", df.shape[1])

#Imprimindo as 5 primeiras linhas
df.head()

def Map_Var_DF (features, df):
  #Criando um dicion�rio para receber as vari�veis
  dict_var = {"feature": [],
              "Tipo": [],
              "Categórico": [],
              "Binário": [],
              "Qtd var unico": [],
              "Min": [],
              "Max": [],
              "% Qtd de Nulos": []}

  #Criando um loop a partir das features
  for feature in features:

    #Armazenando o nome da feature
    dict_var['feature'].append(feature)

    #Armazenando o tipo da vari�vel
    dict_var['Tipo'].append(df[feature].dtypes)

    #Armazenando a quantidade de valores nulos
    dict_var['% Qtd de Nulos'].append(round(df[feature].isnull().sum() / df.shape[0],4))

    if ((df[feature].dtype == "O")):

      #Atribuindo o valor 1 se a vari�vel for categ�rica
      dict_var['Categórico'].append(1)

      #Armazenando a quantidade de valores �nicos
      dict_var['Qtd var unico'].append(df[feature].nunique())

      #Armazenando os valores m�nimos
      dict_var['Min'].append("N/A")

      #Armazenando os valores m�ximos
      dict_var['Max'].append("N/A")

      if (df[feature].nunique() == 2):

        #Atribuindo o valor 1 se a vari�vel for bin�ria
        dict_var['Binário'].append(1)

      else:

        #Atribuindo o valor 0 se a vari�vel n�o for bin�ria
        dict_var['Binário'].append(0)

    else:

      #Atribuindo o valor 0 se a vari�vel n�o for categ�rica
      dict_var['Categórico'].append(0)

      #Armazenando a quantidade de valores �nicos
      dict_var['Qtd var unico'].append(df[feature].nunique())

      #Atribuindo o valor 0 se a vari�vel n�o for bin�ria
      dict_var['Binário'].append(0)

      #Armazenando os valores m�nimos
      dict_var['Min'].append(df[feature].min())

      #Armazenando os valores m�ximos
      dict_var['Max'].append(df[feature].max())

  #Transformando o dicion�rio em dataframe
  df_var = pd.DataFrame.from_dict(data = dict_var)

  #Imprimindo o dataframe
  return df_var

#Armazenando as features
features = df.columns.to_list()

#Armazenando as informa��es das vari�veis
df_var = Map_Var_DF(features = features, df = df)

#Imprimindo o dataframe
df_var

#Copiando o dataset
df_clean = df.copy()

#Exluindo os valores ausentes da vari�vel alvo
df_clean.dropna(subset = ['Classificação'] ,inplace = True)

#Armazenando as vari�veis a serem exclu�das
Col_Ex = ['Sugestão']

#Exluindo as colunas do dataframe
df_clean.drop(labels = Col_Ex, axis = 1, inplace = True)

#Armazenando as features do dataframe
features_clean = df_clean.columns.to_list()

#Replicando a fun��o
var_df_clean = Map_Var_DF(features = features_clean, df = df_clean)

#Imprimindo o datafram
var_df_clean

#Armazenando as features num�ricas
num_feature = var_df_clean['feature'].loc[ (var_df_clean['Tipo'] == 'float64') ].to_list()

#Contador
cont_x = 0
cont_y = 0

# #Definindo os par�metros de style para o matplotlib
rc_params = {'axes.edgecolor':'#787878',
             'axes.titlecolor':'#787878',
             'axes.labelcolor': '#787878',
             'axes.spines.top':False,
             'axes.spines.right': False,
             'axes.spines.left': False,
             'ytick.left': False,
             'xtick.color': '#787878',
             'ytick.color': '#787878',
             'axes.titleweight': 'bold',
             'axes.titlesize': 12
             }

#Aplicando os par�metros no matplotlib/seaborn
with plt.rc_context(rc_params):

  #Instanciando a figure e axes
  fig, ax = plt.subplots(nrows = 8, ncols = 2, figsize = (14,12) )

  #Rodando loop entre as features num�ricas
  for feature in num_feature:

    #Criando o Box Plot para as features
    sns.boxplot(x = feature, data = df_clean, ax = ax[cont_x,cont_y])

    #Atualizando os valores dos contadores para o axes
    if cont_y == 1:
      cont_x = cont_x + 1
      cont_y = 0

    else :
      cont_y = cont_y + 1

  #Imprimindo os gr�ficos
  fig.tight_layout()

#Definindo os par�metros de style para o matplotlib
rc_params = {'axes.edgecolor':'#787878',
             'axes.titlecolor':'#787878',
             'axes.labelcolor': '#787878',
             'axes.spines.top':False,
             'axes.spines.right': False,
             'xtick.color': '#787878',
             'ytick.color': '#787878',
             'axes.titleweight': 'bold',
             'axes.titlesize': 12
             }

#Aplicando os par�metros no matplotlib/seaborn
with plt.rc_context(rc_params):

  #Instanciando o objeto figure e axes
  fig, ax = plt.subplots( figsize = (14,4) )

  #Criando um histograma para a vari�vel tenure
  sns.histplot(data = df_clean, x = 'Classificação', ax = ax, hue = "Classificação", multiple="dodge", shrink=2.8)

    #Armazena o % da amostra
  percentual_default = round((df_clean['Classificação'].value_counts()[1] / df_clean.shape[0])*100,3)

  #Setando o t�tulo do gr�fico
  ax.set_title("Variavel Classificação")

  plt.legend(['2','1','0'],loc = 5)
  #Exibindo o gr�fico
  plt.tight_layout()

#Lista de vari�veis num�ricas
var_num = ['Valor carteira',
           '% Cart',
           'Classificação']

#Lista de vari�veis categ�ricas (getdummies)
var_cat = ['OBS',
           'OBS das operações',
           'Ramo de Atuação']

  #Vamos copiar o dataframe
df_trat = df_clean.copy()


#Aplicando o get_dummies nas vari�veis categ�ricas
df_trat = pd.get_dummies(data = df_trat, columns = var_cat)

#Imprimindo as 5 primeiras linhas
df_trat.head()

#Definindo os valores de X e y
X = df_trat.drop(['Classificação','Cedente', '% Cart'], axis = 1)
y = df_trat['Classificação']

#Dividindo o dataset em treino e test
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    shuffle = True,
                                                    stratify = y,
                                                    random_state = rand)

# #Instanciando os parametros do Kfold para Validaçao Cruzada
# k_fold = KFold(n_splits = 5, shuffle = True, random_state = rand)

X_train

X_test

y_test

from sklearn.feature_selection import SelectFromModel

model_rl = LogisticRegression(random_state = rand)

#Treinando o modelo
model_rl.fit(X = X_train, y = y_train)

#Calculando a probabilidade y
y_proba = model_rl.predict_proba(X_test)

#Transformando em um dataframe
y_proba_df = pd.DataFrame(y_proba)


#df.apply(lambda row: row['First']*row['Second']* row['Third'], axis=1)
y_proba_df['Predict'] = y_proba_df.apply(lambda row: 0 if row[0] > 0.333 else 1 if row[1] > 0.333 else 2.0, axis=1)

y_proba_df

# Classification Report
print(classification_report(y_test, y_proba_df['Predict']))

#print("AUC Score: ",roc_auc_score(y_test, y_proba[:,1]))

print("--------------------------------------------------------------------")

#Instanciando a figure e axes
fig, ax = plt.subplots()

#Plotando a matriz de confusão em um heatmap
sns.heatmap(confusion_matrix(y_test, y_proba_df['Predict'], normalize = 'true'),
            square=True,
            annot=True,
            cbar=False,
            ax = ax)

#Definindo o nome do eixo x
ax.set_xlabel("Previsão do Modelo")

#Definindo o nome do eixo y
ax.set_ylabel("Valor Verdadeiro")

#Definindo o título
ax.set_title("Matriz Confusão Regressão Logística")

#Exibindo a matriz de confusão
plt.show()