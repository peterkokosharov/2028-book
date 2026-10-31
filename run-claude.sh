#!/bin/bash
# run-claude.sh - Launch Claude Code with all required environment
# Usage: ./run-claude.sh
# Or add alias: alias claude='~/run-claude.sh'

# Load user bashrc (for aliases, PATH, etc.)
source ~/.bashrc

# LiteLLM / Anthropic proxy configuration
export LITELLM_DROP_PARAMS="True"
export ANTHROPIC_BASE_URL="http://127.0.0.1:4000"
export ANTHROPIC_AUTH_TOKEN="sk-dummy-key"

# Model routing - map Claude models to working alternatives
export ANTHROPIC_MODEL="nvidia/nemotron-ultra"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="nvidia/nemotron-super"
export ANTHROPIC_DEFAULT_OPUS_MODEL="gemini/gemini-flash-lite"
export ANTHROPIC_DEFAULT_SONNET_MODEL="nvidia/nemotron-ultra"
export ANTHROPIC_DEFAULT_FABLE_MODEL="gemini/gemini-flash"

# Protective flags
export CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1
export DISABLE_PROMPT_CACHING=1

# Optional: API keys (uncomment and fill in, or use ~/.config/litellm/env with systemd)
# export NVIDIA_API_KEY="your_nvidia_key_here"
# export GEMINI_API_KEY="your_google_key_here"
# export GROQ_API_KEY="your_groq_key_here"
# export OPENROUTER_API_KEY="your_openrouter_key_here"
# export ANTHROPIC_API_KEY="your_anthropic_key_here"
# export DEEPSEEK_API_KEY="your_deepseek_key_here"

# Launch Claude
exec claude "$@"