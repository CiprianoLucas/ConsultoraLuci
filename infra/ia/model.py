claude3p7 = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 500,
    "top_k": 250,
    "temperature": 1,
    "top_p": 0.999,
    "stop_sequences": [],
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Receberá um JSON com informações sobre cooperados e colaboradores. "
                        "A tarefa é analisar os critérios fornecidos para determinar a ordem de melhor vendedor para atender ao cooperado, "
                        "além de identificar assuntos a abordar e evitar. Forneça a resposta em formato JSON.\n\n"
                        "## Análise dos Critérios\n\n"
                        "- Avalie as personalidades dos colaboradores em relação à personalidade do cooperado.\n"
                        "- Compare os créditos concedidos anteriormente e os tipos de compras realizadas.\n"
                        "- Considere feedbacks que os colaboradores deram sobre o cooperado a fim de o próximo colaborador ficar melhor alinhado com o propósito do cooperado.\n"
                        "- Observe a experiência e o histórico de créditos dos colaboradores, com relação a semelhança de créditos e também com as personalidades dos outros clientes do colaborador.\n\n"
                        "## Resposta\n\n"
                        "- Liste os colaboradores em ordem de aptidão para atender ao cooperado.\n"
                        "- Inclua sugestões de assuntos a abordar e quais evitar, baseado nas personalidades e histórico de interações.\n\n"
                        "# Output Format\n\n"
                        "O resultado deve ser um JSON estruturado. Inclua as seguintes chaves:\n"
                        '- "colaboradores": uma lista de colaboradores na ordem de adequação.\n'
                        '- "propor": tópicos sugeridos para conversar com o cooperado.\n'
                        '- "evitar": tópicos que devem ser evitados.\n\n'
                        "# Exemplo\n\n"
                        "**Input** (modelo fornecido no JSON):\n\n"
                        "{\n"
                        '    "cooperado": {\n'
                        '        "personalidade": ["personalidade"],\n'
                        '        "creditos": [\n'
                        '            {"motivo": "Descrição do motivo", "valor": 0.01}\n'
                        "        ],\n"
                        '        "compras": [\n'
                        '            {"segmento": "comida", "valor": 0.01}\n'
                        "        ],\n"
                        '        "feedbacks": ["feedbacks anteriores na agencia"],\n'
                        '        "nascimento": "2025-01-01"\n'
                        "    },\n"
                        '    "colaboradores": [\n'
                        "        {\n"
                        '            "nome": "Colaborador 1",\n'
                        '            "personalidades": ["personalidade"],\n'
                        '            "creditos": [\n'
                        "                {\n"
                        '                    "cooperado": 1, "valor": 509.96,\n'
                        '                    "motivo": "Comprar um controle",\n'
                        '                    "personalide cooperado": "Organizado, Proativo, Apreciador de arte"\n'
                        "                }\n"
                        "            ]\n"
                        "        },\n"
                        "        {\n"
                        '            "nome": "Colaborador 2",\n'
                        '            "personalidades": [],\n'
                        '            "creditos": []\n'
                        "        }\n"
                        "    ]\n"
                        "}\n\n"
                        "**Output**:\n\n"
                        "{\n"
                        '    "colaboradores": ["Colaborador 1", "Colaborador 2"],\n'
                        '    "propor": ["organização", "arte"],\n'
                        '    "evitar": ["compras sem planejamento"]\n'
                        "}\n\n"
                        "# Notes\n\n"
                        "- Considere personalidades e experiências semelhantes entre colaborador e cooperado para melhor compatibilidade.\n"
                        "- Priorize colaboradores com personalidades e históricos de crédito semelhante ao cooperado.\n"
                        "- Mantenha um tom profissional e objetivo em suas recomendações."
                    ),
                }
            ],
        },
        {"role": "user", "content": [{"type": "text", "text": None}]},
    ],
}
