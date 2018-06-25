# Monitor de Dados do Twitter

Este repositório compõe projeto de pesquisa com foco empírico nas eleições brasileiras de 2018 do grupo de pesquisa [Resocie](http://resocie.org) do [Instituto de Ciência Política - IPOL](http://ipol.unb.br/) com o apoio técnico do [Departamento de Computação - CIC](http://www.cic.unb.br/) da [Universidade de Brasília - UnB](http://unb.br).

O projeto consiste na coleta sistemática de informações quantitativas da plataforma Twitter com o objetivo de subsidiar a análise do comportamento político de alguns atores da cena eleitoral durante o período de campanha. Além de seu objetivo finalístico para a coleta de dados, o projeto tem também por intuito servir de material de estudo dos alunos da disciplina Engenharia de Software do Departamento de Ciência da Computação da UnB no 1º semestre de 2018.

As instruções a seguir trazem orientações para aqueles que quiserem contribuir com a iniciativa.

# Instruções de instalação

### Instalar pacotes básicos

* [python 3.6](https://www.python.org/)
* [pip](https://pypi.python.org/pypi/pip)
* [virtualenv](https://virtualenv.pypa.io/en/stable/userguide/)
* [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

### Clonar repositório
```
$ git clone https://github.com/unb-cic-esw/twitter-data-monitor
```

### Criar virtual env
```
$ mkvirtualenv twitter-data-monitor
$ workon twitter-data-monitor
```

### Instalar dependências

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

## Licença

Código disponível sob [Licença MIT](LICENSE)
