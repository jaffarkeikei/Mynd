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
@click.option('--data-dir', default=None, help='Directory to store Mynd data')
@click.option('--port', default=8080, help='Port for MCP server')
def start(data_dir, port):
    """Start Mynd with MCP server"""
    click.echo("🧠 Starting Mynd...")
    
    if data_dir is None:
        data_dir = str(Path.home() / ".myndai")
    
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
@click.option('--data-dir', default=None, help='Directory where Mynd data is stored')
def status(data_dir):
    """Show Mynd status and statistics"""
    if data_dir is None:
        data_dir = str(Path.home() / ".myndai")
    
    vault = Mynd(data_dir=data_dir)
    stats = vault.db.get_stats()
    
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

@cli.command()
@click.argument('query_text')
@click.option('--max-tokens', default=4000, help='Maximum tokens in response')
@click.option('--data-dir', default=None, help='Directory where Mynd data is stored')
def query(query_text, max_tokens, data_dir):
    """Query your context memory"""
    if data_dir is None:
        data_dir = str(Path.home() / ".myndai")
    
    vault = Mynd(data_dir=data_dir)
    
    try:
        context = vault.get_context_for_query(query_text, max_tokens=max_tokens)
        
        click.echo(f"🔍 Context for: {query_text}")
        click.echo("="*50)
        
        if context:
            click.echo(context)
        else:
            click.echo("No relevant context found.")
            
    except Exception as e:
        click.echo(f"❌ Query error: {e}")
        raise click.Abort()

@cli.command()
@click.option('--data-dir', default=None, help='Directory where Mynd data is stored')
@click.option('--days', default=30, help='Number of days of history to capture')
def capture(data_dir, days):
    """Manually trigger context capture from browser history and documents"""
    if data_dir is None:
        data_dir = str(Path.home() / ".myndai")
    
    vault = Mynd(data_dir=data_dir)
    
    try:
        click.echo("🔍 Starting manual capture...")
        asyncio.run(vault.initial_capture(days=days))
        click.echo("✅ Capture completed!")
        
        # Show updated stats
        stats = vault.db.get_stats()
        click.echo(f"📈 Total events: {stats['total_events']:,}")
        
    except Exception as e:
        click.echo(f"❌ Capture error: {e}")
        raise click.Abort()

@cli.command()
@click.option('--data-dir', default=None, help='Directory where Mynd data is stored')
def init(data_dir):
    """Initialize Mynd data directory and configuration"""
    if data_dir is None:
        data_dir = str(Path.home() / ".myndai")
    
    click.echo(f"🎯 Initializing Mynd in {data_dir}")
    
    # Create data directory
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
@click.option('--data-dir', default=None, help='Directory where Mynd data is stored')
def demo(data_dir):
    """Set up demo data for showcasing Mynd"""
    if data_dir is None:
        data_dir = str(Path.home() / ".myndai")
    
    vault = Mynd(data_dir=data_dir)
    
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
        event = vault.extractor.create_semantic_event(
            source_type=demo_event["source_type"],
            source_path=demo_event["source_path"],
            content=demo_event["content"],
            metadata=demo_event["metadata"]
        )
        vault.db.store_event(event)
        vault.vector_store.store_event(event)
    
    click.echo("✅ Demo data created!")
    click.echo("\n🎯 Try these demo queries:")
    click.echo("   mynd query 'authentication architecture decision'")
    click.echo("   mynd query 'JWT vs sessions'")
    click.echo("   mynd query 'mobile app authentication'")

if __name__ == "__main__":
    cli() 