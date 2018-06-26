# Colaborando com o projeto

Para colaborar com o projeto Monitor de Dados do Twitter, primeiramente siga as [instruções de instalação](https://github.com/unb-cic-esw/twitter-data-monitor/blob/master/RUNNINGLOCALLY.md) e certifique-se de que consegue rodar o projeto localmente.

### Alterações/Adicão de Funcionalidades:

Siga as instruções abaixo sempre que realizar alterações no código e/ou adicionar funcionalidades:

- Crie uma nova branch e faça alterações nela:
```
$ git checkout -b nova_branch
```

- Certifique-se de que suas alterações não quebraram nenhum teste

- Adicione suas alterações à branch remota:
```
$ git push origin nova_branch
```

- Abra um Pull Request para a master do repositório (testes de integração serão realizados pelo Travis CI.)

- Aguarde a análise dos administradores do repositório
