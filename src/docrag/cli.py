"""Command-line interface for DocRAG Kit."""

import click
from docrag import __version__


@click.group()
@click.version_option(version=__version__, prog_name="docrag")
def cli():
    """DocRAG Kit - Universal RAG system for project documentation.
    
    Quick start:
    1. Run 'docrag init' to initialize RAG system in your project
    2. Run 'docrag index' to index your documentation
    3. Run 'docrag mcp-config' to get MCP server configuration
    """
    pass


@cli.command()
def init():
    """Initialize DocRAG in current project."""
    click.echo("🚀 Initializing DocRAG Kit...")
    click.echo("This command will be implemented in task 6.2")


@cli.command()
def index():
    """Index project documents."""
    click.echo("📚 Indexing documents...")
    click.echo("This command will be implemented in task 6.3")


@cli.command()
def reindex():
    """Rebuild vector database from scratch."""
    click.echo("🔄 Reindexing documents...")
    click.echo("This command will be implemented in task 6.4")


@cli.command()
@click.option("--edit", is_flag=True, help="Open configuration in editor")
def config(edit):
    """Display or edit current configuration."""
    if edit:
        click.echo("✏️  Opening configuration in editor...")
    else:
        click.echo("⚙️  Current configuration:")
    click.echo("This command will be implemented in task 6.5")


@cli.command("mcp-config")
def mcp_config():
    """Display MCP server configuration for Kiro."""
    click.echo("🔌 MCP Server Configuration:")
    click.echo("This command will be implemented in task 6.6")


if __name__ == "__main__":
    cli()
