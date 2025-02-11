#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib.resources
from dotenv import load_dotenv
import os

config = {
    "ready": False,
    "openai": {
        "api_key": "",
        "endpoint": "",
        "api_version": "2024-08-01-preview",
        "model_name": ""
    },
    "llama": {
        "api_key": "",
        "endpoint": "",
        "api_version": "2024-08-01-preview",
        "model_name": ""
    }
}

def initConfig(openai_api_key = "", openai_endpoint = "", openai_model_name = "", llama_api_key = "", llama_endpoint = "", llama_model_name = ""):
    config["openai"]["api_key"] = openai_api_key
    config["openai"]["endpoint"] = openai_endpoint
    config["openai"]["model_name"] = openai_model_name
    config["llama"]["api_key"] = llama_api_key
    config["llama"]["endpoint"] = llama_endpoint
    config["llama"]["model_name"] = llama_model_name
    config["ready"] = True

def initConfigFromEnv():
    load_dotenv()
    
    use_azure = os.getenv("USE_AZURE") == "1"
    
    if use_azure:
        # Configure OpenAI section with Azure credentials
        config["openai"]["api_key"] = os.getenv("AZURE_OPENAI_API_KEY")
        config["openai"]["endpoint"] = os.getenv("AZURE_OPENAI_ENDPOINT")
        config["openai"]["api_version"] = os.getenv("OPENAI_API_VERSION")
        config["openai"]["model_name"] = os.getenv("AZURE_DEPLOYMENT_NAME")
        
        # Configure Llama section to be empty when using Azure
        config["llama"]["api_key"] = ""
        config["llama"]["endpoint"] = ""
        config["llama"]["model_name"] = ""
    else:
        # Configure Llama section with Llama credentials
        config["llama"]["api_key"] = os.getenv("OPENAI_API_KEY")
        config["llama"]["endpoint"] = os.getenv("OPENAI_BASE_URL")
        config["llama"]["model_name"] = os.getenv("OPENAI_MODEL_NAME")
        
        # Configure OpenAI section to be empty when using Llama
        config["openai"]["api_key"] = ""
        config["openai"]["endpoint"] = ""
        config["openai"]["model_name"] = ""
    
    # Set config as ready
    config["ready"] = True
