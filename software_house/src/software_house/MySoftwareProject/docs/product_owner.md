### Pac-Man Project Backlog

#### User Stories (Prioritized)

1. **User Story 1: Pac-Man Movement Control**
   - **Como** jogador, 
   - **Quero** controlar os movimentos de Pac-Man usando as teclas de seta (ou WASD), 
   - **Para que** eu possa navegar pelo labirinto e coletar pellets.

   **Critérios de Aceitação:**
   - Pac-Man deve responder instantaneamente às entradas do teclado.
   - Pac-Man deve se mover em quadrados discretos conforme a grade do labirinto.
   - O movimento deve ser contínuo até o jogador alterar a direção ou encontrar uma parede.

2. **User Story 2: Coleta de Pellets**
   - **Como** jogador,
   - **Quero** que os pellets desapareçam ao serem coletados,
   - **Para que** eu possa aumentar minha pontuação.

   **Critérios de Aceitação:**
   - Ao mover-se para uma tile com um pellet, o pellet deve desaparecer.
   - A pontuação do jogador deve aumentar em 10 pontos após a coleta de cada pellet.

3. **User Story 3: Coleta de Power Pellets**
   - **Como** jogador,
   - **Quero** que Pac-Man possa coletar Power Pellets para mudar o estado dos fantasmas,
   - **Para que** eu possa ganhar a capacidade de comer fantasmas.

   **Critérios de Aceitação:**
   - Power Pellets devem estar localizados nos quatro cantos do labirinto.
   - Ao coletar um Power Pellet, os fantasmas devem ficar azuis por 7-10 segundos.

4. **User Story 4: Comportamento dos Fantasmas**
   - **Como** jogador,
   - **Quero** que os fantasmas tenham comportamentos diferentes,
   - **Para que** a experiência de jogo seja desafiadora e divertida.

   **Critérios de Aceitação:**
   - Blinky deve sempre perseguir Pac-Man.
   - Pinky deve tentar atacar quatro tiles à frente de Pac-Man.
   - Inky deve usar uma combinação da posição de Pac-Man e Blinky para determinar seu alvo.
   - Clyde deve alternar entre perseguir Pac-Man e vagar aleatoriamente.

5. **User Story 5: Sistema de Pontuação**
   - **Como** jogador,
   - **Quero** ver minhas pontuações aumentarem por várias ações,
   - **Para que** eu possa acompanhar meu desempenho no jogo.

   **Critérios de Aceitação:**
   - A pontuação deve ser aumentada em 50 pontos ao coletar um Power Pellet.
   - A pontuação deve ser aumentada conforme as regras de comer fantasmas em estado aterrorizado.

6. **User Story 6: Ciclo de Vida de Pac-Man**
   - **Como** jogador,
   - **Quero** ter um número limitado de vidas,
   - **Para que** eu possa sentir a pressão durante o jogo.

   **Critérios de Aceitação:**
   - O jogador deve começar com 3 vidas.
   - O jogo deve terminar quando todas as vidas forem perdidas.

7. **User Story 7: Progresso de Níveis**
   - **Como** jogador,
   - **Quero** progredir para níveis mais difíceis,
   - **Para que** o jogo permaneça desafiador.

   **Critérios de Aceitação:**
   - O próximo nível deve ser acessível ao comer todos os pellets e Power Pellets de um nível.
   - A velocidade dos fantasmas deve aumentar com cada nível.

8. **User Story 8: Túnel de Warp**
   - **Como** jogador,
   - **Quero** usar túneis de warp para viajar rapidamente no labirinto,
   - **Para que** eu possa escapar facilmente dos fantasmas.

   **Critérios de Aceitação:**
   - Pac-Man e os fantasmas devem reaparecer no lado oposto do labirinto ao usar os túneis.

### Requisitos Técnicos e Não Técnicos

#### Requisitos Técnicos
1. O jogo deve ser desenvolvido utilizando uma ferramenta de desenvolvimento de jogos (ex: Unity, Godot).
2. Deve haver uma lógica de detecção de colisão entre Pac-Man, fantasmas, pellets, e paredes.
3. Implementação de um algoritmo de pathfinding para comportamento dos fantasmas.
4. Sistema de gerenciamento de estados para Pac-Man e fantasmas (normal, aterrorizado, chase, e scatter).
5. Controle de temporização para o movimento de Pac-Man e fantasmas em intervalos regulares.

#### Requisitos Não Técnicos
1. O design do jogo deve ser intuitivo e fácil de entender para novos jogadores.
2. O jogo deve ter uma apresentação gráfica agradável e bem finalizada.
3. As regras do jogo devem ser claramente explicadas na tela inicial ou em um tutorial.
4. O jogo deve ser testado para garantir a jogabilidade em diferentes dispositivos e resoluções de tela.

### Considerações Finais
Este backlog e os requisitos delineados garantem que o projeto "Pac-Man" esteja alinhado com as expectativas dos stakeholders e que cada funcionalidade esteja claramente definida. O foco em user stories permite que a equipe de desenvolvimento entenda as necessidades do usuário enquanto estabelece critérios de aceitação que facilitam a validação do produto final.