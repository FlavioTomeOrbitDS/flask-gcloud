# Orbit Tweets Search - Documentação do Projeto
## Descrição do Projeto:
---
Orbit Tweets Search é um projeto de aplicação web que permite ao usuário exportar tweets por meio de vários parâmetros e filtros presentes em uma página web, que se conecta à API oficial do Twitter para a extração desses dados. 
Foi desenvolvido utilizando o Framework Flask na versão 2.2.2

### Estrutura do Projeto
Nessa versão 1.0, o Front End e o Back End da aplicação foram desenvolvidos no mesmo projeto.
Os arquivos html, bem como os arquivos de estilo e javascript estão na pasta **templates**
Já as configurações de rota, connexão com a API do Twitter e demais funções encontram-se nos arquivos **main.py** e **scripts.py**
```
├── flask-gcloud/
│   ├── static/                     # pasta que contém os arquivos estáticos da aplicação  
|   |    ├──logo-orbit.jpeg         # arquivo com o logotipo da Orbit Data Science
|   ├── templates/                  # Pasta que contém os arquivos HTML da aplicação
|   |    ├──index.html              # Página Principal da aplicação. Possui as opções para fazer o Tweets Serarch
|   |    ├──login.html              # Página de Login
|   |    ├──tweetscount.html        # Página com as opções de Tweets Count
|   ├── venv/                           
|   ├── .gitignore
|   ├── app.py
|   ├── app.yaml                    # Arquivo com as configurações para fazer o deploy no Google Cloud
|   ├── main.py                       
|   ├── requirements.txt            # Arquivo que lista os módulos necessários para o projeto
|   ├── scripts.py                  # Arquivo com as funções globais da aplicação
```
## Telas da Aplicação
---
### Login Page:

![Login Page](https://user-images.githubusercontent.com/115179333/226707926-93e0b2e8-9660-440c-9e35-510017c9e9ee.png)

### Index Page:
![Index Page](https://user-images.githubusercontent.com/115179333/226708353-7b93ed0e-ac02-40f1-a9da-c43156249588.png)

### Tweets Count Page:
![Tweets Count Page](https://user-images.githubusercontent.com/115179333/226708420-d6e0cd4c-7c7b-4231-bb9a-c5c6f3fb7401.png)



## Instalação e configuração
---
#### Pré-Requisitos
Para executar este projeto, você precisará ter instalado em sua máquina:

* Python 3.8 ou superior
* Pip (gerenciador de pacotes do Python)
* Conta do Google Cloud Platform com o Cloud Storage e o Cloud Run habilitados
* Conta de desenvolvedor do Twitter com acesso à API

#### Instalação
1. Clone o repositório para a sua máquina:
```
git clone https://github.com/FlavioTomeOrbitDS/flask-gcloud.git

```
2. No terminal, navegue até a pasta raiz do projeto, crie um **virtual enviroment** e ative-o:
```
>python -m venv venv
```
```
>venv\Scripts\activate
```
3. Instale as dependências:
```
pip install -r requirements.txt

```

## Execução
---
Para executar o projeto, execute o seguinte comando:
```
python main.py

```
## Deploy no Google App Engine
Para fazer o deploy de uma aplicação Flask no Google App Engine, siga as seguintes etapas:

1. Certifique-se de ter o SDK do Google Cloud instalado em sua máquina. Caso não tenha, faça o download e siga as instruções de instalação na página https://cloud.google.com/sdk/docs/install.
3. Abra o terminal ou prompt de comando e navegue até o diretório raiz do Projeto.
4. Crie um arquivo chamado app.yaml e adicione o seguinte conteúdo:
```
runtime: python310

entrypoint: gunicorn -b :$PORT main:app -t 60 -w 1 --threads 8
```
Este arquivo de configuração especifica a versão do Python a ser usada, bem como o comando de entrada para iniciar o servidor web.
4. Execute o seguinte comando no terminal para iniciar o deploy:
```
gcloud app deploy
```
5. O comando acima vai iniciar o processo de deploy da aplicação no Google App Engine. Caso seja a primeira vez que você esteja fazendo deploy, será necessário fazer login na sua conta do Google Cloud Platform e selecionar o projeto onde você deseja implantar a aplicação.

6. Após o deploy ser concluído com sucesso, acesse a URL fornecida pelo Google App Engine para visualizar a sua aplicação Flask.

## Principais Métodos
---
### getTweetsFullArchive():

Método responsável por realizar buscas utilizando a API do Twitter através do endpoint full archive. Esse método recebe como parâmetros:

* query: palavra-chave ou hashtag que será pesquisada;
* lang: idioma dos tweets que serão buscados. O valor padrão é -1;
* fromDate: data inicial da busca, no formato 'AAAAMMDDHHMM';
* toDate: data final da busca, no formato 'AAAAMMDDHHMM';
* lat: latitude do ponto de interesse. O valor padrão é -1;
* long: longitude do ponto de interesse. O valor padrão é -1;
* radius: raio de busca em quilômetros. O valor padrão é -1;
* country: código do país onde a busca será realizada. O valor padrão é -1.

#### Fluxo do Método:
1. Verifica se o parâmetro lang é diferente de -1. Se sim, adiciona a string ' lang:'+lang na query;
2. Verifica se o parâmetro country é diferente de -1. Se sim, adiciona a string ' place_country:'+country na query;
3. Verifica se os parâmetros lat, long e radius são diferentes de -1. Se sim, adiciona a string " point_radius:[long lat radiuskm]" na query;
4. Realiza a primeira requisição sem o parâmetro 'next' para obter os primeiros resultados da busca;
5. Caso a requisição seja bem sucedida, armazena os resultados em um DataFrame;
6. Verifica se há um token 'next' na resposta. Se sim, realiza novas requisições utilizando esse token para obter o restante dos resultados;
7. Concatena os resultados obtidos em um DataFrame e retorna o mesmo.
#### Saída:
df1: DataFrame contendo os resultados obtidos na busca. Caso não seja possível obter resultados, retorna um DataFrame vazio.

### getTweetsCount():
Esta função recebe como entrada os seguintes parâmetros:

* query: string que contém a palavra-chave da pesquisa.
* lang: string que contém o código do idioma da pesquisa. Se não houver um código específico, o valor padrão é "-1".
* fromDate: string no formato "YYYYMMDDHHmm" que define a data e hora de início da pesquisa.
* toDate: string no formato "YYYYMMDDHHmm" que define a data e hora de término da pesquisa.
* lat: string que define a latitude geográfica da pesquisa. Se não houver uma coordenada específica, o valor padrão é "-1".
* long: string que define a longitude geográfica da pesquisa. Se não houver uma coordenada específica, o valor padrão é "-1".
* radius: string que define o raio geográfico da pesquisa em quilômetros. Se não houver um raio específico, o valor padrão é "-1".
* country: string que define o país da pesquisa. Se não houver um país específico, o valor padrão é "-1".

#### Fluxo do Método:

1. O código começa definindo a variável bearer_token com a chave de autorização para acessar a API do Twitter. Em seguida, define-se o cabeçalho da consulta contendo a chave de autorização.

2. Se houver um idioma especificado, o código atualiza a consulta adicionando o parâmetro lang. Se houver um país especificado, o código atualiza a consulta adicionando o parâmetro place_country.

3. Se houver uma latitude, longitude e raio geográfico especificados, o código atualiza a consulta adicionando o parâmetro point_radius.

4. Em seguida, o código define o objeto de parâmetros e a URL da API do Twitter. A função usa a biblioteca requests para enviar uma solicitação HTTP GET para a API do Twitter com os parâmetros e cabeçalho definidos. O código exibe a URL de consulta na saída padrão.

5. Se a resposta HTTP retornar o código de status 429, o código exibe uma mensagem de erro na saída padrão e retorna um objeto pandas.DataFrame vazio.

6. Se a resposta HTTP retornar um código de status diferente de 429, o código exibe a resposta HTTP na saída padrão. Se a resposta contiver dados JSON, o código converte os dados em um objeto pandas.DataFrame.

7. Se houver um token "next" na resposta JSON, o código usa esse token para obter os dados restantes. O código usa um loop while para obter os dados restantes até que não haja mais tokens "next".

8. Se a resposta HTTP retornar o código de status 429 durante a execução do loop while, o código exibe uma mensagem de erro na saída padrão e retorna o objeto pandas.DataFrame atual.

9. Ao final do código, a função retorna o objeto pandas.DataFrame contendo as contagens diárias de tweets correspondentes à consulta.

#### Saída:
A função retorna um objeto pandas.DataFrame contendo as contagens diárias de tweets correspondentes à consulta. A API do Twitter é acessada para obter esses dados. A função usa o cabeçalho de autorização e a consulta de URL fornecidos pela API do Twitter.
