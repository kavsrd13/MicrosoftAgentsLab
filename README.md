# Exercise: Memory Usage in Azure AI Foundry Agents

## Overview
Learn how to create and use memory in Foundry Agent Service to build agents that retain user preferences and conversation history across sessions. This exercise provides detailed step-by-step instructions from Azure resource creation to running your first memory-enabled agent.

## Learning Objectives
By completing this exercise, you will:
- Set up Azure AI Foundry Project
- Deploy GPT-4 chat model for memory processing
- Deploy text embedding model for semantic search
- Install and configure Python SDK
- Create a memory store with chat and embedding models
- Add user preferences to memory using the API
- Search and retrieve memories using semantic search
- Understand how memory is partitioned by scope

---

## PART 1: Azure AI Foundry Setup (Portal)

### Step 1: Create Azure AI Foundry Project

**What is a Project?** A project is a workspace in Azure AI Foundry where you deploy models and build AI applications.

1. **Navigate to Azure AI Foundry**
   - Open browser and go to: https://ai.azure.com
   - Sign in with your Azure account credentials

2. **Create New Project**
   - Click **"+ New project"** button
   - Fill in the form:
     - **Project name**: `memory-agent-project` (lowercase, no spaces)
     - **Subscription**: Select your Azure subscription
     - **Resource group**: 
       - Click **Create new** if you don't have one
       - Name: `rg-ai-foundry`
       - Click **OK**
     - **Location/Region**: Choose `East US` or `West Europe`
   - Click **Create**
   - Wait 2-3 minutes for deployment

3. **Get Project Endpoint**
   - Once created, click on your project
   - Go to **"Settings"** in the left menu or click **"Overview"**
   - Look for **"Project endpoint"** or **"Connection string"**
   - Example format: `https://your-hub-xxx.services.ai.azure.com/api/projects/memory-agent-project`
   - **IMPORTANT**: Copy this entire URL - save it in a notepad!

---

### Step 2: Deploy GPT-4 Chat Model

**Why?** Memory store needs a chat model to extract and process user preferences from conversations.

1. **Navigate to Deployments**
   - In your project, click **"Deployments"** from left menu
   - Click **"+ Create deployment"** or **"+ Deploy model"**

2. **Select Model**
   - Browse or search for **"gpt-4"** or **"gpt-4o"**
   - Click on the model card
   - Click **"Deploy"**

3. **Configure Deployment**
   - **Deployment name**: `gpt-4.1` (remember this exact name!)
   - **Model version**: Select the latest available
   - **Deployment type**: `Standard`
   - **Tokens per Minute Rate Limit (thousands)**: `10` (or higher if available)
   - Click **Deploy**

4. **Wait for Deployment**
   - Status will show "Creating..." then "Succeeded"
   - This takes 1-2 minutes
   - **Verify**: You should see `gpt-4.1` in your deployments list

---

### Step 3: Deploy Text Embedding Model

**Why?** Memory store uses embeddings to perform semantic search on stored memories.

1. **Create Another Deployment**
   - Stay in **"Deployments"** page
   - Click **"+ Create deployment"** again

2. **Select Embedding Model**
   - Search for **"text-embedding-3-small"**
   - Click on the model
   - Click **"Deploy"**

3. **Configure Deployment**
   - **Deployment name**: `text-embedding-3-small` (exact name!)
   - **Model version**: Latest
   - **Deployment type**: `Standard`
   - Click **Deploy**

4. **Verify Both Deployments**
   - Go to **"Deployments"** list
   - Confirm you have:
     - ✅ `gpt-4.1` (Status: Succeeded)
     - ✅ `text-embedding-3-small` (Status: Succeeded)

---

## PART 2: Local Development Setup

### Step 4: Install Python and Create Environment

1. **Verify Python Installation**
   ```powershell
   python --version
   ```
   - Should show Python 3.8 or higher
   - If not installed, download from: https://www.python.org/downloads/

2. **Navigate to Exercise Folder**
   ```powershell
   cd d:\work\AgentFramework\AgentLabs\Agents\Microsoft_Foundry\Exercise_Agents_Memory
   ```

3. **Create Virtual Environment** (Recommended)
   ```powershell
   # Create virtual environment
   python -m venv venv
   
   # Activate it (Windows PowerShell)
   .\venv\Scripts\activate
   
   # Your prompt should now show (venv)
   ```

4. **Upgrade pip**
   ```powershell
   python -m pip install --upgrade pip
   ```

---

### Step 5: Install Azure AI SDK

1. **Install Required Packages**
   ```powershell
   pip install azure-ai-projects
   pip install azure-identity
   ```

2. **Verify Installation**
   ```powershell
   pip list | findstr azure
   ```
   
   **Expected output:**
   ```
   azure-ai-projects       1.0.0 (or higher)
   azure-core             1.x.x
   azure-identity         1.x.x
   ```

3. **Troubleshooting**
   - If installation fails, try:
     ```powershell
     pip install --upgrade azure-ai-projects azure-identity
     ```

---

### Step 6: Configure Azure Authentication

1. **Install Azure CLI** (if not already installed)
   
   **Check if installed:**
   ```powershell
   az --version
   ```
   
   **If not installed:**
   - Download from: https://aka.ms/installazurecliwindows
   - Or use winget:
     ```powershell
     winget install Microsoft.AzureCLI
     ```
   - Restart PowerShell after installation

2. **Login to Azure**
   ```powershell
   az login
   ```
   - Browser will open automatically
   - Sign in with your Azure account
   - Look for "You have signed in" message
   - Close browser and return to terminal

3. **Verify Login**
   ```powershell
   az account show
   ```
   - Should display your subscription details

---

### Step 7: Set Environment Variable

**Why?** Your code needs to know which Azure project to connect to.

1. **Set Temporary Environment Variable** (current session only)
   ```powershell
   $env:AZURE_AI_PROJECT_ENDPOINT = "https://your-hub-xxx.services.ai.azure.com/api/projects/memory-agent-project"
   ```
   **Replace with YOUR actual endpoint!**

2. **Set Permanent Environment Variable** (recommended)
   ```powershell
   [System.Environment]::SetEnvironmentVariable('AZURE_AI_PROJECT_ENDPOINT', 'https://your-hub-xxx.services.ai.azure.com/api/projects/memory-agent-project', 'User')
   ```
   **Replace with YOUR actual endpoint!**

3. **Verify It's Set**
   ```powershell
   echo $env:AZURE_AI_PROJECT_ENDPOINT
   ```
   - Should display your full project endpoint URL

4. **Restart Terminal** (if you set permanent variable)
   - Close and reopen PowerShell to load the permanent variable

---

### Step 8: Initialize the AI Client

**What you're doing:** Connecting your Python code to your Azure AI project.

**Complete TODO 1:**
```python
# Get endpoint from environment variable
endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

# Create the AI client
client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential()
)
```

**Test it:**
```powershell
python exercise_memory.py
```

**Expected:** No errors, program starts successfully

**If error "endpoint must not be None":**
- Check Step 7 - environment variable not set correctly
- Run: `echo $env:AZURE_AI_PROJECT_ENDPOINT`

---

### Step 9: Create Memory Store Options

**What you're doing:** Configuring what types of information the memory system should store.

**Complete TODO 2:**
```python
options = MemoryStoreDefaultOptions(
    chat_summary_enabled=True,          # Store conversation summaries
    user_profile_enabled=True,          # Store user preferences
    user_profile_details="Avoid irrelevant or sensitive data, such as age, financials, precise location, and credentials"
)
```

**Key points:**
- `chat_summary_enabled=True` - Stores conversation context
- `user_profile_enabled=True` - Stores user preferences like name, likes/dislikes
- `user_profile_details` - Privacy control: tells AI what NOT to store

---

### Step 10: Define Memory Store

**What you're doing:** Specifying which models to use for memory processing.

**Complete TODO 3:**
```python
definition = MemoryStoreDefaultDefinition(
    chat_model="gpt-4.1",                    # YOUR chat model deployment name
    embedding_model="text-embedding-3-small", # YOUR embedding model deployment name
    options=options
)
```

**IMPORTANT:**
- Use the EXACT deployment names from Step 3 and Step 4
- These must match what's in your Azure portal
- Case-sensitive!

---

### Step 11: Create the Memory Store

**What you're doing:** Creating a persistent storage container for memories.

**Complete TODO 4:**
```python
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
```

**Run and test:**
```powershell
python exercise_memory.py
```

**Expected output:**
```
Created memory store: student_memory_store
```

Or if running again:
```
Using existing memory store: student_memory_store
```

---

### Step 12: Set Scope and Add User Preferences

**What you're doing:** Storing user information in memory with user isolation.

**Complete TODO 5:**
```python
# Scope = unique identifier for this user
scope = "student_user_123"

# User message containing preferences
user_message = ResponsesUserMessageItemParam(
    content="My name is John and I love cappuccino"
)
```

**What is Scope?**
- Think of it like a user ID
- Each user gets their own isolated memory space
- Prevents one user's memories from mixing with another's

---

### Step 13: Store the Memory

**What you're doing:** Sending the user's message to be processed and stored.

**Complete TODO 6:**
```python
update_poller = client.memory_stores.begin_update_memories(
    name=memory_store_name,
    scope=scope,
    items=[user_message],
    update_delay=0  # Process immediately
)

update_result = update_poller.result()
print(f"Memory updated: {len(update_result.memory_operations)} operation(s)")
```

**Run and test:**
```powershell
python exercise_memory.py
```

**Expected output:**
```
Memory updated: 0 operation(s)
```

**Note:** `0` operations is NORMAL! Memory processing happens asynchronously in the background. The AI is extracting "John" and "cappuccino" from your message.

---

### Step 14: Search for Specific Memories

**What you're doing:** Using semantic search to find relevant memories.

**Complete TODO 7:**
```python
# Create a search query
query = ResponsesUserMessageItemParam(
    content="What is my coffee preference?"
)

# Search memories
search_response = client.memory_stores.search_memories(
    name=memory_store_name,
    scope=scope,
    items=[query],
    options=MemorySearchOptions(max_memories=5)
)

# Print results
print(f"\nFound {len(search_response.memories)} memory/memories:")
for memory in search_response.memories:
    print(f"  - {memory.memory_item.content}")
```

**Run and test:**
```powershell
python exercise_memory.py
```

**Expected output:**
```
Found 1 memory/memories:
  - User prefers cappuccino
```

**What happened?**
- Your query "What is my coffee preference?" 
- Semantic search found the memory about "cappuccino"
- Even though exact words don't match, AI understands meaning!

---

### Step 15: Retrieve All User Profile Memories

**What you're doing:** Getting ALL stored memories for this user.

**Complete TODO 8:**
```python
# Search WITHOUT a query = get all memories
static_response = client.memory_stores.search_memories(
    name=memory_store_name,
    scope=scope,
    options=MemorySearchOptions(max_memories=10)
)

print(f"\nStatic memories: {len(static_response.memories)}")
for memory in static_response.memories:
    print(f"  - {memory.memory_item.content}")
```

**Run and test:**
```powershell
python exercise_memory.py
```

**Expected output:**
```
Static memories: 1
  - User prefers cappuccino
```

**Difference from Step 15:**
- Step 15: Search WITH query (semantic search)
- Step 16: Search WITHOUT query (get everything)

---

### Step 16: Clean Up (Optional)

**What you're doing:** Deleting stored memories.

**Complete TODO 9:**
```python
# Uncomment to delete
client.memory_stores.delete_scope(name=memory_store_name, scope=scope)
print(f"Deleted memories for scope: {scope}")
```

**When to use:**
- User requests data deletion
- Testing and need to reset
- Comply with privacy regulations (GDPR)

---

## PART 4: Run Complete Solution

### Step 17: Test the Complete Program

1. **Run your completed exercise:**
   ```powershell
   python exercise_memory.py
   ```

2. **OR run the provided solution:**
   ```powershell
   python solution_memory.py
   ```

**Complete expected output:**
```
Client initialized
Created memory store: student_memory_store
Memory updated: 0 operation(s)

Found 1 memory/memories:
  - User prefers cappuccino

Static memories: 1
  - User prefers cappuccino
```

---

## Key Concepts Explained

---

## Key Concepts Explained

### 🔑 Scope
**Purpose:** Isolates memory for different users

**Example:**
```python
scope = "user_john_123"  # John's memories
scope = "user_alice_456" # Alice's memories (separate)
```

**Best practices:**
- Use unique user IDs
- Format: `"user_{userid}"` or `"{{$userId}}"` for authenticated users
- Prevents data leakage between users

---

### 📦 Memory Types

**1. User Profile Memory**
- Stores: User preferences, name, likes/dislikes
- Persistence: Long-term, across all conversations
- Example: "User prefers cappuccino", "User name is John"

**2. Chat Summary Memory**
- Stores: Conversation context and summaries
- Persistence: Recent conversation history
- Example: "Discussed coffee preferences", "Talked about morning routine"

---

### 🔍 Search Methods

**Semantic Search (with query):**
```python
search_memories(scope=scope, items=[query])
```
- Finds relevant memories based on meaning
- Example: Query "coffee" finds "cappuccino preference"

**Retrieve All (without query):**
```python
search_memories(scope=scope)
```
- Gets all static user profile memories
- No filtering, returns everything for that scope

---

### 🤖 How Memory Works

1. **Input:** "My name is John and I love cappuccino"
2. **Processing:** GPT-4 extracts key information
3. **Storage:** Creates memory items:
   - "User name: John"
   - "User prefers cappuccino"
4. **Embedding:** Text-embedding model creates vectors
5. **Retrieval:** Semantic search finds relevant memories

---

## Troubleshooting Guide

### ❌ Error: "endpoint must not be None"
**Cause:** Environment variable not set

**Solution:**
```powershell
$env:AZURE_AI_PROJECT_ENDPOINT = "your-endpoint-here"
echo $env:AZURE_AI_PROJECT_ENDPOINT  # Verify
```

---

### ❌ Error: "Model deployment 'gpt-4.1' not found"
**Cause:** Deployment name mismatch

**Solution:**
1. Go to Azure portal → your project → Deployments
2. Check EXACT deployment name (case-sensitive)
3. Update code to match:
   ```python
   chat_model="gpt-4"  # Use your actual name
   ```

---

### ❌ Error: "Authentication failed"
**Cause:** Not logged into Azure

**Solution:**
```powershell
az login
az account show  # Verify login
```

---

### ⚠️ No memories returned / Empty results
**Cause:** Memory processing is asynchronous

**Solution:**
- Wait 5-10 seconds
- Run the search again
- Memories may still be processing in background

---

### ❌ Error: "Memory store already exists"
**Cause:** Store name already used

**Solution:**
- Change `memory_store_name` to something unique
- Or use the existing one (code handles this with try/except)

---

## Success Criteria Checklist

### Azure Setup
- ✅ Azure AI Foundry hub created
- ✅ Azure AI project created
- ✅ Project endpoint copied and saved
- ✅ GPT-4 model deployed (gpt-4.1)
- ✅ Embedding model deployed (text-embedding-3-small)

### Local Setup
- ✅ Python 3.8+ installed
- ✅ Virtual environment created and activated
- ✅ Azure SDK installed (`azure-ai-projects`)
- ✅ Azure CLI installed
- ✅ Logged in via `az login`
- ✅ Environment variable set (`AZURE_AI_PROJECT_ENDPOINT`)

### Code Execution
- ✅ Client initialized successfully
- ✅ Memory store created
- ✅ User message stored
- ✅ Semantic search returns results
- ✅ Static memories retrieved
- ✅ Understands scope isolation

---

## Experiment and Learn

### Try These Variations:

**1. Different User Preferences:**
```python
content="My name is Alice and I prefer green tea"
```

**2. Multiple Scopes:**
```python
scope = "user_alice"  # Alice's memories
scope = "user_bob"    # Bob's memories (isolated)
```

**3. Different Queries:**
```python
content="What is my name?"
content="What drinks do I like?"
content="Tell me about my preferences"
```

**4. Privacy Controls:**
```python
user_profile_details="Store only beverage preferences, avoid personal identifiers"
```

---

## Additional Resources

### Documentation
- [Memory Usage Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/memory-usage?view=foundry&tabs=python)
- [Azure AI Foundry Portal](https://ai.azure.com)
- [Python SDK Reference](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects-readme)

### Useful Commands
```powershell
# Check environment
echo $env:AZURE_AI_PROJECT_ENDPOINT

# List deployments
az ml deployment list --workspace-name your-project

# Check Azure login
az account show

# Reinstall packages
pip uninstall azure-ai-projects -y
pip install azure-ai-projects
```

---

## Next Steps

After completing this exercise, you can:

1. **Integrate with Agents:**
   - Attach memory to a conversational agent
   - Enable persistent context across chat sessions

2. **Add Memory Tool to Agents:**
   - Use `MemorySearchTool` in agent definitions
   - Auto-update memories during conversations

3. **Explore Advanced Features:**
   - Custom memory extraction rules
   - Multiple memory stores for different purposes
   - Memory consolidation strategies

4. **Build Real Applications:**
   - Customer support bot with user history
   - Personal assistant with preferences
   - Multi-tenant applications with isolated memories

---

## Summary

**What you learned:**
- ✅ Set up Azure AI Foundry from scratch
- ✅ Deployed GPT-4 and embedding models
- ✅ Installed and configured Python SDK
- ✅ Created memory stores programmatically
- ✅ Stored and retrieved user preferences
- ✅ Used semantic search for memory retrieval
- ✅ Implemented user isolation with scopes

**Key takeaway:** Memory in Azure AI Foundry enables building intelligent agents that remember user context, preferences, and conversation history - making interactions more personalized and contextual.

---

## Need Help?

- Check troubleshooting section above
- Review `solution_memory.py` for working example
- Verify all deployment names match exactly
- Ensure environment variables are set correctly

**Good luck! 🚀**
