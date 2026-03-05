#!/usr/bin/env bash
# uxe-team install script
# Installs skills and agents to ~/.claude/ or a target project

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET=""
INSTALL_SKILLS=true
INSTALL_AGENTS=true

usage() {
  echo "Usage: ./scripts/install.sh [options]"
  echo ""
  echo "Options:"
  echo "  --project <path>   Install to a specific project instead of globally"
  echo "  --skills           Install skills only"
  echo "  --agents           Install agents only"
  echo "  --help             Show this message"
  echo ""
  echo "Examples:"
  echo "  ./scripts/install.sh                              # Install globally"
  echo "  ./scripts/install.sh --project ~/my-ds           # Install to a project"
  echo "  ./scripts/install.sh --skills                    # Skills only"
  echo "  ./scripts/install.sh --agents                    # Agents only"
}

while [[ "$#" -gt 0 ]]; do
  case $1 in
    --project) TARGET="$2"; shift ;;
    --skills) INSTALL_AGENTS=false ;;
    --agents) INSTALL_SKILLS=false ;;
    --help) usage; exit 0 ;;
    *) echo "Unknown option: $1"; usage; exit 1 ;;
  esac
  shift
done

if [ -z "$TARGET" ]; then
  SKILLS_DIR="$HOME/.claude/skills"
  AGENTS_DIR="$HOME/.claude/agents"
  SCOPE="globally (~/.claude/)"
else
  SKILLS_DIR="$TARGET/.claude/skills"
  AGENTS_DIR="$TARGET/.claude/agents"
  SCOPE="to $TARGET/.claude/"
fi

echo "Installing uxe-team $SCOPE"
echo ""

if [ "$INSTALL_SKILLS" = true ]; then
  mkdir -p "$SKILLS_DIR"
  for skill_dir in "$REPO_DIR"/skills/*/; do
    skill_name=$(basename "$skill_dir")
    echo "  Installing skill: $skill_name"
    cp -r "$skill_dir" "$SKILLS_DIR/$skill_name"
  done
  echo "  Skills installed: $(ls "$REPO_DIR/skills" | wc -l | tr -d ' ')"
fi

if [ "$INSTALL_AGENTS" = true ]; then
  mkdir -p "$AGENTS_DIR"
  for agent_file in "$REPO_DIR"/agents/*.md; do
    agent_name=$(basename "$agent_file")
    echo "  Installing agent: $agent_name"
    cp "$agent_file" "$AGENTS_DIR/$agent_name"
  done
  echo "  Agents installed: $(ls "$REPO_DIR/agents" | wc -l | tr -d ' ')"
fi

echo ""
echo "Done. Restart Claude Code to load the new skills and agents."
