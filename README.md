Here is your **full, professional, ready-to-publish README.md** — clean, modern, beautifully formatted, and fully aligned with your actual codebase.

---

# 📚 **Library Desk Agent**

### *An Intelligent Autonomous AI Agent for Library Management*

The **Library Desk Agent** is a fully autonomous, reasoning-driven library assistant built with **Python, Flask, SQLite, and Ollama (LLaMA 3.1)**.
It combines natural language understanding, planning, tool execution, and a modern chat UI to deliver a real, functional, end-to-end AI Agent.

The system intelligently handles book search, ordering, restocking, pricing, and inventory analysis — all via natural conversation.

---

## 🚀 **Features**

* 🔍 **Natural-language book search** (title + author)
* 🧾 **Create customer orders** with automatic stock updates
* 📦 **Restock books** intelligently by title
* 💲 **Edit book prices** directly
* 🛠️ **Full tool-calling system** using structured JSON for agent actions
* 🧠 **Short-term memory** stored in SQLite (last 3 messages)
* 🔄 **Multi-step reasoning agent loop** (up to 2 steps)
* 📊 **Inventory summary** with low-stock detection
* 💬 **Modern interactive chat UI** (typing indicator, animations, real-time messaging)
* 🗄️ **Database inspector** for debugging (books, orders, messages, tools)

---

## 🧰 **Tech Stack**

### **Backend**

* Python 3.x
* Flask + CORS
* SQLite3
* Ollama (LLaMA 3.1)
* Structured Tool Calling
* REST API (`/chat` endpoint)

### **Frontend**

* HTML5, CSS3, JavaScript
* FontAwesome Icons
* Responsive modern UI

---

## 📁 **Folder Structure**

```
library_agent/
│── agent.py
│── tools.py
│── libraryDB.py
│── TestDB.py
│── user_interface.py
│── app/
│    └── index.html
│── library.db   (auto-created)
│── README.md
```

---

## ⚙️ **Installation Guide**

### **1️⃣ Install Python dependencies**

```bash
pip install flask flask-cors openai requests
```

### **2️⃣ Install & run Ollama**

Download: [https://ollama.com/download](https://ollama.com/download)

Then pull the model:

```bash
ollama pull llama3.1
```

### **3️⃣ Initialize the database**

```bash
python libraryDB.py
```

This will create tables + insert seed data ✔

### **4️⃣ Run the backend**

```bash
python user_interface.py
```

### **5️⃣ Open the frontend**

Open:

```
app/index.html
```

---

## ▶️ **How to Run the Project**

### **Start the Flask server**

```bash
python user_interface.py
```

Backend now listens on:

```
http://127.0.0.1:5000/chat
```

### **Open the chat UI**

Simply open `index.html` in your browser.

---

## 🔌 **API / Agent Workflow**

### **POST /chat**

The frontend sends:

```json
{
  "message": "Find clean code book",
  "session_id": "optional"
}
```

Backend returns:

```json
{
  "reply": "Found 2 matching books...",
  "session_id": "d2c1-9321-..."
}
```

### **Agent → Tools (from agent.py)**

Tools include:

```python
find_books(q)
create_order(customer_id, items)
restock_book(title, qty)
update_price(isbn, price)
order_status(order_id)
inventory_summary(threshold)
log_message(...)
```



The agent will **think → choose tool → request → receive → answer**.



---

## 📘 **Usage Examples**

### ➤ Search for books

```
Find books by Robert Martin
```

### ➤ Create an order

```
Create an order for customer 2:  
3 copies of Clean Code and 1 copy of The Pragmatic Programmer.
```

### ➤ Restock a book

```
Restock Clean Architecture by 5
```

### ➤ Check order status

```
What is the status of order 3?
```

---

## 🔮 **Future Improvements**

* Add authentication system
* Add long-term memory with vector DB
* Add analytics dashboard
* Improve UI with React or Vue
* Add voice assistant mode
* Add more complex multi-step agent planning


