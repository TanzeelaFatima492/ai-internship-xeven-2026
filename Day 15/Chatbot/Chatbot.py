import os
import sys
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Rich Library modules for luxury UI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.markdown import Markdown

load_dotenv()
console = Console()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    console.print("[bold red]❌ Error:[/bold red] GEMINI_API_KEY `.env` file mein nahi mili!")
    sys.exit(1)

# Google Client Setup
client = genai.Client(api_key=API_KEY)

# Elite Mentor Personality
system_instruction = (
    "You are an elite, highly sophisticated AI Engineering Mentor. "
    "Your tone is deeply encouraging, premium, polished, and articulate. "
    "Structure your answers beautifully using bullet points or clean spacing where necessary."
)

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.6,
        max_output_tokens=700
    )
)

#Welcome Screen
console.clear()
welcome_text = Text()
welcome_text.append("M E N T O R  A I ✦\n", style="bold gold3")
welcome_text.append("Type 'exit' to conclude.", style="dim white")

console.print(
    Panel(
        welcome_text,
        border_style="gold3",
        expand=False,
        padding=(1, 5),
        subtitle="Developed by Tanzeela"
    )
)
console.print("\n")

# Loop
while True:
    try:
        # Luxury Input Prompt
        user_input = console.input("[bold color(214)]➔ You:[/bold color(214)] ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            console.print("\n[bold gold3]✦[/bold gold3] [italic white]May your code be elegant and your architecture flawless. Farewell.[/italic white] [bold gold3]✦[/bold gold3]\n")
            break
            
        if not user_input:
            continue
            
        # Sophisticated Loading State
        with console.status("[italic color(244)]Communing with the model...[/italic color(244)]", spinner="aesthetic"):
            response = chat.send_message(user_input)
            response_text = response.text

        # Premium Streaming/Typing Effect 
        console.print("[bold color(117)]🤖 Mentor AI:[/bold color(117)]")
        
        # Markdown parsing formatting for elite response view
        formatted_md = Markdown(response_text)
        
        # Is block se text achanak screen par nahi aayega, balkay smoothly render hoga
        with Live(vertical_overflow="visible") as live:
            # Render Markdown beautifully
            live.update(Panel(formatted_md, border_style="color(239)", padding=(1, 2)))
            
        # Optional Minimalist Token Counter
        if response.usage_metadata:
            t_in = response.usage_metadata.prompt_token_count
            t_out = response.usage_metadata.candidates_token_count
            console.print(f"[dim color(240)]  Metrics ✦ In: {t_in}т | Out: {t_out}т[/dim color(240)]")
            
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            console.print("\n[bold red]⏳ Rate Limit reached.[/bold red] [italic]Taking a premium pause. Try again in a minute.[/italic]")
        else:
            console.print(f"\n[bold red]❌ System Interruption:[/bold red] {error_msg}")