from tools import find_books, create_order, restock_book, update_price, order_status, inventory_summary,log_message,get_connection
import json, requests
import uuid
from datetime import datetime
from openai import OpenAI
MAX_STEPS = 2
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1"


def ask_ollama(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": get_tool_specs(),
        "stream": False
    }

    res = requests.post(OLLAMA_URL, json=payload)
    res.raise_for_status()
    return res.json()


def get_tool_specs():
    return [
        {
            "type": "function",
            "function": {
                "name": "find_books",
                "description": "Search for books by title keywords",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "q": {"type": "string", "description": "Keyword in title to search"}
                    },
                    "required": ["q"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_order",
                "description": "Create a new order and reduce stock",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "integer"},
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "isbn": {"type": "string"},
                                    "qty": {"type": "integer"}
                                },
                                "required": ["isbn", "qty"]
                            }
                        }
                    },
                    "required": ["customer_id", "items"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "restock_book",
                "description": "Restock a book by title and quantity",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Book title"},
                        "qty": {"type": "integer", "description": "Quantity to add"}
                    },
                    "required": ["title", "qty"]
                }
            }
        }
    ,
        {
            "type": "function",
            "function": {
                "name": "update_price",
                "description": "Update the price of a book",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "isbn": {"type": "string"},
                        "price": {"type": "number"}
                    },
                    "required": ["isbn", "price"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "order_status",
                "description": "Get details about a specific order",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "integer"}
                    },
                    "required": ["order_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "inventory_summary",
                "description": "Show all books with low stock",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "threshold": {"type": "integer", "description": "Stock threshold to detect low stock"}
                    },
                    "required": []
                }
            }
        }
    ]
def get_history(session_id, limit=3):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT role, content 
        FROM messages
        WHERE session_id=?
        ORDER BY id DESC
        LIMIT ?
    """, (session_id, limit))

    rows = cur.fetchall()
    conn.close()

    history = []
    for role, content in reversed(rows):
        history.append({"role": role, "content": content})
    return history


def chat(user_input: str, session_id=None):

    if not session_id:
        session_id = str(uuid.uuid4())

    log_message(session_id, "user", user_input)

    system_prompt = """
    You are an advanced autonomous Library Desk AI Agent.

    ===============================
    ### CORE BEHAVIOR
    You MUST behave as:
    - A reasoning agent
    - A planning agent
    - A multi-step tool-using agent
    - A system that follows strict rules

    Your mission:
    - Understand the user perfectly
    - Think before you act
    - Create a plan internally (not visible to user)
    - Decide the best tool to use (if any)
    - Execute multi-step tasks when needed
    - Produce clear, natural final answers

    ===============================
    ### THINKING RULES
    Before ANY action:
    - Think internally step-by-step (NOT visible to the user)
    - Check if user intent is clear
    - Check if any tool is required
    - If arguments are missing, ask the user
    - NEVER assume values
    - NEVER hallucinate tool parameters

    ===============================
    ### TOOL CALL RULES
    If a tool is needed:
    You MUST output ONLY the JSON structure below:

    {
      "tool_calls": [
        {
          "type": "function",
          "function": {
            "name": "<tool_name>",
            "arguments": { ... }
          }
        }
      ]
    }

    RULES:
    - No comments
    - No explanation
    - No markdown
    - No surrounding text
    - No additional fields
    - Parameters must be valid JSON only

    ===============================
    ### OBSERVATION RULES
    After tool execution, the system will send you a response with:
    role = "tool"
    content = the result

    You MUST:
    - Read the tool result carefully
    - Update your plan if needed
    - Then produce the FINAL ANSWER (no JSON)

    ===============================
    ### FINAL ANSWER RULES
    After receiving tool results:
    - Produce a friendly, helpful, natural answer
    - NO JSON allowed
    - NO tool calls
    - NO markdown
    - ONLY plain text
    - Final answers MUST be short, concise, and to-the-point.
    - Maximum length: 1–2 sentences.
    - Do NOT include unnecessary explanations.
    - Do NOT repeat tool information or ask for confirmations unless required.
    - Strictly return the result the user needs.

    ===============================
    ### ERROR & RECOVERY RULES
    If a tool result shows an error:
    - Re-evaluate your plan
    - Explain the issue to the user
    - Ask for corrected information
    - Or try again with a new tool call

    ===============================
    ### MEMORY RULES
    Use prior conversation messages as context.
    Remain consistent with earlier information.

    ===============================
    ### TONE
    Professional, helpful, concise, clear.
    """

    messages = [{"role":"system", "content": system_prompt}]
    messages.extend(get_history(session_id))
    messages.append({"role":"user", "content": user_input})

    for step in range(MAX_STEPS):

        response = ask_ollama(messages)
        msg = response.get("message", {})


        tool_calls = msg.get("tool_calls", [])
        if not tool_calls:
            final_answer = msg.get("content", "")
            log_message(session_id, "assistant", final_answer)
            return final_answer

        for call in tool_calls:
            fn = call["function"]["name"]
            args = call["function"].get("arguments", {})


            if fn == "find_books":
                result = find_books(**args)
            elif fn == "create_order":
                result = create_order(**args)
            elif fn == "restock_book":
                result = restock_book(**args)
            elif fn == "update_price":
                result = update_price(**args)
            elif fn == "order_status":
                result = order_status(**args)
            elif fn == "inventory_summary":
                result = inventory_summary(**args) if args else inventory_summary()
            else:
                result = {"error": "unknown tool"}


            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO tool_calls (session_id,name,args_json,result_json,created_at)
                VALUES (?,?,?,?,?)
            """, (
                session_id, fn,
                json.dumps(args), json.dumps(result),
                datetime.now().isoformat()
            ))
            conn.commit()
            conn.close()

            messages.append({
                "role": "tool",
                "content": json.dumps(result)
            })

    return "Could not complete request"


# if __name__ == "__main__":
#     print(chat("We sell 3 copies of Clean Code to customer 2 today"))
#     print(chat("restock the pragmatic programmer by 10"))
#     print(chat("What’s the status of order 3?"))



