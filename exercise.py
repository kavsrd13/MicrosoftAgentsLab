"""
Exercise: Memory Usage in Azure AI Foundry Agents
Complete the code below by filling in the TODO sections
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    MemoryStoreDefaultDefinition,
    MemoryStoreDefaultOptions,
    ResponsesUserMessageItemParam,
    MemorySearchOptions
)
from azure.identity import DefaultAzureCredential


# TODO: Step 1 - Initialize the AIProjectClient
# Get endpoint from environment variable or set directly
endpoint = "PASTE ENDPOINT"
# Create the client with endpoint and DefaultAzureCredential()



# TODO: Step 2 - Create Memory Store Options
# Set chat_summary_enabled=True
# Set user_profile_enabled=True
# Set user_profile_details to avoid sensitive data



# TODO: Define the memory store definition
# Set chat_model to your deployment name (e.g., "gpt-4.1")
# Set embedding_model to your deployment name (e.g., "text-embedding-3-small")
# Pass the options



# TODO: Create the memory store
# Name: "student_memory_store"
# Use try/except to handle if it already exists



# TODO: Step 3 - Add Memories
# Set a scope (e.g., "student_user_123")


# Create a user message with: "My name is John and I love cappuccino"


# Call begin_update_memories to store the memory
# Set update_delay=0 for immediate processing


# Get the result



# TODO: Step 4 - Search for Memories
# Create a query: "What is my coffee preference?"


# Search memories using the query


# Print the found memories



# TODO: Step 5 - Retrieve User Profile Memories
# Call search_memories WITHOUT items parameter to get all user profile memories


# Print the static memories



# TODO: Step 6 - Clean Up (Optional)
# Delete memories for the scope
# client.memory_stores.delete_scope(name="student_memory_store", scope=scope)
