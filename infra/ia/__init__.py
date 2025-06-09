import json
import re
import uuid
import time
import boto3


class IaRepository:
    session: boto3.Session
    agent_id: str
    agent_alias: str

    def __init__(self, session: boto3.Session, agent_id: str, agent_alias: str):
        self.session = session
        self.agent_id = agent_id
        self.agent_alias = agent_alias

    def consultar_associado(self, dados: dict) -> str:
        dados_json = json.dumps(dados, ensure_ascii=False)

        client = self.session.client("bedrock-agent-runtime")

        output_text = ""

        # return {
        #     "colaboradores": ["Colaborador 1", "Colaborador 2"],
        #     "propor": ["organização", "arte"],
        #     "evitar": ["compras sem planejamento"],
        # }
        response = client.invoke_agent(
            agentId=self.agent_id,
            agentAliasId=self.agent_alias,
            sessionId=str(uuid.uuid4()),
            inputText=dados_json,
        )
        time.sleep(10)
        try:
            if "completion" in response:
                for event in response["completion"]:
                    time.sleep(10)
                    if "chunk" in event:
                        chunk = event["chunk"]
                        part = chunk.get("bytes", b"").decode("utf-8")
                        output_text += part
            else:
                output_text = response.get("outputText", "")

            matches = re.findall(r"\{.*?\}", output_text, re.DOTALL)
            resultado_dict = json.loads(matches[0])
        except Exception:
            resultado_dict = {
                "colaboradores": [],
                "propor": [],
                "evitar": [],
                "ia": output_text or "Me desculpe! Buguei ;(",
            }

        return resultado_dict
