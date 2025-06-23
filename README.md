# Medical Research Report Writer

This script uses OpenAI's API to help generate academic medical research content. It transforms user input into research questions using the PICO framework and generates introduction sections suitable for peer-reviewed medical journals.

## Features

- **Research Question Generation**: Converts user input into structured research questions using the PICO framework
- **Academic Introduction Writing**: Generates formal introduction sections with proper citations for medical research papers
- **Professional Output**: Formatted for submission to leading medical journals (NEJM, The Lancet, JAMA, BMJ, Nature Medicine)

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API Key**
   Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

3. **Run the Script**
   ```bash
   python main.py
   ```

## How It Works

1. **Input**: Enter your research topic or question
2. **PICO Framework**: The script converts your input into a structured research question using:
   - **P**opulation: Who is being studied?
   - **I**ntervention: What is being tested?
   - **C**omparison: What is it compared to?
   - **O**utcome: What are the measured results?
3. **Introduction Generation**: Creates a 500-800 word academic introduction with 15-20 citations

## Output

The script generates two main outputs:
- A structured research question based on your input
- A complete introduction section ready for academic submission

## Recent Fixes

- Updated to use the modern OpenAI API (v1.0+)
- Fixed model name from "gpt-4.1" to "gpt-4" 
- Changed invalid "developer" role to "system"
- Fixed string interpolation for proper variable substitution
- Added proper error handling for both API calls
- Enhanced output formatting with clear section headers

## Getting an OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Add it to your `.env` file

## Repository

This project is hosted at: https://github.com/mustafa-boorenie/report_writer.git 