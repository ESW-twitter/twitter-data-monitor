from app import app


@app.route('/api/teste_api')
def teste_api():
	return "TESTE"