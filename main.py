import customtkinter as ctk  # Biblioteca de interface gráfica
from config import APPEARANCE_MODE, COLOR_THEME

# Importa as duas janelas principais do sistema
from src.ui.janela_principal import JanelaPrincipal   # Janela do sistema após login
from src.ui.login_view       import LoginView         # Tela de autenticação


# if __name__ == "__main__" garante que este bloco só execute quando o arquivo for rodado diretamente (python main.py) e NÃO quando for importado por outro arquivo.

if __name__ == "__main__":

    # Define o tema visual antes de criar qualquer janela
    # Precisa ser chamado antes do CTk() — ordem importa
    ctk.set_appearance_mode(APPEARANCE_MODE)  # "light" = fundo claro
    ctk.set_default_color_theme(COLOR_THEME)  # Tema base do CustomTkinter

    # Cria a janela RAIZ — obrigatória para o CTkToplevel (LoginView) funcionar
    # O CTkToplevel sempre precisa de uma janela pai existindo
    root = ctk.CTk()

    # Esconde a janela raiz — não queremos mostrá-la, só precisamos que exista
    # O usuário verá apenas o Login e depois a Janela Principal
    root.withdraw()

    # Cria e exibe a tela de login
    login = LoginView()

    # grab_set() bloqueia interação com outras janelas enquanto o login está aberto
    # O usuário não consegue "escapar" para outra parte do sistema
    login.grab_set()

    # Pausa a execução AQUI até que a janela de login seja fechada
    # Quando o usuário autenticar ou fechar, o código continua abaixo
    root.wait_window(login)

    # Verifica se o login foi bem-sucedido
    # login.usuario_logado é None se o usuário fechou sem autenticar
    usuario = login.usuario_logado

    if not usuario:
        # Usuário fechou o login sem autenticar — encerra o sistema
        root.destroy()
    else:
        # Login bem-sucedido — cria a janela principal passando o usuário
        # O usuário logado será exibido no footer da sidebar
        app = JanelaPrincipal(usuario=usuario)

        # Inicia o loop de eventos — mantém a janela aberta e responsiva
        # É aqui que o sistema "fica rodando" até o usuário fechar
        app.mainloop()