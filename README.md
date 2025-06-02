Motivacionalia
Motivacionalia is a FastAPI-based Python application that generates personalized motivational messages using biblical principles and the Google Gemini API. It accepts user inputs such as name, feelings, challenges, goals, and support sources, delivering uplifting messages in a JSON format.
Project Structure
motivacionalia/
├── main.py
├── routes.py
├── models/
│   └── motivational_message.py
├── services/
│   └── create_motivational_message_service.py
├── scripts/
│   └── script.py
├── .env
├── .gitignore
└── README.md

Prerequisites

Python 3.12.4
Virtual environment (recommended)
Google Gemini API key

Setup

Clone the repository (if applicable):
git clone <repository-url>
cd motivacionalia


Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install fastapi uvicorn python-dotenv google-generativeai pydantic


Configure environment variables:Create a .env file in the project root with:
API_KEY=your_google_gemini_api_key
PORT=3333
HOST=0.0.0.0

Replace your_google_gemini_api_key with your actual Gemini API key.


Running the Application

Start the FastAPI server:
python main.py

The server will run at http://localhost:3333.

Test the API:Use a tool like Thunder Client, Postman, or curl to test the endpoints.

GET /teste: Returns a sample motivational message.
curl http://localhost:3333/teste

Expected response:
{
  "data": {
    "nome": "Ana",
    "mensagem": "Ei, Ana! Deus está contigo em cada passo! 'Tudo posso naquele que me fortalece' (Filipenses 4:13). Continue brilhando!"
  }
}


POST /create: Generates a personalized motivational message.
curl -X POST http://localhost:3333/create \
-H "Content-Type: application/json" \
-d '{
      "name": "João",
      "how_you_feel_currently": "Cansado, mas motivado",
      "main_challenges": "Conciliar estudos e trabalho",
      "goals_dreams": "Ser um engenheiro de software",
      "how_you_handle_emotions": "Oro e converso com amigos",
      "support_sources": "Família e igreja",
      "personal_care": "Leio a Bíblia e corro"
    }'

Expected response:
{
  "nome": "João",
  "mensagem": "Olá, João! Deus te capacita para superar os desafios! 'Esforcem-se e tenham bom ânimo' (Josué 1:9). Com tua fé, apoio da família e corrida, vais conquistar teu sonho de ser engenheiro!"
}





Testing with Thunder Client

Open Thunder Client in VS Code.
Create a GET request to http://localhost:3333/teste.
Create a POST request to http://localhost:3333/create with the JSON body above.
Send the requests and verify the responses.

Running the Test Script
To test the service directly:
python scripts/script.py

Troubleshooting

ModuleNotFoundError: Ensure all dependencies are installed (pip install -r requirements.txt if you create one).
API key errors: Verify the .env file has a valid Gemini API key.
Connection issues: Confirm the server is running and the port (3333) is not blocked.

Contributing
Feel free to submit issues or pull requests to improve the project.
License
This project is unlicensed and free to use.
