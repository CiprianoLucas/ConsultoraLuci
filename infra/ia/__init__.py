import json
import uuid

import boto3


class IaRepository:
    session: boto3.Session
    agent_id: str
    agent_alias: str

    def __init__(self, session: boto3.Session, agent_id: str, agent_alias: str):
        self.session = session
        self.agent_id = agent_id
        self.agent_alias = agent_alias

    def consultar_cooperado(self, dados: dict) -> str:
        dados_json = json.dumps(dados, ensure_ascii=False)

        client = self.session.client("bedrock-agent-runtime")

        response = client.invoke_agent(
            agentId=self.agent_id,
            agentAliasId=self.agent_alias,
            sessionId=str(uuid.uuid4()),
            inputText=dados_json,
        )

        output_text = '{\n    "colaboradores": ["Caio", "Maria", "João"],\n    "propor": [\n        "soluções práticas e objetivas para necessidades financeiras",\n        "detalhes sobre investimentos em arte",\n        "opções organizadas e estruturadas",\n        "explicações detalhadas sobre produtos financeiros"\n    ],\n    "evitar": [\n        "atendimentos demorados",\n        "comunicação confusa ou imprecisa",\n        "atrasos no atendimento",\n        "abordagens desorganizadas"\n    ]\n}'

        if "completion" in response:
            for event in response["completion"]:
                if "chunk" in event:
                    chunk = event["chunk"]
                    part = chunk.get("bytes", b"").decode("utf-8")
                    output_text += part
        else:
            output_text = response.get("outputText", "")

        resultado_dict = json.loads(output_text)

        return resultado_dict
