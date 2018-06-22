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
$ git clone git@github.com:code4pol/twitter-data-monitor.git
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
$ export TWITTER_CONSUMER_KEY="[twitter_consumer_key do seu app]"
$ export TWITTER_CONSUMER_SECRET="[twitter_consumer_secret do seu app]"
$ export TWITTER_ACCESS_TOKEN="[twitter_access_token do seu app]"
$ export TWITTER_ACCESS_TOKEN_SECRET="[twitter_access_token_secret do seu app]"
```

## Banco de dados

O endereço de conexão com o banco de dados deve ser exportado para o ambiente seguindo o padrão:
```
$ export DATABASE_URL="driver://username:password@host:port/database_name"
```
Por exemplo:
```
$ export DATABASE_URL="mysql://root@localhost/Twitter"
```

## Executar os testes

Todos os testes foram desenvolvidos utilizando a biblioteca [unittest](https://docs.python.org/3/library/unittest.html) nativa do Python. Para executá-los, a partir da pasta raiz do projeto, execute:

```
$ python -m pytest
```


## Licença

Código disponível sob [Licença MIT](LICENSE)
