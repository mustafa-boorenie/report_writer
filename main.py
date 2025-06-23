from openai import OpenAI
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Initialize OpenAI client and rich console
client = OpenAI()
console = Console()

user_input = input("Enter a input: ")
research_question = ""

# Make an API call for the research question
try:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": f"turn this input into a prompt for a LLM with the instructions: 'You are an expert prompt engineer specializing in creating prompts for research purposes. You are given a input which you will need to rephrase into a research input within the context of medical research using the PICO framework. The input is: {user_input}'"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    # Get the assistant's reply
    console.print("\n[bold cyan]RESEARCH QUESTION:[/bold cyan]")        
    console.print("Research Question:", response.choices[0].message.content)
    research_question = response.choices[0].message.content
except Exception as e:
    print(f"An error occurred generating the research question: {e}")

# Make an API call for literature review/introduction with streaming and spinner
if research_question:  # Only proceed if we got a research question
    intro_prompt = (
        f"You are an expert academic writer specializing in the writing of systematic reviews and original research articles for peer-reviewed medical journals.\n\n"
        f"Your task is to write an *Introduction* section for a paper that addresses the following research question:\n"
        f"{research_question}\n\n"
        "The Introduction should:\n"
        "1. Be roughly **500–800 words** in length.\n"
        "2. Include approximately **15–20 citations** from **recent (last 10 years if possible), peer-reviewed journal articles**.\n"
        "   - Format citations as simple (Author, Year) inline, so that they can be manually inserted into a reference manager later.\n"
        "3. Clearly lay out:\n"
        "   - **Background** of the topic — the existing state of knowledge.\n"
        "   - **Context** — why this is an important area of study.\n"
        "   - **Rationale** — what gap in the literature or clinical practice this study seeks to address.\n"
        "   - **Primary objective(s)** of the paper.\n"
        "   - **Secondary objective(s)** if applicable.\n\n"
        "Maintain a formal academic tone appropriate for submission to a leading medical journal (such as NEJM, The Lancet, JAMA, BMJ, or Nature Medicine).\n\n"
        "Do not fabricate references — only use plausible, realistic references that exist in the literature (you may provide a placeholder author and year if needed)."
    )
    
    try:
        console.print("\n[bold cyan]INTRODUCTION SECTION:[/bold cyan]")        
        # Create streaming response using the OpenAI Responses API
        stream = client.responses.create(
            model="o3",
            background=True,
            input=intro_prompt,
            stream=True
        )
        
        # Variables to track streaming content
        accumulated_text = ""
        
        # Create a live display
        with Live(console=console, refresh_per_second=10) as live:
            for event in stream:
                # Handle different event types from the Responses API
                if event.type == "response.created":
                    # Initial response created
                    display_text = Text()
                    display_text.append("🔄 ", style="blue")
                    display_text.append("Starting generation... ", style="cyan")
                    live.update(Panel(display_text, title="[bold green]AI Response[/bold green]", border_style="green"))
                    
                elif event.type == "response.queued":
                    # Response queued for processing
                    display_text = Text()
                    display_text.append("⏳ ", style="yellow")
                    display_text.append("Response queued... ", style="cyan")
                    live.update(Panel(display_text, title="[bold green]AI Response[/bold green]", border_style="green"))
                    
                elif event.type == "response.in_progress":
                    # Response is being generated
                    display_text = Text()
                    display_text.append("🔄 ", style="blue")
                    display_text.append("Generating... ", style="cyan")
                    if accumulated_text:
                        display_text.append("\n\n")
                        display_text.append(accumulated_text, style="white")
                    live.update(Panel(display_text, title="[bold green]AI Response[/bold green]", border_style="green"))
                    
                elif event.type == "response.output_text.delta":
                    # New text content available
                    if hasattr(event, 'delta') and event.delta:
                        accumulated_text += event.delta
                        
                        # Create the display with spinner and content
                        display_text = Text()
                        display_text.append("🔄 ", style="blue")
                        display_text.append("Generating... ", style="cyan")
                        display_text.append("\n\n")
                        display_text.append(accumulated_text, style="white")
                        
                        # Update the live display
                        live.update(Panel(display_text, title="[bold green]AI Response[/bold green]", border_style="green"))
                
                elif event.type == "response.completed":
                    # Response generation completed
                    break
        
        # Final display without spinner
        console.print("\n[bold green]✅ Generation Complete![/bold green]")
        console.print(Panel(accumulated_text, title="[bold green]Final Introduction[/bold green]", border_style="green"))
        
    except Exception as e:
        console.print(f"[bold red]An error occurred generating the introduction: {e}[/bold red]")
else:
    console.print("[bold yellow]Could not generate introduction due to missing research question.[/bold yellow]")   

