# Instruções de instalação

## Instalar pacotes básicos

* [python 3.6](https://www.python.org/)
* [pip](https://pypi.python.org/pypi/pip)
* [virtualenv](https://virtualenv.pypa.io/en/stable/userguide/)
* [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

## Clonar repositório
```
$ git clone https://github.com/unb-cic-esw/twitter-data-monitor
```

## Criar virtual env
```
$ mkvirtualenv twitter-data-monitor
$ workon twitter-data-monitor
```

## Instalar dependências

Todas as bibliotecas de que o projeto depende estão listadas no arquivo [requirements.txt](requirements.txt). Para instalá-las, execute:

```
$ cd twitter-data-monitor
$ pip install -r requirements.txt
```

## Chaves de acesso

Acesse o [gerenciador de aplicações do Twitter](https://apps.twitter.com/) para gerar as chaves necessárias para acesso à API da plataforma. Essas chaves deverão ser exportadas para o ambiente com os seguintes comandos:
```
$ export TWITTER_CONSUMER_KEY="twitter_consumer_key_do_seu_app"
$ export TWITTER_CONSUMER_SECRET="twitter_consumer_secret_do_seu_app"
$ export TWITTER_ACCESS_TOKEN="twitter_access_token_do_seu_app"
$ export TWITTER_ACCESS_TOKEN_SECRET="twitter_access_token_secret_do_seu_app"
```

## Banco de dados

O endereço de conexão com o banco de dados deve ser exportado para o ambiente seguindo o padrão:
```
$ export DATABASE_URL="driver://usuario:senha@host:porta/nome_do_banco"
```
Como no exemplo abaixo:
```
$ export DATABASE_URL="mysql://root:123456@localhost/Twitter"
```

Note que, dependendo do banco de dados utilizado, outras bibliotecas deverão ser instaladas para correto funcionamento do programa.

Se, por exemplo, for utilizado o MySQL, os seguintes comandos deverão ser executados (Ubuntu 16.04):

```
$ sudo apt-get install libmysqlclient-dev
$ pip install mysqlclient
```

## Executar os testes
```
$ python -m pytest
```

## Executar o servidor localmente:
```
$ python __init__.py
```
