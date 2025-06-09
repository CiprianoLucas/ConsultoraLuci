import json
import re

from aiobotocore.session import get_session

from infra.ia.model import claude3p7


class IaRepository:
    def __init__(self, iam_aws_key: str, iam_aws_pass: str):
        self.iam_aws_key = iam_aws_key
        self.iam_aws_pass = iam_aws_pass

    async def enviar_pergunta(self, data: str) -> str:
        session = get_session()
        async with session.create_client(
            "bedrock-runtime",
            region_name="us-east-1",
            aws_access_key_id=self.iam_aws_key,
            aws_secret_access_key=self.iam_aws_pass,
        ) as client:

            payload = json.loads(json.dumps(claude3p7))
            payload["messages"][1]["content"][0]["text"] = json.dumps(data)

            try:
                response = await client.invoke_model(
                    modelId=(
                        "arn:aws:bedrock:us-east-1:381492098067:inference-profile"
                        "/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
                    ),
                    contentType="application/json",
                    accept="application/json",
                    body=json.dumps(payload),
                )

                body_bytes = await response["body"].read()
                body = json.loads(body_bytes)
                resposta = body["content"][0]["text"]

                matches = re.findall(r"\{.*?\}", resposta, re.DOTALL)
                resultado_dict = json.loads(matches[0])

            except Exception:
                resultado_dict = {"colaboradores": [], "propor": [], "evitar": []}

            return resultado_dict
