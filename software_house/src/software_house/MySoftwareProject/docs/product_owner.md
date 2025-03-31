**Backlog do Projeto Dropoff Detection System**

**Visão Geral do Escopo do Projeto**  
O Dropoff Detection System é uma aplicação web projetada para validar se um pacote foi entregue no local correto. Os usuários podem inserir uma descrição do local onde o pacote foi deixado e carregar uma imagem desse local. O sistema utilizará um modelo de linguagem da OpenAI para comparar a descrição com a imagem e retornará uma mensagem indicando se a entrega é válida ou não.

---

### **Requisitos do Projeto**

**Funcionalidades do Frontend**  
1. Título da aplicação: "Dropoff Detection System".
2. Caixa de texto para o usuário inserir a descrição do local.
3. Botão para carregar a imagem do local onde o pacote foi deixado.
4. Botão para visualizar/imagem carregada (toggle).
5. Botão para rodar a verificação da imagem em relação à descrição.
6. Mensagem de retorno – "Valid" ou "Invalid", posicionada de forma visível.
7. Botão tipo expandir/recolher para visualizar a explicação sobre a análise.

---

**Funcionalidades do Backend**  
1. Desenvolver o backend usando Python e FastAPI.
2. Receber mensagens de texto e imagem.
3. Realizar o encoding da imagem em base64.
4. Utilizar a API da OpenAI com o modelo GPT-4o para validação.
5. Implementar regras detalhadas de análise baseada na descrição e imagem.
6. Garantir que só imagens sem pessoas e pacotes visíveis sejam consideradas válidas.
7. Documentar o código e garantir boas práticas de programação.

---

### **Histórias de Usuário**

1. **Como um usuário**, quero inserir a descrição do local do pacote, para que eu possa validar a entrega.
   - **Critérios de Aceitação**:
     - A caixa de texto deve estar disponível e visível.
     - O texto deve ser aceito e armazenado para validação.

2. **Como um usuário**, quero carregar uma imagem do local do pacote, para que o sistema a valide contra a descrição que forneci.
   - **Critérios de Aceitação**:
     - O botão de upload deve aceitar formatos de imagem .png, .jpeg, .jpg e .webp.
     - A imagem deve ser carregada e exibida corretamente.

3. **Como um usuário**, quero que o sistema valide se o pacote foi entregue no local correto, para que eu saiba se a entrega é válida.
   - **Critérios de Aceitação**:
     - O sistema deve retornar "Valid" ou "Invalid" com base na validação.
     - A mensagem deve ser posicionada de forma visível na interface.

4. **Como um usuário**, quero visualizar a explicação da análise feita pelo sistema, para entender o motivo da validação.
   - **Critérios de Aceitação**:
     - Ao expandir a seção de explicação, uma resposta descritiva deve ser exibida.
     - O conteúdo deve formatar a análise e o raciocínio por trás da resposta "Valid" ou "Invalid".

---

### **Documentação Requerida**

1. **Guia de Instalação e Configuração**:
   - Passos para configurar o ambiente local para execução da aplicação.
   - Dependências necessárias e como instalá-las.

2. **Documentação da API**:
   - Detalhes sobre os endpoints do FastAPI.
   - Formatos de requisições e respostas.

3. **Guia do Usuário para a Interface Web**:
   - Instruções sobre como utilizar o sistema.
   - Exemplos de entradas e resultados esperados.

4. **Organização de Pastas e Guia para Execução do Código**:
   - Estrutura proposta de diretórios.
   - Como executar o servidor e acessar a aplicação.

---

### **Prioridade do Backlog:**

1. Desenvolvimento da interface do usuário (UI) e a experiência do usuário (UX).
2. Implementação da lógica do backend e integração com a API da OpenAI.
3. Criação de documentação abrangente para facilitar a utilização e manutenção do sistema.
4. Realização de testes para garantir a eficácia da validação de entregas.

---

Assim, este backlog oferece uma base sólida para começar o desenvolvimento do Dropoff Detection System, alinhando os requisitos técnicos com as expectativas do cliente. A organização e priorização deste backlog fornecerão um caminho claro para as etapas futuras do projeto.