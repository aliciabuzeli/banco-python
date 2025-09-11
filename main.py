from flask import Flask, render_template, request, redirect, flash, url_for
import fdb

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCO (4)\BANCO.FDB'
user = 'sysdba'
passaword = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=passaword)

@app.route('/')
def index():
    cursor = con.cursor()
    cursor.execute("SELECT id_livro, titulo, autor, ano_publicacao FROM LIVROS")
    livros = cursor.fetchall()
    cursor.close()

    return render_template('livros.html', livros=livros)


@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Livro')

@app.route('/criar', methods=['POST'])
def criar():
    #pega os dados do formulario
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano_publicacao = request.form['ano_publicacao']

    cursor = con.cursor()

    try:
        cursor.execute('SELECT 1 FROM livros WHERE livros.TITULO = ?', (titulo,))
        if cursor.fetchone(): #se existir algum livro com o titulo passado
            flash("Erro: Livro já cadstrado", "error")
            return redirect(url_for('/novo'))

        cursor.execute("INSERT INTO livros(titulo, autor, ano_publicacao) VALUES (?,?,?)",
                       (titulo, autor, ano_publicacao))
        con.commit()
    finally:
        cursor.close()
    flash("Livro cadastrado com sucesso")
    return redirect(url_for('index'))
                        
@app.route('/atualizar')
def atualizar():
    return render_template('editar.html', titulo='Editar livro')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor= con.cursor() #abre cursor
    cursor.execute("select id_livro, titulo, autor, ano_publicacao from livros where id_livro = ?", (id,))
    livro = cursor.fetchone()

    if not livro:
        cursor.close()
        flash("Livro não encontado")
        return redirect(url_for('index'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano_publicacao = request.form['ano_publicacao']

        cursor.execute("update livros set titulo = ?, autor = ?, ano_publicacao = ? where id_livro = ?",
                       (titulo, autor, ano_publicacao, id))
        con.commit()
        flash("Livro atualizado com sucesso")
        return redirect(url_for('index'))

    cursor.close()
    return render_template('editar.html', livro=livro, titulo='Editar Livro')

@app.route('/deletar/<int:id>', methods=('POST',))
def deletar(id):
    cursor = con.cursor()  # Abre o cursor

    try:
        cursor.execute('DELETE FROM livros WHERE id_livro = ?', (id,))
        con.commit()  # Salva as alterações no banco de dados
        flash('Livro excluído com sucesso!', 'success')  # Mensagem de sucesso
    except Exception as e:
        con.rollback()  # Reverte as alterações em caso de erro
        flash('Erro ao excluir o livro.', 'error')  # Mensagem de erro
    finally:
        cursor.close()  # Fecha o cursor independentemente do resultado

    return redirect(url_for('index'))  # Redireciona para a página principal













if __name__ == '__main__':
    app.run(debug=True)