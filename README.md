# Search and Rescue (SAR) Agent Framework - CSC 581

## Introduction

The First Aid Agent helps with providing first aid guidance and assessing medical triage levels. It can also combine a first aid query with a given triage level assessed and give a combined output. The agent has access to two data sources (in the knowledge directory):
1. A json file consisting of possible first aid questions and their answers which are answered using fuzzy matching using difflib
2. A csv file consisting of patient info and assessed triage levels 

The agent uses OpenAI's API key to access the LLM to assess a triage level and provide a combined answer. 
## Insights

After reviewing the feedback given, I learned that there are several areas for improvement, most of them relating to inline documentation, logging, and error handling. 
The feedback highlighted that while the core functionality was present and functional, the error handling around external API (OpenAI) calls was minimal. Given this, I learned that I should handle API-related or network-related errors more gracefully so the user understands the status of the system instead of being confused about any time-outs. I also recognized the need to provide meaningful fallback behaviors when input data (from the CSV and JSON files) is incomplete.
The feedback also pointed out certain edge cases I could cover in my test, such as no matching intent found or any missing CSV fields, which would be helpful for me as the developer to know if something goes wrong.
Additionally, while my test cases cover basic functionality, the feedback suggested that I could expand the coverage by mocking the OpenAI API responses in tests to avoid depending on the API again while testing, which is a great idea since it reduces the usage of API calls numerous times and saves money for me. 

## Modifications

Based on the feedback, I did the following:
Added more inline documentation. This could be useful if I or anyone else continues the project in the future and also allows for easy understanding of the code’s functionality. 
Added logging for core functionalities as well as to catch any errors
Updated return statements for errors
Added more test coverage and handled cases where files aren’t found


## How to Submit
Please submit a link to your clone of the repository to Canvas. 

## Prerequisites

- Python 3.8 or higher
- pyenv (recommended for Python version management)
- pip (for dependency management)

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sar-project
```

2. Set up Python environment:
```bash
# Using pyenv (recommended)
pyenv install 3.9.6  # or your preferred version
pyenv local 3.9.6

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

4. Configure environment variables:

#### OpenAI:
- Obtain required API keys:
  1. OpenAI API key: Sign up at https://platform.openai.com/signup
- Update your `.env` file with the following:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
#### Google Gemini:
- Obtain required API keys:
  1. ``` pip install google-generativeai ```
  2. ``` import google.generativeai as genai ```
  3. Google Gemini API Key: Obtain at https://aistudio.google.com/apikey
- Configure with the following:
  ```
  genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
  ```

Make sure to keep your `.env` file private and never commit it to version control.

## Project Structure

```
sar-project/
├── src/
│   └── sar_project/         # Main package directory
│       └── agents/          # Agent implementations
│       └── config/          # Configuration and settings
│       └── knowledge/       # Knowledge base implementations
├── tests/                   # Test directory
├── pyproject.toml           # Project metadata and build configuration
├── requirements.txt         # Project dependencies
└── .env                     # Environment configuration
```

## Development

This project follows modern Python development practices:

1. Source code is organized in the `src/sar_project` layout
2. Use `pip install -e .` for development installation
3. Run tests with `pytest tests/`
4. Follow the existing code style and structure
5. Make sure to update requirements.txt when adding dependencies


## FAQ

### Assignment Questions

**Q: How do I choose a role for my agent?**

**A:** Review the list of SAR roles above and consider which aspects interest you most. Your agent should provide clear value to SAR operations through automation, decision support, or information processing.

**Q: What capabilities should my agent have?**

**A:** Your agent should handle tasks relevant to its role such as: data processing, decision making, communication with other agents, and providing actionable information to human operators.

**Q: Can I add new dependencies?**

**A:** Yes, you can add new Python packages to requirements.txt as needed for your implementation.


### Technical Questions

**Q: Why am I getting API key errors?**

**A:** Ensure you've properly set up your .env file and obtained valid API keys from the services listed above.

**Q: How do I test my agent?**

**A:** Use the provided test framework in the tests/ directory. Write tests that verify your agent's core functionality.

**Q: Can I use external libraries for my agent?**

**A:** Yes, you can use external libraries as long as they are compatible.
