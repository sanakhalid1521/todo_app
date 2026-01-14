# Todo App Setup Instructions

## Setting up OpenAI API Key

To enable the AI chatbot functionality, you need to add your OpenAI API key to the environment variables.

### Steps:

1. Get your OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)

2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

3. If you don't have a `.env` file, copy the example:
   ```bash
   cp .env.example .env  # if you have an example file
   ```

   Or create/edit the `.env` file directly:
   ```bash
   nano .env
   ```

4. Add your OpenAI API key to the `.env` file:
   ```env
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

5. Save the file and restart your backend server.

### Alternative (Using Mock Responses):
If you don't have an OpenAI API key, the application will automatically fall back to mock responses that simulate AI functionality. The chatbot will still work with natural language processing but without the advanced AI capabilities.

### Example .env file:
```env
DATABASE_URL=your_database_url_here
OPENAI_API_KEY=your_openai_api_key_here  # Leave empty to use mock responses
```

## Running the Application

### Backend (FastAPI):
```bash
cd backend
pip install -r requirements.txt  # if you have a requirements file
uvicorn main:app --reload
```

### Frontend (Next.js):
```bash
cd frontend
npm install
npm run dev
```

The chatbot will be accessible through the floating chat icon on the frontend.