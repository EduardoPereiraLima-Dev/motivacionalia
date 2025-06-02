from pydantic import BaseModel, Field

class MotivationalMessageRequest(BaseModel):
    name: str
    how_you_feel_currently: str = Field(alias="como_voce_se_sente_atualmente")
    main_challenges: str = Field(alias="principais_desafios")
    goals_dreams: str = Field(alias="metas_sonhos")
    how_you_handle_emotions: str = Field(alias="como_lida_emocoes")
    support_sources: str = Field(alias="fontes_apoio")
    personal_care: str = Field(alias="cuidados_pessoais")

    class Config:
        validate_by_name = True
