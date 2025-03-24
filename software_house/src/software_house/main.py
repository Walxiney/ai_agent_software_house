#!/usr/bin/env python
import sys
import warnings

from crew import SoftwareHouse

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'project_name': """AI-Powered To-Do List""",
        'project_description': """Um sistema de To-Do List moderno com uma API REST,
        interface frontend interativa e funcionalidades avançadas.',
        
        Features:
        - Adicionar, editar e excluir tarefas,
        - Marcar tarefas como concluídas,
        - Filtrar e ordenar tarefas por data e prioridade,
        - Autenticação de usuários,
        - Persistência de dados em um banco de dados relacional
        
        Tech_stack:
        - frontend: React.js,
        - backend: FastAPI (Python),
        - database: PostgreSQL,
        - authentication: JWT
        
        Documentation_requirements:
        - Guia de instalação e configuração,
        - API documentation usando Swagger/OpenAPI,
        - Guia do usuário para a interface web
        """
    }


    SoftwareHouse().crew().kickoff(inputs=inputs)



def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        SoftwareHouse().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SoftwareHouse().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        SoftwareHouse().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

if __name__ == "__main__":
    run()
    #train()
    #replay()
    #test()