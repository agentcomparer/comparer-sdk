# Agent Comparer CLI

A command-line interface for interacting with the [Agent Comparer](https://agentcomparer.com) API to analyze and compare AI models and agents.

## Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- virtualenv (recommended for isolated environments)

### Installation

1. Clone this repository or download the `comparer-cli.py` script

2. Create and activate a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Make the script executable (Unix-like systems only):
```bash
chmod +x comparer-cli.py
```

### Configuration

Set your API key as an environment variable. You can find the API key in your [account profile](https://agentcomparer.com/profile)

```bash
# On Windows (Command Prompt):
set COMPARER_API_KEY=your_api_key_here

# On Windows (PowerShell):
$env:COMPARER_API_KEY="your_api_key_here"

# On macOS/Linux:
export COMPARER_API_KEY=your_api_key_here
```

## Usage

### List Available Models

View all available model combinations in a formatted table:

```bash
# List all models
python comparer-cli.py list-models

# Search for specific models
python comparer-cli.py list-models --search "gpt"
python comparer-cli.py list-models --search "claude"
```

### List Providers

View all available AI providers and their model counts:

```bash
python comparer-cli.py list-providers
```

### Get Provider Statistics

View statistics about AI providers and their models:

```bash
python comparer-cli.py stats
```

### Search Models

Search for models with specific criteria:

```bash
# Basic search by provider
python comparer-cli.py search --provider anthropic

# Search with context window constraints
python comparer-cli.py search --min-context 8000 --max-context 32000

# Search with token constraints
python comparer-cli.py search --min-output-tokens 1000 --max-output-tokens 4000

# Search with capability filters
python comparer-cli.py search --tools --multilingual --streaming
```

Available search options:
- `--provider`: Filter by provider name
- `--min-context`: Minimum context window size
- `--max-context`: Maximum context window size
- `--min-output-tokens`: Minimum output tokens
- `--max-output-tokens`: Maximum output tokens
- `--tools/--no-tools`: Filter by tool availability
- `--multilingual/--no-multilingual`: Filter by multilingual support
- `--audio/--no-audio`: Filter by audio support
- `--vision/--no-vision`: Filter by vision support
- `--reasoning/--no-reasoning`: Filter by reasoning capabilities
- `--fine-tuning/--no-fine-tuning`: Filter by fine-tuning support
- `--streaming/--no-streaming`: Filter by realtime streaming support

### Compare Models

Compare multiple models using a specification file:

1. Generate a sample specification:
```bash
python comparer-cli.py sample-spec compare > compare-spec.json
```

2. Edit the generated file as needed and run the comparison:
```bash
python comparer-cli.py compare compare-spec.json
```

### Calculate Prices

Calculate prices for multiple model/token combinations:

1. Generate a sample specification:
```bash
python comparer-cli.py sample-spec calculate > calculate-spec.json
```

2. Edit the generated file as needed and run the calculation:
```bash
python comparer-cli.py calculate calculate-spec.json
{
  "calculations": [
    {
      "provider": "aws",
      "model_family": "meta_llama",
      "model_name": "llama_3.2_instruct_3b",
      "input_tokens": 1000,
      "output_tokens": 500,
      "input_price": 0.15,
      "output_price": 0.15,
      "input_cost": 0.00015,
      "output_cost": 7.5e-05,
      "total_cost": 0.000225
    },
    {
      "provider": "mistral",
      "model_family": "fine_tuning",
      "model_name": "mistral-small",
      "input_tokens": 2000,
      "output_tokens": 1000,
      "input_price": 0.2,
      "output_price": 0.6,
      "input_cost": 0.0004,
      "output_cost": 0.0006,
      "total_cost": 0.001
    }
  ],
  "total_cost": 0.001225,
  "metadata": {
    "agent_id": "cli-sample",
    "task_id": "calculation-test",
    "message_id": "msg789",
    "thread_id": "thread012"
  },
  "transaction_id": "zRCAxefgeHiAoYhndFdyrA"
}
```


### Sample Specifications

Generate sample specification files for compare and calculate commands:

```bash
# Generate sample compare specification
python comparer-cli.py sample-spec compare > compare-spec.json

# Generate sample calculate specification
python comparer-cli.py sample-spec calculate > calculate-spec.json
{
  "comparisons": [
    {
      "provider": "mistral",
      "model_family": "premier_models",
      "model_name": "mistral-large-24.11",
      "input_tokens": 1000,
      "output_tokens": 500,
      "input_price": 2.0,
      "output_price": 6.0,
      "input_cost": 0.002,
      "output_cost": 0.003,
      "total_cost": 0.005
    },
    {
      "provider": "together",
      "model_family": "qwen",
      "model_name": "Qwen_2.5_7B",
      "input_tokens": 1000,
      "output_tokens": 500,
      "input_price": 0.3,
      "output_price": 0.3,
      "input_cost": 0.0003,
      "output_cost": 0.00015,
      "total_cost": 0.00045
    }
  ],
  "cheapest_option": {
    "provider": "together",
    "model_family": "qwen",
    "model_name": "Qwen_2.5_7B",
    "input_tokens": 1000,
    "output_tokens": 500,
    "input_price": 0.3,
    "output_price": 0.3,
    "input_cost": 0.0003,
    "output_cost": 0.00015,
    "total_cost": 0.00045
  },
  "token_counts": {
    "input_tokens": 1000,
    "output_tokens": 500
  },
  "metadata": {
    "agent_id": "cli-sample",
    "task_id": "comparison-test",
    "message_id": "msg123",
    "thread_id": "thread456"
  },
  "transaction_id": "GqFs3w3xN8eejU4r6EgX9Q"
}
```

The generated files will include the necessary metadata and randomly selected models for each command.

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   Error: COMPARER_API_KEY environment variable not set
   ```
   Solution: Make sure you've set the COMPARER_API_KEY environment variable.

2. **Permission Denied**
   ```
   Permission denied: './comparer-cli.py'
   ```
   Solution: Make sure the script is executable:
   ```bash
   chmod +x comparer-cli.py
   ```

3. **Module Not Found**
   ```
   ModuleNotFoundError: No module named 'tabulate'
   ```
   Solution: Make sure you've activated the virtual environment and installed the requirements:
   ```bash
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

### Getting Help

For any command, you can add `--help` to see available options:

```bash
python comparer-cli.py --help
python comparer-cli.py search --help
python comparer-cli.py sample-spec --help
```

