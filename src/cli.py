# CLI interface for the pipeline generator
# Added more commands and better error handling

import click
import sys
from pathlib import Path

@click.group()
def cli():
    """CI/CD Pipeline Generator - Automatically creates p    """CI/CD Pipeline Generator - Automatically creates p    """CI/CD Pipeline Generator - Automatically creates p    """CI/CD Pipeline Generator - Automatically creates p    """CI/CD Pipeline Generator - Automatically creates p    """CI/CD Pipeline Generator - Automati.e    """CI/CD Pipeline Generator - Automatically creates p    """CI/ja    """CI/CD Pipeline Generator - Autrk    """CI/CD Pipeline Generator - Automatically creates p    """CI/CD Pipeline Generator - Automatically creates p    """CI/CD Pipeline Generator - Automatically creates p    """CI/CD Pipeline Generator - Automatically creates p    """CI/CD Pipeline Generator - Automatically creates p    """CI/CD Pipelinerat    """CI/CD Pipeline Generator - li    """CI/CD Pipeline Generator - Automati: implement actual generation
    click.echo("✅ Pipeline generated")

@cli.command()
def version():
    """Show version information"""
    click.echo("CI/CD Pipeline Generator v0.1.0")
    click.echo("Author: Mario Perez")

if __name__ == '__main__':
    cli()
