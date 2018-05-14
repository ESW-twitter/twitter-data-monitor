
class twitterAPI:

	def __init__(self, app):
		self.app = app

		#COLOCAR AQUI AS ROTAS DA API
		@app.route('/teste')
		def hello():
			return "Teste!"