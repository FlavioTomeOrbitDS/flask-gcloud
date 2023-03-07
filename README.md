# Orbit Tweets Search - Documentação do Projeto
## Descrição do Projeto:
---
Orbit Tweets Search é um projeto de aplicação web que permite ao usuário exportar tweets por meio de vários parâmetros e filtros presentes em uma página web, que se conecta à API oficial do Twitter para a extração desses dados. 

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