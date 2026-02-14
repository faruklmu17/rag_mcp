# Example Queries for the LLM

Once you run `python llm_client.py`, you can ask questions like these:

## Basic Queries

**Q: What assignments does Alice Smith have?**
> The LLM will query the MCP server and tell you all of Alice's assignments with their statuses.

**Q: Which work items are currently in Testing status?**
> Lists all items being tested and who's working on them.

**Q: How many assignments are in each status?**
> Provides a breakdown/summary of the agile board.

## Analysis Queries

**Q: Are there any items in "Ready for QA" status?**
> This will reveal the intentional bug - there IS a "Ready for QA" item in the database!

**Q: Which engineers are working on defects vs stories?**
> Analyzes the type of work each engineer is doing.

**Q: What's the current workload distribution across engineers?**
> Shows how many assignments each engineer has.

## QA-Focused Queries

**Q: Are there any status values that seem unusual or unexpected?**
> The LLM might identify "Ready for QA" as unusual if it's not a standard agile status.

**Q: Compare the database statuses with the expected statuses: Developing, Under Review, Testing, Done**
> This will help identify the discrepancy that the tests are catching.

**Q: What work items have multiple engineers assigned?**
> Shows collaboration or handoffs between team members.

**Q: Summarize the current state of the agile board**
> Gets a high-level overview of all work in progress.

## Advanced Queries

**Q: Is there any work that Alice Smith started but someone else is now testing?**
> Traces work items through different engineers and statuses.

**Q: Generate a QA report for the current sprint**
> The LLM can create a formatted report based on the data.

**Q: What potential issues do you see in the current board state?**
> Let the LLM analyze and identify problems (like the "Ready for QA" status).

---

## How It Works

1. **You ask a question** → 
2. **llm_client.py connects to mcp_server.py** → 
3. **MCP server queries the SQLite database** → 
4. **Data is sent to Groq LLM with your question** → 
5. **LLM analyzes and responds** → 
6. **You get an intelligent answer!**

The key advantage: The LLM has **real-time access** to your database through MCP, so it always works with current data.

