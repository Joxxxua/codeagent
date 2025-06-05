import os
import sys
from dotenv import load_dotenv
from autogen import (
    AssistantAgent,
    UserProxyAgent,
    GroupChat,
    GroupChatManager
)

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()


llm_config = {
    "model": "gpt-4", 
    "api_key": os.getenv("OPENAI_API_KEY"),
    "temperature": 0.2
}


coder = AssistantAgent(
    name="Coder",
    system_message="Você é um programador Python. Escreva o código com base na tarefa, e corrija se houver falhas.",
    llm_config=llm_config,
    human_input_mode="NEVER",  
    is_termination_msg=lambda x: "fim" in x.get("content", "").lower()
)


executor = AssistantAgent(
    name="Executor",
    system_message="Você executa o código fornecido e mostra a saída real da execução.",
    llm_config=llm_config,
    code_execution_config={"work_dir": "autogen_workspace", "use_docker": False},
    human_input_mode="NEVER"
)


reviewer = AssistantAgent(
    name="Reviewer",
    system_message="Você revisa o código e a saída da execução. Se houver erros ou melhorias, peça ajustes ao programador.",
    llm_config=llm_config,
    human_input_mode="NEVER"
)


user = UserProxyAgent(
    name="Usuário",
    code_execution_config=False,
    system_message="Você pede tarefas aos agentes.",
)


groupchat = GroupChat(
    agents=[user, coder, executor, reviewer],
    messages=[],  
    max_round=2
)


manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config  
)


user.initiate_chat(
    manager,
    message="Escrevam um código Python que calcule a média de uma lista de números e mostre o resultado. Validem se o valor está correto após execução."
)
    