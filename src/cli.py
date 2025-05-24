"""
CLI interface for Mynd
"""
import click
import asyncio
import os
from pathlib import Path

from .main import Mynd

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    🧠 Mynd - Universal AI Memory
    
    Give every AI a photographic memory of YOUR life - securely, locally, forever.
    """
    pass

@cli.command()
@click.option('--port', default=8080, help='Port for MCP server')
def start(port: int):
    """Start Mynd with MCP server"""
    click.echo("🧠 Starting Mynd...")
    
    # Initialize Mynd
    data_dir = str(Path.home() / ".mynd")
    click.echo(f"📁 Data directory: {data_dir}")
    click.echo(f"🌐 MCP server will start on port {port}")
    
    vault = Mynd(data_dir=data_dir)
    vault.port = port
    
    try:
        asyncio.run(vault.run())
    except KeyboardInterrupt:
        click.echo("\n👋 Mynd stopped")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        raise click.Abort()

@cli.command()
def status():
    """Show Mynd status and statistics"""
    try:
        mynd = Mynd(data_dir=str(Path.home() / ".mynd"))
        stats = mynd.db.get_stats()
        
        click.echo("📊 Mynd Status:")
        click.echo("="*50)
        click.echo(f"📁 Data directory: {stats['db_path']}")
        click.echo(f"📈 Total events captured: {stats['total_events']:,}")
        click.echo(f"🔥 Recent activity (7 days): {stats['recent_activity']:,}")
        
        if stats['event_counts']:
            click.echo("\n📋 Events by type:")
            for source_type, count in stats['event_counts'].items():
                click.echo(f"   {source_type}: {count:,}")
        
        # Check if MCP server is running
        import requests
        try:
            response = requests.get("http://localhost:8080/api/status", timeout=2)
            if response.status_code == 200:
                click.echo("\n🟢 MCP server: Running")
            else:
                click.echo("\n🔴 MCP server: Not responding")
        except requests.RequestException:
            click.echo("\n🔴 MCP server: Not running")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        raise click.Abort()

@cli.command()
@click.argument('query')
@click.option('--max-tokens', default=4000, help='Maximum tokens to return')
def query(query: str, max_tokens: int):
    """Query Mynd for relevant context"""
    try:
        mynd = Mynd(data_dir=str(Path.home() / ".mynd"))
        
        # Get context
        context = mynd.get_context_for_query(query, max_tokens=max_tokens)
        
        click.echo(f"🔍 Context for: {query}")
        click.echo("="*50)
        
        if context:
            click.echo(context)
        else:
            click.echo("No relevant context found.")
            
    except Exception as e:
        click.echo(f"❌ Query error: {e}")
        raise click.Abort()

@cli.command()
@click.argument('source_file', type=click.Path(exists=True))
@click.option('--type', 'source_type', default='document', 
              type=click.Choice(['document', 'code', 'browser']),
              help='Type of content')
def capture(source_file: str, source_type: str):
    """Capture content from a file"""
    try:
        mynd = Mynd(data_dir=str(Path.home() / ".mynd"))
        
        click.echo("🔍 Starting manual capture...")
        asyncio.run(mynd.initial_capture(source_file=source_file, source_type=source_type))
        click.echo("✅ Capture completed!")
        
        # Show updated stats
        stats = mynd.db.get_stats()
        click.echo(f"📈 Total events: {stats['total_events']:,}")
        
    except Exception as e:
        click.echo(f"❌ Capture error: {e}")
        raise click.Abort()

@cli.command()
def init():
    """Initialize Mynd data directory and database"""
    click.echo("🎯 Initializing Mynd...")
    
    # Create data directory
    data_dir = str(Path.home() / ".mynd")
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    # Initialize database
    vault = Mynd(data_dir=data_dir)
    
    click.echo("✅ Database initialized")
    click.echo("✅ Directory structure created")
    
    # Check for Ollama
    try:
        import ollama
        client = ollama.Client()
        models = client.list()
        click.echo("✅ Ollama detected")
        
        # Check for required model
        model_names = [model['name'] for model in models['models']]
        if 'llama3.1:8b-instruct-q4_0' in model_names:
            click.echo("✅ Required LLM model available")
        else:
            click.echo("⚠️  Required LLM model not found")
            click.echo("   Run: ollama pull llama3.1:8b-instruct-q4_0")
            
    except ImportError:
        click.echo("⚠️  Ollama not installed")
        click.echo("   Visit: https://ollama.ai for installation")
    except Exception:
        click.echo("⚠️  Ollama not running")
        click.echo("   Start Ollama service first")
    
    click.echo("\n🚀 Ready to start Mynd!")
    click.echo("   Run: mynd start")

@cli.command()
def demo():
    """Create demo semantic events for testing"""
    try:
        mynd = Mynd(data_dir=str(Path.home() / ".mynd"))
        
        click.echo("🎬 Setting up demo data...")
        
        # Create some example semantic events
        demo_events = [
            {
                "source_type": "browser",
                "source_path": "https://docs.python.org/authentication",
                "content": "Researched JWT vs session authentication. Decided on JWT because mobile app needs stateless auth. Considered security implications of client-side token storage but chose it over Redis complexity.",
                "metadata": {"domain": "docs.python.org", "timestamp": "2024-03-15"}
            },
            {
                "source_type": "document", 
                "source_path": "/Users/dev/projects/auth-decisions.md",
                "content": "Architecture Decision: JWT Authentication. Problem: Need authentication for web and mobile. Solution: JWT with refresh tokens. Reasoning: Stateless, mobile-friendly, scalable. Trade-offs: XSS risk vs infrastructure simplicity.",
                "metadata": {"file_type": "markdown", "last_modified": "2024-03-15"}
            },
            {
                "source_type": "code",
                "source_path": "/Users/dev/projects/user-service/auth.py", 
                "content": "# Implemented JWT authentication with refresh tokens\n# Choice: Used PyJWT library for token handling\n# Security: Added token expiration and refresh mechanism\n# Performance: Tokens cached in memory for validation speed",
                "metadata": {"language": "python", "lines": 150}
            }
        ]
        
        for demo_event in demo_events:
            event = mynd.extractor.create_semantic_event(
                source_type=demo_event["source_type"],
                source_path=demo_event["source_path"],
                content=demo_event["content"],
                metadata=demo_event["metadata"]
            )
            mynd.db.store_event(event)
            mynd.vector_store.store_event(event)
        
        click.echo("✅ Demo data created!")
        click.echo("\n🎯 Try these demo queries:")
        click.echo("   mynd query 'authentication architecture decision'")
        click.echo("   mynd query 'JWT vs sessions'")
        click.echo("   mynd query 'mobile app authentication'")
    except Exception as e:
        click.echo(f"❌ Demo error: {e}")
        raise click.Abort()

if __name__ == "__main__":
    cli() 