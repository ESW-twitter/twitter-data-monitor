from app import app


@app.route('/teste_api')
def teste_api():
	return "TESTE"