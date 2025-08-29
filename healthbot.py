#!/usr/bin/env python3
"""
HealthBot: AI-Powered Patient Education System
A modular LangGraph-style workflow for patient education
"""

from healthbot_modules.workflow import HealthBotWorkflow

def main():
    """Main entry point for HealthBot application"""
    try:
        workflow = HealthBotWorkflow()
        workflow.execute_workflow()
    except Exception as e:
        print(f"Failed to initialize HealthBot: {str(e)}")
        print("Please check your config.env file and API keys.")

if __name__ == "__main__":
    main()