# 📚 **Library Desk Agent**

### **An Intelligent Autonomous AI Agent for Library Management**

The **Library Desk Agent** is a fully autonomous, reasoning-driven library assistant built using **Python, Flask, SQLite, and Ollama (LLaMA 3.1)**.
It performs real-world operations such as book search, ordering, stock updates, and inventory analysis using **natural conversation, multi-step reasoning, and structured tool calling**.

---

# 🚀 **Features**

* 🔍 **Natural-language book search** (by title or author)
* 🧾 **Create customer orders** with automatic stock reduction
* 📦 **Restock books** by title with real DB updates
* 💲 **Update book prices** instantly
* 🛠️ **Structured JSON Tool Calling System**
* 🧠 **Short-term memory** (last 3 messages stored in SQLite)
* 🔄 **Multi-step reasoning loop** (up to 2 steps for performance)
* 📊 **Inventory summary** detecting low-stock books
* 💬 **Modern chat UI** with typing animation + real-time messages
* 🗄️ **Built-in DB Inspector** (books, orders, messages, tools)

---

# 🧰 **Tech Stack**

### **Backend**

* Python 3.x
* Flask + CORS
* SQLite3
* Ollama (LLaMA 3.1)
* Structured Tool Calling
* REST API (`/chat` endpoint)

### **Frontend**

* HTML5 + CSS3 + JavaScript
* FontAwesome Icons
* Responsive UI with animations

---

# 📁 **Folder Structure**

```
library_agent/
│── agent.py
│── tools.py
│── libraryDB.py
│── TestDB.py
│── user_interface.py
│── app/
│    └── index.html
│── library.db          # auto-created
│── README.md
```

---

# ⚙️ **Installation Guide**

### **1️⃣ Install Python dependencies**

```bash
pip install flask flask-cors openai requests
```

### **2️⃣ Install & run Ollama**

Download from: [https://ollama.com/download](https://ollama.com/download)

Then pull the model:

```bash
ollama pull llama3.1
```

### **3️⃣ Initialize the database**

```bash
python libraryDB.py
```

Creates all tables + seed data ✔

### **4️⃣ Run the backend**

```bash
python user_interface.py
```

### **5️⃣ Open the frontend**

Simply open:

```
app/index.html
```

---

# ▶️ **How to Run the Project**

### **Start backend**

```bash
python user_interface.py
```

Server runs at:

```
http://127.0.0.1:5000/chat
```

### **Open UI**

Open the file:

```
app/index.html
```

The agent now responds in real time and calls tools automatically.

---

# 🔌 **API + Agent Workflow**

### **📨 Frontend → Backend**

POST `/chat`

```json
{
  "message": "Find clean code book",
  "session_id": "optional"
}
```

### **📤 Backend → Frontend**

```json
{
  "reply": "Found 2 matching books...",
  "session_id": "d2c1-9321-..."
}
```

---

# 🤖 **Agent → Tools System**

The agent can call any of the following tools:

* `find_books(q)`
* `create_order(customer_id, items)`
* `restock_book(title, qty)`
* `update_price(isbn, price)`
* `order_status(order_id)`
* `inventory_summary(threshold)`
* `log_message(...)`

Workflow:

1. Agent thinks internally
2. Chooses best tool
3. Executes it
4. Reads the DB result
5. Sends final natural-language reply

---

# 📘 **Usage Examples**

### 🔎 **Search for books**

> Find books by Robert Martin

### 🧾 **Create an order**

> Create an order for customer 2: 3 copies of Clean Code and 1 copy of The Pragmatic Programmer

### 📦 **Restock**

> Restock Clean Architecture by 5

### 🧪 **Order status**

> What is the status of order 3?

---

# 📉 **Database Inspector (Debug Tools)**

Run:

```bash
python TestDB.py
```

See:

* books
* customers
* orders
* messages
* tool_calls

---

# 🔮 **Future Improvements**

* 🔐 Add authentication
* 🧠 Add long-term memory using vector DB
* 📊 Analytics dashboard
* 🎨 Rebuild UI using React or Vue
* 🎙️ Add voice-assistant mode
* 🧩 Enhance multi-step planning & chain-of-thought
