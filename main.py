from flask import Flask, request, redirect, render_template, flash

app = Flask(__name__)
app.secret_key = 'chave'

livros=[]
emprestado=[]

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
        livros.append([codigo, nome, autor, ano])
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
        livros[codigo] = [codigo, nome, autor, ano]
        return redirect('/')
    else:
        livro = livros[codigo]
        return render_template('editar_livro.html', livro=livro)

@app.route('/apagar_livro/<int:codigo>')
def apagar_livro(codigo):
    del livros[codigo]
    return redirect('/')

@app.route('/emprestar_livro/<int:codigo>')
def emprestar_livro(codigo):
    if request.method == 'POST':
        flash('Livro Emprestado')
        emprestado.append([livros[codigo]])
        return redirect('/')
    else:
        return render_template('livros_emprestados.html')



if __name__=='__main__':
    app.run(debug=True)
