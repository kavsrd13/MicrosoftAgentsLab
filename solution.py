"""
Exercise Solution: Memory Usage in Azure AI Foundry Agents
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


# Step 1 - Initialize the AIProjectClient
endpoint = "                "
client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential()
)
print(f"Client initialized")


# Step 2 - Create Memory Store Options
options = MemoryStoreDefaultOptions(
    chat_summary_enabled=True,
    user_profile_enabled=True,
    user_profile_details="Avoid irrelevant or sensitive data, such as age, financials, precise location, and credentials"
)

definition = MemoryStoreDefaultDefinition(
    chat_model="gpt-4.1",
    embedding_model="text-embedding-3-small",
    options=options
)

# Create the memory store
memory_store_name = "student_memory_store"
try:
    memory_store = client.memory_stores.create(
        name=memory_store_name,
        definition=definition,
        description="Student exercise memory store"
    )
    print(f"Created memory store: {memory_store.name}")
except Exception as e:
    if "already exists" in str(e):
        print(f"Using existing memory store: {memory_store_name}")
        memory_store = client.memory_stores.get(name=memory_store_name)
    else:
        raise e


# Step 3 - Add Memories
scope = "student_user_123"

user_message = ResponsesUserMessageItemParam(
    content="My name is John and I love cappuccino"
)

update_poller = client.memory_stores.begin_update_memories(
    name=memory_store_name,
    scope=scope,
    items=[user_message],
    update_delay=0
)

update_result = update_poller.result()
print(f"Memory updated: {len(update_result.memory_operations)} operation(s)")


# Step 4 - Search for Memories
query = ResponsesUserMessageItemParam(content="What is my coffee preference?")

search_response = client.memory_stores.search_memories(
    name=memory_store_name,
    scope=scope,
    items=[query],
    options=MemorySearchOptions(max_memories=5)
)

print(f"\nFound {len(search_response.memories)} memory/memories:")
for memory in search_response.memories:
    print(f"  - {memory.memory_item.content}")


# Step 5 - Retrieve User Profile Memories
static_response = client.memory_stores.search_memories(
    name=memory_store_name,
    scope=scope,
    options=MemorySearchOptions(max_memories=10)
)

print(f"\nStatic memories: {len(static_response.memories)}")
for memory in static_response.memories:
    print(f"  - {memory.memory_item.content}")


# Step 6 - Clean Up (Optional)
# Uncomment to delete memories for this scope
# client.memory_stores.delete_scope(name=memory_store_name, scope=scope)
# print(f"Deleted memories for scope: {scope}")
