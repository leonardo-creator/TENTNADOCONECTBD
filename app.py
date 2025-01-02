from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# Conexão com o banco de dados
DB_CONN = "postgresql://postgres:7sw0F2MNx0ObN32g@singly-light-topi.data-1.use1.tembo.io:5432/postgres"

# Criar a aplicação FastAPI
app = FastAPI()

# Modelo de resposta para os dados
class DadoBarragem(BaseModel):
    barragem: str
    data_e_hora: str
    nivel_m: float
    volume_mm: float

# Endpoint para obter todos os dados
@app.get("/dados", response_model=List[DadoBarragem])
async def get_dados():
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(DB_CONN)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Executar a query para obter os dados
        query = """
        SELECT 
            barragem AS barragem,
            "Data e Hora" AS data_e_hora,
            "Nível (m)" AS nivel_m,
            "Volume (mm)" AS volume_mm
        FROM dados_barragens
        """
        cursor.execute(query)
        dados = cursor.fetchall()

        # Fechar conexão
        cursor.close()
        conn.close()

        # Retornar os dados como lista de dicionários
        return dados

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados: {e}")
