from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from app_leandro.bmq_config import conecta_no_banco_de_dados
from .forms import ContatoForm
from django.shortcuts import render, 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.db import transaction  
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

def index(request):
    return render(request, 'templates/paginainicial.html')

def template(request):
    return render(request, 'templates/template.html')
# Create your views here.

def cadastro():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))

    # Obtém os valores dos campos "nome", "email" e "senha" do formulário submetido via POST.
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    # Validação dos campos obrigatórios
    if not nome or not email or not senha:
        flash('Todos os campos são obrigatórios.')
        return render_template('cadastro.html')

    try:
        # Conecta ao banco de dados
        bd_mysql = conecta_no_banco_de_dados()
        cursor = bd_mysql.cursor()

        # Verifica se o email já está cadastrado
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = %s;", (email,))
        existe = cursor.fetchone()[0]

        if existe > 0:
            flash('Email já cadastrado')
            return render_template('cadastro.html')

        # Insere novo usuário no banco de dados
        sql = 'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)'
        values = (nome, email, senha)
        cursor.execute(sql, values)
        bd_mysql.commit()

        return redirect(url_for('pagina_usuarios'))
    except bd_mysql.connector.Error as e:
        return render_template('cadastro.html', error=str(e))
    finally:
        if bd_mysql is not None:
            bd_mysql.close()
    

def cliente():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    usuario_id = session.get('usuario_id')
    bd_mysql = conecta_no_banco_de_dados()
    cursor = bd_mysql.cursor()
    cursor.execute("""
        SELECT ct.*
        FROM meus_clientes AS ct
        INNER JOIN usuario_contato AS uc ON uc.contato_id = ct.id
        WHERE uc.usuario_id = %s ORDER BY ct.id
    """, (usuario_id,))
    meus_clientes = cursor.fetchall()
    return render_template("cliente.html", meus_clientes=meus_clientes)


def meus_clientes():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    bd_mysql = conecta_no_banco_de_dados()
    cursor = bd_mysql.cursor()
    cursor.execute('SELECT * FROM meus_clientes WHERE meus_clientes.situacao != "Atendimento" AND meus_clientes.situacao != "Finalizado";')
    meus_clientes = cursor.fetchall()
    return render_template("meus_clientes.html", meus_clientes=meus_clientes)

def sucesso():
    return render_template('sucesso.html')

def paginainicial():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    # Renderiza o template 'paginainicial.htmlp' e retorna a página HTML gerada.
    return render_template("paginainicial.html")


def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            try:
                # Estabelecer conexão com o banco de dados
                bmq = conecta_no_banco_de_dados()

                # Preparar consulta SQL e valores
                nome = form.cleaned_data['nome']
                email = form.cleaned_data['email']
                mensagem = form.cleaned_data['mensagem']
                sql = "INSERT INTO contatos (nome, email, mensagem) VALUES (%s, %s, %s)"
                values = (nome, email, mensagem)

                # Executar consulta SQL e confirmar alterações
                cursor = bmq.cursor()
                cursor.execute(sql, values)
                bmq.commit()

                # Mensagem de sucesso e redirecionamento
                print(f"Dados do formulário salvos com sucesso!")
                return HttpResponseRedirect('/')

            except Exception as err:
                # Manipular erros de banco de dados
                print(f"Erro ao salvar dados no banco de dados: {err}")
                mensagem_erro = "Ocorreu um erro ao processar o seu contato. Tente novamente mais tarde."
                return render(request, 'erro.html', mensagem_erro=mensagem_erro), 500

            finally:
                # Fechar conexão com o banco de dados se estiver aberta
                if bmq is not None:
                    bmq.close()

        else:
            # Manipular dados de formulário inválidos
            return render(request, 'contato.html', {'form': form})

    else:
        # Renderizar formulário vazio
        form = ContatoForm()
        return render(request, 'contato.html', {'form': form})