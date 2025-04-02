# Arquitetura do Software para o Projeto "Pacman"

## Visão Geral

A arquitetura do software para o jogo "Pacman" será composta por um sistema modular e escalável, que separa as responsabilidades em diferentes camadas: frontend, backend, e banco de dados. Esta abordagem permite um desenvolvimento mais contínuo e organizado, além de facilitar a manutenção e a escalabilidade.

### Camadas

1. **Frontend**:
    - **Tecnologia**: React.js (ou similar)
    - **Função**: Responsável pela interface gráfica com o usuário. Utiliza a biblioteca React para construir uma UI interativa e responsiva, permitindo que o jogador veja o labirinto e controle Pac-Man.
    - **Módulos**:
        - Tela de Inicialização
        - Labirinto/Layout
        - Pontuação
        - Game Over

2. **Backend**:
    - **Tecnologia**: Python com Flask ou FastAPI
    - **Função**: Lida com a lógica do jogo, gerenciamento de estado, e comunicação com o frontend. Este será responsável pelo gerenciamento de estados de Pac-Man e fantasmas, detecção de colisão, e progressão de níveis.
    - **Módulos**:
        - Gerenciamento de Jogo (estado, pontuação, vidas)
        - Comportamento dos Fantasmas
        - Conexão com Banco de Dados
        - API REST para comunicação com o frontend

3. **Banco de Dados**:
    - **Tecnologia**: SQLite ou PostgreSQL
    - **Função**: Armazena dados relacionados a pontuações, níveis e perfis de jogadores (se necessário).
    - **Estrutura**:
        - Tabela de Usuários (id, score, level, etc.)
        - Tabela de Partidas (id, user_id, game_data, etc.)

### Diagramas UML

1. **Diagrama de Casos de Uso**

   ```plaintext
   +-----------------------+
   |       Jogador         |
   +-----------------------+
              |
              | inicia jogo
              v
   +-----------------------+
   |      Jogo            |
   +-----------------------+
   | -Inicio              |
   | -Game Loop           |
   | -Detectar Colisão    |
   | -Gerenciar Estado     |
   +-----------------------+
   ```

2. **Diagrama de Classes**

   ```plaintext
   +-----------------------+          +-----------------------+
   |       PacMan         |<---------|      Ghost            |
   +-----------------------+          +-----------------------+
   | -x: int              |          | -x: int              |
   | -y: int              |<---------| -y: int              |
   | -lives: int          |          | -state: String       |
   | -score: int          |          +-----------------------+
   | +move()              |          | +move()              | 
   | +eatPellet()         |          | +updateBehavior()     |
   +-----------------------+          +-----------------------+
   ```

3. **Diagrama de Sequência**

   ```plaintext
   Jogador -> Frontend: Iniciar Jogo
   Frontend -> Backend: Carregar Estado
   Backend -> Banco de Dados: Recuperar Dados
   Banco de Dados -> Backend: Dados do Jogo
   Backend -> Frontend: Enviar Estado Atual
   Frontend -> Jogador: Exibir Jogo
   ```

### Justificativa das Escolhas Tecnológicas e Padrões Adotados

- **React.js** no frontend foi escolhido pelas suas capacidades de construir interfaces dinâmicas de forma eficiente e reutilizável.
- **Python** como linguagem backend foi escolhido pela sua simplicidade e pelo suporte a frameworks robustos como Flask e FastAPI, que facilitam a construção de APIs RESTful.
- **SQLite** ou **PostgreSQL** são escolhas adequadas para o banco de dados, fornecendo robustez e desempenho, além de eliminar a complexidade de configuração.

### Plano para Comunicação Eficiente entre Componentes e Fluxo de Dados

- **APIs RESTful** serão utilizadas para permitir a comunicação entre o frontend e o backend. O backend irá fornecer endpoints para iniciar o jogo, recuperar o estado do jogo, e atualizar a pontuação.
- **Websockets** podem ser considerados para uma comunicação em tempo real, especialmente se futuramente decidirmos incluir modos multiplayer.

### Estrutura de Dados para o Jogo

- O labirinto é representado por uma matriz bidimensional. Cada célula contém informações sobre o tipo de tile (parede, pellet, power pellet, etc.).
- Os estados de Pac-Man e dos fantasmas serão geridos por um sistema de gerenciamento centralizado, utilizando um padrão de projeto de estado, permitindo transitions entre os diferentes modos (Chase, Scatter, Frightened).

## Conclusão

A arquitetura proposta oferece uma solução robusta para o desenvolvimento do jogo "Pacman", atendendo aos requisitos funcionais e não funcionais estabelecidos, enquanto garante modularidade, escalabilidade e segurança. A divisão clara entre as camadas facilita o fluxo de dados e a manutenção do sistema, permitindo um desenvolvimento ágil e eficiente.