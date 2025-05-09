from flask import Flask, request, redirect, render_template, flash
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'chave'

emprestados=[]
livros=[]

@app.route('/')
def index():
    return render_template('index.html', livros=livros)

@app.route('/adicionar_livro', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        nome= request.form['nome']
        autor = request.form['autor']
        ano = request.form['ano']

        codigo= len(livros)
        livros.append([codigo, nome, autor, ano, ])
        flash('Livro Adicionado')
        return redirect('/')
    else:
        return render_template('adicionar_livro.html')

@app.route('/editar_livro/<int:codigo>', methods=['GET', 'POST'])
def editar_livro(codigo):
    if request.method == 'POST':
        nome = request.form['nome']
        autor = request.form['autor']
        ano = request.form['ano']
        livros[codigo] = [codigo, nome, autor, ano,]
        return redirect('/')
    else:
        livro = livros[codigo]
        return render_template('editar_livro.html', livro=livro)

@app.route('/apagar_livro/<int:codigo>')
def apagar_livro(codigo):
    del livros[codigo]
    return redirect('/')

@app.route("/emprestar_livro/<int:codigo>")
def emprestar_livro(codigo):
    hoje = datetime.now()
    devolucao = hoje + timedelta(days=-7)
    livros[codigo]["emprestado"] = True
    livros[codigo]["data_emprestimo"] = hoje
    livros[codigo]["data_devolucao"] = devolucao

    flash("Livro emprestado! Devolução até " + devolucao.strftime("%d/%m/%Y"))
    return redirect("/")



@app.route("/devolver/<int:codigo>")
def devolver(codigo):
    hoje = datetime.now()
    devolucao = livros[codigo]["data_devolucao"]
    atraso = (hoje - devolucao).days
    if atraso > 0:
        multa = 10 + (10 * 0.01 * atraso)
        flash(f"Livro devolvido com {atraso} dias de atraso. multa: R$ {multa}")
    return redirect("/")



if __name__=='__main__':
    app.run(debug=True)


