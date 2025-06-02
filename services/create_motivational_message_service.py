import os
import json
from google.generativeai import GenerativeModel, configure

class CreateMotivationalMessageService:
    async def execute(
        self,
        name: str,
        how_you_feel_currently: str,
        main_challenges: str,
        goals_dreams: str,
        how_you_handle_emotions: str,
        support_sources: str,
        personal_care: str
    ):
        try:
            # Configure Google Generative AI with API key from environment
            configure(api_key=os.getenv("API_KEY"))
            model = GenerativeModel("gemini-1.5-flash")

            # Construct the prompt as per the requirements
            prompt = (
    f"Gere uma mensagem motivacional personalizada com base apenas nas respostas fornecidas, utilizando versículos e princípios da Bíblia de forma espontânea, extrovertida e acolhedora. "
    f"A mensagem deve utilizar linguagem no artigo masculino, sem termos femininos ou neutros, se referindo à pessoa como 'guerreiro', 'amigo', 'irmão' e similares. "
    f"Use o nome da pessoa na mensagem e crie o texto motivacional levando em conta as respostas dadas para: "
    f"nome: {name}, "
    f"como_voce_se_sente_atualmente: {how_you_feel_currently}, "
    f"principais_desafios: {main_challenges}, "
    f"metas_sonhos: {goals_dreams}, "
    f"como_lida_emocoes: {how_you_handle_emotions}, "
    f"fontes_apoio: {support_sources}, "
    f"cuidados_pessoais: {personal_care}. "
    f"Ignore qualquer outro parâmetro que não esteja listado acima. "
    f"O retorno deve ser apenas um JSON, contendo: "
    f"nome: string com o nome da pessoa, "
    f"mensagem: string com a mensagem motivacional baseada nas respostas e princípios bíblicos, de forma extrovertida, sem acentos nas chaves do JSON."
)

          

            # Generate content using the model (synchronous call, no await)
            response = model.generate_content(prompt)

            if response and response.candidates:
                json_text = response.candidates[0].content.parts[0].text

                # Extract JSON from response (remove markdown code fences)
                json_string = json_text.replace("```json\n", "").replace("\n```", "").strip()
                json_object = json.loads(json_string)

                return json_object
            else:
                raise ValueError("No valid response from the model")

        except Exception as e:
            raise Exception(f"Failed to create motivational message: {str(e)}")