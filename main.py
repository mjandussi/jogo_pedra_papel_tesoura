from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

@app.route('/')
def home():
    session.clear()  # Limpa a sessão para começar um novo jogo
    return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    escolhas = ['pedra', 'papel', 'tesoura']
    escolha_usuario = request.form.get('escolha')
    escolha_computador = random.choice(escolhas)

    if escolha_usuario:  # Se o usuário não cancelou
        session['escolhas_usuario'] = session.get('escolhas_usuario', [])
        session['escolhas_computador'] = session.get('escolhas_computador', [])
        session['escolhas_usuario'].append(escolha_usuario)
        session['escolhas_computador'].append(escolha_computador)

        if escolha_usuario == escolha_computador:
            resultado = 'Empate!'
        elif (escolha_usuario == 'pedra' and escolha_computador == 'tesoura') or \
             (escolha_usuario == 'papel' and escolha_computador == 'pedra') or \
             (escolha_usuario == 'tesoura' and escolha_computador == 'papel'):
            resultado = 'Você venceu!'
        else:
            resultado = 'Você perdeu!'
    else:
        resultado = 'Jogo cancelado.'

    return render_template('index.html', resultado=resultado)

@app.route('/finalizar', methods=['POST'])
def finalizar():
    vitorias_usuario = 0
    vitorias_computador = 0
    for escolha_usuario, escolha_computador in zip(session['escolhas_usuario'], session['escolhas_computador']):
        if escolha_usuario == escolha_computador:
            pass
        elif (escolha_usuario == 'pedra' and escolha_computador == 'tesoura') or \
             (escolha_usuario == 'papel' and escolha_computador == 'pedra') or \
             (escolha_usuario == 'tesoura' and escolha_computador == 'papel'):
            vitorias_usuario += 1
        else:
            vitorias_computador += 1

    vencedor = 'Empate' if vitorias_usuario == vitorias_computador else 'Você' if vitorias_usuario > vitorias_computador else 'Computador'

    return render_template('resultado.html', vitorias_usuario=vitorias_usuario, vitorias_computador=vitorias_computador, vencedor=vencedor)

if __name__ == '__main__':
    app.run(debug=True)
