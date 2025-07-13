# RAG LEGO Price Chat Assistant 🧱

A modern chat-based application that uses Retrieval-Augmented Generation (RAG) to provide LEGO set price information. Built with Flask, FastAPI, and CopilotKit, powered by OpenAI (GPT) to deliver intelligent responses about LEGO set prices.

## 🚀 Features

- **Modern Chat Interface**: Built with vanilla CSS and CopilotKit components
- **OpenAI Integration**: Powered by GPT models for intelligent responses
- **RAG-Powered Responses**: AI-generated responses augmented with LEGO price data
- **Multi-Source Data**: Integration with Rebrickable API
- **FastAPI Backend**: High-performance API with automatic documentation
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Gitpod Ready**: One-click cloud development environment
- **Model Indicators**: Visual badges showing which AI model was used
- **Responsive Design**: Beautiful UI that works on all devices

## 📁 Project Structure

```
rag-lego-price/
├── backend/
│   ├── main.py              # FastAPI server with RAG endpoints
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/
│   ├── app.py              # Streamlit web application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Frontend container
├── docker-compose.yml      # Multi-service orchestration
├── .gitpod.yml           # Gitpod development environment
└── README.md             # This file
```

## 🛠️ Technology Stack

### Frontend
- **Streamlit**: Modern web framework for data apps
- **streamlit-chat**: Chat interface components
- **Responsive Design**: Mobile-first approach

### Backend
- **FastAPI**: High-performance web framework
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for FastAPI
- **LangChain**: RAG implementation framework
- **OpenAI API**: Primary LLM (GPT models)

### Data Sources
- **Rebrickable API**: LEGO set information and pricing
- **Mock Data**: Fallback for development and testing

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **Gitpod**: Cloud development environment

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (for cloning the repository)
- OpenAI API key (required for AI responses)

### Option 1: Gitpod (Recommended)

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/rogerolowski/streamlit-rag-alex)

Click the button above to launch the application in Gitpod. The application will automatically start and be available at the provided URL.

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/rogerolowski/streamlit-rag-alex.git
   cd rag-lego-price
   ```

2. **Configure API keys** (see Configuration section below)
   ```bash
   # Create .env file with your API keys
   OPENAI_API_KEY=your_openai_api_key_here
   REBRICKABLE_API_KEY=your_rebrickable_api_key_here
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend (Streamlit): http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Gitpod Development

1. Click the "Open in Gitpod" button above or visit: `https://gitpod.io/#https://github.com/rogerolowski/streamlit-rag-alex`
2. The application will automatically start in the cloud
3. Access the frontend at the provided URL

## 🔧 Configuration Guide

### Required API Keys

#### 1. OpenAI API (Primary LLM)
The application uses OpenAI's GPT models for generating intelligent responses.

**To get your OpenAI API key:**
1. Visit https://platform.openai.com/
2. Sign up for an account
3. Navigate to API Keys section
4. Generate your API key

**Environment Variable:**
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

#### 2. LEGO Data APIs (Future Implementation)
These APIs will be used to fetch real LEGO set data.

**Rebrickable API:**
1. Visit https://rebrickable.com/api/
2. Sign up for an account
3. Get your API key

**Environment Variables:**
```bash
REBRICKABLE_API_KEY=your_rebrickable_api_key_here
```

### Setup Instructions

#### Option 1: Environment Variables (Recommended)

Create a `.env` file in the project root:

```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
REBRICKABLE_API_KEY=your_rebrickable_api_key_here
```

#### Option 2: Docker Compose Environment

Add your API keys to the `docker-compose.yml` file:

```yaml
services:
  backend:
    environment:
      - OPENAI_API_KEY=your_openai_api_key_here
      - REBRICKABLE_API_KEY=your_rebrickable_api_key_here
```

#### Option 3: System Environment Variables

Set the environment variables in your system:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
export REBRICKABLE_API_KEY="your_rebrickable_api_key_here"
```

### Model Priority

The application uses the following priority for AI models:

1. **OpenAI (GPT)** - Primary model (if configured)
2. **Rule-based** - Basic fallback for simple queries

### Testing Your Configuration

1. Start the application: `docker-compose up --build`
2. Open the frontend: http://localhost:8501
3. Check the sidebar for API status indicators
4. Try asking a question to test the AI responses

### Troubleshooting

#### API Not Working
- Verify your API keys are correct
- Check that the environment variables are properly set
- Ensure you have sufficient API credits/quota
- Check the backend logs for error messages

#### Model Not Responding
- The application will fallback to rule-based responses if OpenAI is not configured
- Check the model badge in responses to see which model was used
- Verify API connectivity in the sidebar status

#### Rate Limiting
- OpenAI has rate limits based on your plan
- The application includes error handling for rate limits
- Consider upgrading your API plan if you hit limits frequently

### Security Notes

- Never commit your API keys to version control
- Use environment variables or secure secret management
- Regularly rotate your API keys
- Monitor your API usage to avoid unexpected charges

## 📚 GitHub Repository Setup

To set up your GitHub repository and push your code:

```bash
# Add the remote origin
git remote add origin https://github.com/rogerolowski/streamlit-rag-alex.git

# Rename the branch to main
git branch -M main

# Push to GitHub and set upstream
git push -u origin main
```

**Note**: After pushing to GitHub, you can use the Gitpod launch button above to quickly start the application in the cloud.

## 🔧 API Endpoints

### Backend API (FastAPI)

- `GET /health` - Health check endpoint with API status
- `POST /api/chat` - Chat endpoint for LEGO price queries
- `GET /api/sets/search` - Search for LEGO sets
- `GET /api/sets/{set_number}` - Get specific LEGO set information
- `GET /api/sets` - Get all available LEGO sets

### Frontend (Streamlit)

- Modern chat interface with streamlit-chat components
- Real-time responses with loading states
- Example questions and suggestions
- Error handling and user feedback
- Model indicator badges
- Responsive design for all devices

## 💬 Example Queries

Try asking questions like:
- "What's the price of set 75192-1?"
- "How much does the Millennium Falcon cost?"
- "Tell me about the Titanic set price"
- "What's the current price of the Porsche 911?"
- "Show me Star Wars set prices"

## 🧠 RAG Implementation

The application uses Retrieval-Augmented Generation to:

1. **Query Processing**: Extract set numbers and keywords from user input
2. **Data Retrieval**: Search LEGO databases for relevant set information
3. **Context Building**: Augment responses with retrieved price data
4. **Response Generation**: Use OpenAI GPT to generate natural language responses

### AI Model Priority
1. **OpenAI (GPT)** - Primary model (if configured)
2. **Rule-based** - Basic fallback for simple queries

### Data Sources
- **Rebrickable API**: Primary source for LEGO set information
- **Mock Data**: Development fallback with sample sets

## 🎨 UI/UX Features

### Modern Design
- **Streamlit**: Clean and modern web framework
- **streamlit-chat**: Professional AI chat components
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: Built-in Streamlit animations
- **Model Badges**: Visual indicators for AI model usage

### User Experience
- **Real-time Chat**: Instant message sending and receiving
- **Loading States**: Clear feedback during API calls
- **Error Handling**: User-friendly error messages
- **API Status**: Live monitoring of backend connectivity
- **Example Questions**: Helpful suggestions for users

## 🔮 Future Enhancements

- [ ] **Real API Integration**: Connect to actual Rebrickable API
- [ ] **Enhanced OpenAI Integration**: Support for GPT-4 and other models
- [ ] **Price History**: Track historical price changes
- [ ] **User Authentication**: User accounts and favorites
- [ ] **Price Alerts**: Notifications for price changes
- [ ] **Advanced Filters**: Filter by theme, price range, etc.
- [ ] **Mobile App**: Native mobile application
- [ ] **Dark Mode**: Toggle between light and dark themes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Streamlit, FastAPI, and streamlit-chat
- Powered by OpenAI (GPT) models
- RAG (Retrieval-Augmented Generation) technology
- streamlit-chat for modern AI chat components
- Inspired by the need for better LEGO price discovery
- API integration with Rebrickable

---

**Happy Building! 🧱** 