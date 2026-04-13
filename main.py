import sys

# Force UTF-8 encoding on Windows to prevent UnicodeEncodeError in terminal 
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from rich.console import Console
from rich.markdown import Markdown
from core.chat import ReasoningChatSession

console = Console()

def main():
    console.rule("[bold blue]OpenRouter Reasoning CLI[/bold blue]")
    console.print("Type your message to start chatting. Type 'quit' or 'exit' to stop.\n")
    
    try:
        chat = ReasoningChatSession()
    except Exception as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        return

    while True:
        try:
            user_input = console.input("[bold green]You:[/bold green] ")
            if user_input.strip().lower() in ['quit', 'exit']:
                console.print("[dim]Goodbye![/dim]")
                break
                
            if not user_input.strip():
                continue
                
            console.print("[dim]Thinking...[/dim]")
            
            message = chat.send_message(user_input)
            
            # Extract reasoning details for display
            # Some models might use `reasoning` directly instead of `reasoning_details` in the SDK depending on mapping
            reasoning = getattr(message, "reasoning_details", None)
            
            # Print reasoning if available
            if reasoning:
                console.print("\n[bold yellow]Reasoning:[/bold yellow]")
                # Convert to string in case it's a dict (e.g. {"reasoning": "..."})
                console.print(f"[yellow]{reasoning}[/yellow]")
            
            # Print the final response
            console.print("\n[bold blue]Assistant:[/bold blue]")
            if message.content:
                console.print(Markdown(message.content))
            else:
                console.print("[italic dim]No completion content returned.[/italic dim]")
                
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye![/dim]")
            break
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
