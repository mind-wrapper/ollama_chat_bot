# Ollama Chat Bot

A Django-based chat bot leveraging [Ollama](https://ollama.com/) for natural language processing.

## Features

- Interactive chat interface powered by Django
- Integrates Ollama models for conversational AI
- Extensible for custom chat bot logic and responses
- Open-source under the GNU General Public License v3.0

## Technologies Used

- Python
- Django
- Ollama (LLM backend)

## Setup Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/mind-wrapper/ollama_chat_bot.git
    cd ollama_chat_bot
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Ollama**
    - Ensure you have [Ollama](https://ollama.com/) installed and running.
    - Configure the Django settings or environment variables to point to your Ollama instance.

4. **Run migrations**
    ```bash
    python manage.py migrate
    ```

5. **Start the development server**
    ```bash
    python manage.py runserver
    ```

6. **Access the chat bot**
    - Visit `http://localhost:8000` in your browser.

## Usage

- Simply interact with the chat interface to start a conversation powered by Ollama's language model.
- You can extend the bot by modifying the Django views or integrating new Ollama models.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Author

- [mind-wrapper](https://github.com/mind-wrapper)
