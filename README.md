# Monitor de Dados do Twitter

Este repositório compõe projeto de pesquisa com foco empírico nas eleições brasileiras de 2018 do grupo de pesquisa [Resocie](http://resocie.org) do [Instituto de Ciência Política - IPOL](http://ipol.unb.br/) com o apoio técnico do [Departamento de Computação - CIC](http://www.cic.unb.br/) da [Universidade de Brasília - UnB](http://unb.br).

O projeto consiste na coleta sistemática de informações quantitativas da plataforma Twitter com o objetivo de subsidiar a análise do comportamento político de alguns atores da cena eleitoral durante o período de campanha. Além de seu objetivo finalístico para a coleta de dados, o projeto tem também por intuito servir de material de estudo dos alunos da disciplina Engenharia de Software do Departamento de Ciência da Computação da UnB no 1º semestre de 2018.

As instruções a seguir trazem orientações para aqueles que quiserem contribuir com a iniciativa.

## Preparar ambiente

Um bom processo de trabalho em desenvolvimento de software começa com a preparação de um ambiente adequado de programação.

### Instalar pacotes básicos

* [python 3.6](https://www.python.org/)
* [pip](https://pypi.python.org/pypi/pip)
* [virtualenv](https://virtualenv.pypa.io/en/stable/userguide/)
* [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

O [Henrique Bastos](https://github.com/henriquebastos) fez [uma postagem super relevante sobre organização de ambientes python](https://medium.com/welcome-to-the-django/guia-definitivo-para-organizar-meu-ambiente-python-a16e2479b753). Vale a leitura.

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

Acesse o [gerenciador de aplicações do Twitter](https://apps.twitter.com/) para gerar as chaves necessárias para acesso à API da plataforma. Essas chaves deverão ser inseridas no arquivo [keys.json](keys.json)

## Executar os testes

Todos os testes foram desenvolvidos utilizando a biblioteca [unittest](https://docs.python.org/3/library/unittest.html) nativa do Python. Para executá-los, a partir da pasta raiz do projeto, execute:

```
$ python -m unittest discover tests
```

Sugiro darem uma olhada [nesta ótima introdução ao unittest](http://pythontesting.net/framework/unittest/unittest-introduction/)

## ToDo

Este é apenas um esqueleto de projeto para que o grupo comece a trabalhar. Resta ainda muito trabalho a ser feito. Algumas ideias:

* Corrigir testes quebrados
* Complementar testes
* Remover código hard-coded
* Corrigir código replicado
* Incluir mecanismo de logging
* Expandir quantidade dos dados buscados
* Criar interface CLI para execução do programa
* Implementar mecanismo para automatização da coleta recorrente dos dados
* Persistir dados coletados em base estruturada
* Viabilizar interface de integração da base de dados criada com canal para geração de informações visuais

## Licença

Código disponível sob [Licença MIT](LICENSE)
