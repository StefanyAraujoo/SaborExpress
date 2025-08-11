# Criando DB
import os
import sqlite3

caminho_db = 'restaurante_DB.db'

# Verifica se o DB existe caso nao exista o cria e faz os inserts iniciais
if not os.path.exists(caminho_db):
    conexao = sqlite3.connect('restaurante_DB.db')
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurantes (
            id INTEGER PRIMARY KEY,
            nome VARCHAR(200),
            categoria VARCHAR(200),
            ativo INTEGER DEFAULT 0 -- 0 = False, 1 = True        
        )
    ''')

    # restaurantes padroes
    restaurantes_padroes = [{
                    'nome': 'Praça',
                    'categoria': 'Japonesa', 
                    'ativo': False
                },
                {
                    'nome': 'Pizza Suprema', 
                    'categoria': 'Pizza', 
                    'ativo': True
                },
                {
                    'nome': 'Cantina', 
                    'categoria': 'Italiano', 
                    'ativo': False  
                }]
    
    for item in restaurantes_padroes:
        cursor.execute(
            'INSERT INTO restaurantes (nome, categoria, ativo) VALUES (?, ?, ?)',
            (item['nome'], item['categoria'], int(item['ativo']))
        )
    
    conexao.commit()

else:
    conexao = sqlite3.connect('restaurante_DB.db')
    cursor = conexao.cursor()

# Logica do app

def exibir_nome_do_programa():
    print("""𝓢𝓪𝓫𝓸𝓻 𝓔𝔁𝓹𝓻𝓮𝓼𝓼\n""")
    
# Dicionario Global sobre os restaurantes com nome (str), categoria (str) e ativo (true or false)
restaurantes = []

# Function para carregar os restaurantes do DB para o Dicionario Global
def carregar_restaurantes():
    restaurantes.clear()

    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute('SELECT * from restaurantes')
    resultadoQuery = cursor.fetchall()

    for restaurante in resultadoQuery:
        dados_restaurante = {
            'nome': restaurante['nome'], 
            'categoria': restaurante['categoria'], 
            'ativo': bool(restaurante['ativo'])
            }
        restaurantes.append(dados_restaurante)


def exibir_opcoes():
    print('1. Cadastrar restaurante')
    print('2. Listar restaurantes')
    print('3. Alternar estado do restaurante')
    print('4. Deletar um restaurante')
    print('5. Sair\n')

def finalizar_app():
    exibir_subtitulo('Finalizando o app\n')

def voltar_ao_menu_principal():
    input('\nDigite uma tecla para voltar para ao menu principal')
    main()
    
def opcao_invalida():
    print('Opcão invalida')
    voltar_ao_menu_principal()

def exibir_subtitulo(texto):
    os.system('cls')
    linha = '*' * (len(texto))
    print(linha)
    print(texto)
    print(linha)
    print()

def escolher_opcao():
    """
    Função para processar a escolha do usuário no menu
    """

    try:
        opcao_escolhida = int(input('Esclha uma opção: '))

        if opcao_escolhida == 1:
            # print('\nOpção 1 escolhida')
            # voltar_ao_menu_principal()
            cadastrar_novo_restaurante()
        elif opcao_escolhida == 2:
            # print('\nOpção 2 escolhida\n')
            # voltar_ao_menu_principal()
            listar_restaurantes()
        elif opcao_escolhida == 3:
            # print('\nOpção 3 escolhida')
            # voltar_ao_menu_principal()
            alterar_estado_do_restaurante()
        elif opcao_escolhida == 4:
            deletar_restaurante()
        elif opcao_escolhida == 5:
            # print('\nOpção 4 escolhida')
            # voltar_ao_menu_principal()
            finalizar_app()
        else:
            opcao_invalida()
    except:
        opcao_invalida()

# ===========================================

def cadastrar_novo_restaurante():
    """
    Função para cadsatrar um novo restaurante

    Inputs:
    - Nome do restaurante
    - Categoria

    Outputs:
    - Adiciona um novo restaurante à lista de restaurantes
    """

    exibir_subtitulo('Cadastro de novos restaurantes\n')

    nome_do_restaurante = input('Digite o nome do restaurante que deseja cadastrar: ')
    categoria = input(f'Digite o nome da categoria do restaurante {nome_do_restaurante}: ')

    try:
        cursor.execute(
            'INSERT INTO restaurantes (nome, categoria, ativo) VALUES (?, ?, ?)',
            (nome_do_restaurante, categoria, 0)
        )

        conexao.commit()

        dados_do_restaurante = {'nome': nome_do_restaurante, 'categoria': categoria, 'ativo': False}
        restaurantes.append(dados_do_restaurante)
        print(f'O restaurante {nome_do_restaurante} foi cadastrado com sucesso!')

    except sqlite3.Error as e:
        print("Erro ao inserir:", e)
        conexao.rollback()  # desfaz alterações feitas na transação atual

    voltar_ao_menu_principal()


def listar_restaurantes():
    """
    Função para listar todos os restaurantes cadastrados
    """

    exibir_subtitulo('Listando os restaurantes')

    print(f'{'Nome do Restaurante'.ljust(31)} | {'Categoria'.ljust(30)} | Status')
    for restaurante in restaurantes:
        nome_restaurante = restaurante['nome']
        categoria = restaurante['categoria']
        ativo = 'Ativado' if restaurante ['ativo'] else 'Desativado'
        print(f'-{nome_restaurante.ljust(30)} | -{categoria.ljust(30)}| -{ativo}')

    voltar_ao_menu_principal()

def alterar_estado_do_restaurante():
    """
    Função para ativar ou desativar um restaurante
    """
    exibir_subtitulo('Alterando o estado do restaurante\n')
    nome_restaurante = input('Digite o nome do restaurante que deseja alterar o estado: ')
    restaurante_encontrado = False

    for restaurante in restaurantes:
        if nome_restaurante == restaurante['nome']:
            restaurante_encontrado = True

            try:
                cursor.execute(
                    'UPDATE restaurantes SET ativo = 1 - ativo WHERE nome = ?',
                    (nome_restaurante,)
                )

                conexao.commit()
                restaurante['ativo'] = not restaurante['ativo']

                print(f'O restaurante {nome_restaurante} foi ativado com sucesso!' if restaurante['ativo'] else f'O restaurante {nome_restaurante} foi desativado com sucesso!')

            except sqlite3.Error as e:
                print("Erro ao mudar:", e)
                conexao.rollback()  # desfaz alterações feitas na transação atual
            break
    
    if not restaurante_encontrado:
        print('O restaurante não foi encontrado!')

    voltar_ao_menu_principal()

def deletar_restaurante():
    """
    Função para deletar um restaurante
    """
    exibir_subtitulo('Deletando um restaurante')
    nome_restaurante = input('Digite o nome do restaurante que deseja deletar: ')
    restaurante_encontrado = False

    for restaurante in restaurantes:
        if nome_restaurante == restaurante['nome']:
            restaurante_encontrado = True
            deletar = input(f'Você tem certeza que deseja deletar o restaurante {nome_restaurante}?\nResponda:\nSim ou Não\n')

            if deletar.lower() == 'Sim'.lower():
                try:
                    cursor.execute(
                        'DELETE FROM restaurantes WHERE nome = ?',
                        (nome_restaurante,)
                    )

                    conexao.commit()

                    restaurantes.remove(restaurante)
                    mensagem = f'O restaurante {nome_restaurante} foi deletado com sucesso!'

                except sqlite3.Error as e:
                    print("Erro ao inserir:", e)
                    conexao.rollback()  # desfaz alterações feitas na transação atual

            elif deletar.lower() == 'Não'.lower():
                mensagem = 'Operação cancelada'
            else:
                mensagem = 'Opção invalida'
            
            print(mensagem)
    if not restaurante_encontrado:
        print('O restaurante não foi encontrado!')

    voltar_ao_menu_principal()

def main():
    """
    Função principal que inicia o programa
    """

    os.system('cls')
    carregar_restaurantes()
    exibir_nome_do_programa()
    exibir_opcoes()
    escolher_opcao()
    

if __name__ == '__main__':
    main()