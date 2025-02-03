#!/usr/bin/env python3

import os
import sys
import json
import random

from pathlib import Path
from typing import Optional, List, Dict
from collections import defaultdict

import click
import requests
from tabulate import tabulate

API_KEY = os.getenv('COMPARER_API_KEY')
BASE_URL = 'https://agentcomparer.com'

class ApiClient:
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({'X-API-Key': api_key})
    
    def get_models(self) -> List[Dict]:
        response = self.session.get(f"{BASE_URL}/api/models/list")
        response.raise_for_status()
        return response.json()
    
    def get_stats(self) -> Dict:
        response = self.session.get(f"{BASE_URL}/api/models/stats")
        response.raise_for_status()
        return response.json()
    
    def get_providers(self) -> List[str]:
        models = self.get_models()

        counts = defaultdict(int)
        for m in models:
            provider = m['provider']
            counts[provider] += 1
        return counts
    
    def search_models(self,
                     provider: Optional[str] = None,
                     min_context: Optional[int] = None,
                     max_context: Optional[int] = None,
                     min_output_tokens: Optional[int] = None,
                     max_output_tokens: Optional[int] = None,
                     tools: Optional[bool] = None,
                     multilingual: Optional[bool] = None,
                     audio: Optional[bool] = None,
                     vision: Optional[bool] = None,
                     reasoning: Optional[bool] = None,
                     fine_tuning: Optional[bool] = None,
                     streaming: Optional[bool] = None):
        
        payload = {
            "metadata": {
                "agent_id": "cli",
                "task_id": "search"
            },
            "provider": provider,
            "min_context": min_context,
            "max_context": max_context,
            "min_output_tokens": min_output_tokens,
            "max_output_tokens": max_output_tokens,
            "tools": tools,
            "multilingual": multilingual,
            "audio": audio,
            "vision": vision,
            "reasoning": reasoning,
            "fine_tuning": fine_tuning,
            "realtime_streaming": streaming
        }

        response = self.session.post(f"{BASE_URL}/api/agents/search", json=payload)
        response.raise_for_status()
        return response.json()

    def compare_models(self, data: Dict):
        response = self.session.post(f"{BASE_URL}/api/agents/compare", json=data)
        response.raise_for_status()
        return response.json()

    def calculate_price(self, data: Dict):
        response = self.session.post(f"{BASE_URL}/api/agents/calculate", json=data)
        response.raise_for_status()
        return response.json()

@click.group()
@click.option("--server", default=None, help="Run against a particular server")
def cli(server):
    """CLI tool for interacting with the Agent Comparer API"""
    if not API_KEY:
        raise click.ClickException("COMPARER_API_KEY environment variable not set")

    global BASE_URL
    if server:
        BASE_URL = server

@cli.command()
@click.option('--search', help='Search string to filter models', default='')
def list_models(search):
    """List all available model combinations"""
    client = ApiClient(API_KEY)
    try:
        models = client.get_models()
        
        # Filter models if search string is provided
        if search:
            search = search.lower()
            models = [
                model for model in models
                if search in model.get('provider', '').lower() or
                   search in model.get('model_family', '').lower() or
                   search in model.get('model_name', '').lower()
            ]
        
        if not models:
            if search:
                click.echo(f"No models found matching search: {search}")
            else:
                click.echo("No models available")
            return

        headers = ["Provider", "Model Family", "Model Name"]
        table_data = [[
            model.get('provider', 'N/A'),
            model.get('model_family', 'N/A'),
            model.get('model_name', 'N/A')
        ] for model in models]
        
        click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
        click.echo(f"\nTotal models: {len(models)}")
    except requests.RequestException as e:
        raise click.ClickException(f"API request failed: {str(e)}")

@cli.command()
def list_providers():
    """List all available providers"""
    client = ApiClient(API_KEY)
    try:
        providers = client.get_providers()
        if not providers:
            click.echo("No providers available")
            return

        headers = ["Provider", "Models"]
        table_data = [[provider, count] for provider,count in providers.items()]
        click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
        click.echo(f"\nTotal providers: {len(providers)}")
    except requests.RequestException as e:
        raise click.ClickException(f"API request failed: {str(e)}")

@cli.command()
def stats():
    """Get provider statistics"""
    client = ApiClient(API_KEY)
    try:
        stats = client.get_stats()
        headers = ["Provider", "Model Count"]
        table_data = [[provider, count] for provider, count in stats.items()]
        click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
    except requests.RequestException as e:
        raise click.ClickException(f"API request failed: {str(e)}")

@cli.command()
@click.option('--provider', help='Filter by provider name')
@click.option('--min-context', type=int, help='Minimum context window size')
@click.option('--max-context', type=int, help='Maximum context window size')
@click.option('--min-output-tokens', type=int, help='Minimum output tokens')
@click.option('--max-output-tokens', type=int, help='Maximum output tokens')
@click.option('--tools/--no-tools', default=None, help='Filter by tool availability')
@click.option('--multilingual/--no-multilingual', default=None, help='Filter by multilingual support')
@click.option('--audio/--no-audio', default=None, help='Filter by audio support')
@click.option('--vision/--no-vision', default=None, help='Filter by vision support')
@click.option('--reasoning/--no-reasoning', default=None, help='Filter by reasoning capabilities')
@click.option('--fine-tuning/--no-fine-tuning', default=None, help='Filter by fine-tuning support')
@click.option('--streaming/--no-streaming', default=None, help='Filter by realtime streaming support')
def search(provider, min_context, max_context, min_output_tokens, max_output_tokens,
          tools, multilingual, audio, vision, reasoning, fine_tuning, streaming):
    """Search for models with specific criteria"""
    client = ApiClient(API_KEY)
    try:
        results = client.search_models(
            provider=provider,
            min_context=min_context,
            max_context=max_context,
            min_output_tokens=min_output_tokens,
            max_output_tokens=max_output_tokens,
            tools=tools,
            multilingual=multilingual,
            audio=audio,
            vision=vision,
            reasoning=reasoning,
            fine_tuning=fine_tuning,
            streaming=streaming
        )
        click.echo("Search Results:")
        click.echo(json.dumps(results, indent=2))
    except requests.RequestException as e:
        raise click.ClickException(f"API request failed: {str(e)}")

@cli.command()
@click.argument('spec', type=click.Path(exists=True))
def compare(spec):
    """Compare models using spec from JSON file"""
    client = ApiClient(API_KEY)
    try:
        with open(spec) as f:
            data = json.load(f)
        results = client.compare_models(data)
        click.echo(json.dumps(results, indent=2))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise click.ClickException(f"Error reading input file: {str(e)}")
    except requests.RequestException as e:
        raise click.ClickException(f"API request failed: {str(e)}")

@cli.command()
@click.argument('spec', type=click.Path(exists=True))
def calculate(spec):
    """Calculate prices using input from JSON file"""
    client = ApiClient(API_KEY)
    try:
        with open(spec) as f:
            data = json.load(f)
        results = client.calculate_price(data)
        click.echo(json.dumps(results, indent=2))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise click.ClickException(f"Error reading input file: {str(e)}")
    except requests.RequestException as e:
        raise click.ClickException(f"API request failed: {str(e)}")

@cli.command()
@click.argument('command', type=click.Choice(['compare', 'calculate']))
def sample_spec(command):
    """Generate sample input JSON for compare or calculate commands"""

    client = ApiClient(API_KEY)
    models = client.get_models()    

    twomodels = random.sample(models, 2)

    if command == 'compare':
        print(json.dumps({
            "models": twomodels,
            "input_tokens": 1000,
            "output_tokens": 500,
            "metadata": {
                "agent_id": "cli-sample",
                "task_id": "comparison-test",
                "message_id": "msg123",
                "thread_id": "thread456"
            }
        }, indent=4))

    if command == 'calculate':
        twomodels[0].update({
            "input_tokens": 1000,
            "output_tokens": 500
        }) 
        twomodels[1].update({
            "input_tokens": 2000,
            "output_tokens": 1000
        })       
        print(json.dumps({        
            "calculations": twomodels,
            "metadata": {
                "agent_id": "cli-sample",
                "task_id": "calculation-test",
                "message_id": "msg789",
                "thread_id": "thread012"
            }
        }, indent=4))

if __name__ == '__main__':
    cli()
