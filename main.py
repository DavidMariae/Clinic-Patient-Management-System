from src.controllers.clinica_controller import ClinicaController
from src.ui.janela_principal import JanelaPrincipal

if __name__ == "__main__":
    # 1. Inicia o cérebro
    controller = ClinicaController()

    # 2. Inicia a interface passando o cérebro para ela
    app = JanelaPrincipal(controller)

    # 3. Roda o sistema
    app.mainloop()
