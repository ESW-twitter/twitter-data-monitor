# End-Points


## Das capturas de Atores (followers, following, likes e número de tweets):

* /api/actors

	Retorna a lista de usernames de atores monitorados

* /api/actors/datetime

	Retorna a lista de datas em que as capturas foram realizadas

* /api/actor/username/

	Retorna as informações quantitativas instantâneas do ator especificado pelo username, e as datas de coleta de tweets e datas de coleta de informações quantitativas do ator.

* /api/actor/username/date

	Retorna as informações quantitativas to ator especificado pelo username na data especificada. Caso existam varias capturas no mesmo dia, estas estarão separadas pela hora/minuto da captura.

## Das capturas de Tweets por ator:

* /api/actor/username/date/tweets

	Retorna as informações de todos os tweets daquele ator como estavam na data especificada.

## Das capturas de Relações entre atores:

* /api/relations

	Retorna as datas em que as relações de retweets foram capturadas

* /api/relations/date

	Retorna as informações de Relações de Retweets entre atores na data especificada. Cada ator presente na captura terá uma lista de dicionarios relacionada ao seu username. Nessa lista, cada item contem a informação de quem o ator retweetou e quantas vezes. 
	Caso existam varias capturas no mesmo dia, estas estarão separadas pela hora/minuto da captura.