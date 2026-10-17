# DevTrack API

DevTrack is a minimal, high-performance engineering issue tracking backend built with Django. It allows software teams to register core issue reporters, enforce data validation constraints using custom Python classes, and manage issue life cycles across dynamic polymorphic priority boundaries. 

---

## 🚀 How to Run the Project

Follow these steps sequentially to configure your local workspace environment and boot up the API application server.

### 1. Initialize Workspace & Install Dependencies
Open your terminal application, navigate straight into the root folder containing the project configuration setups, and download the web core frameworks:
```bash
# Navigate into the project root directory
cd devtrack

# Install required package engines from your layout settings
pip install -r requirements.txt
```

### 2. Launch the Local Development Server
Execute the default management framework script to spin up the local service loop:
```bash
python manage.py runserver
```
Upon execution, your console will output confirmation logs indicating that the application layer is healthy. The server is officially active and listening for network traffic locally at:
👉 **`http://127.0.0`**

### 3. Stop the Application Server
Whenever you finish evaluating routes or want to pause development, navigate back to your running terminal window and execute this key command shortcut:
* **All Platforms (Windows, macOS, Linux):** Press **`Ctrl + C`**

---

## 📡 API Endpoint Reference Documentation

All request parameters and payloads are transmitted using structural `application/json` string encoding standards.

### 👤 Reporter Management

#### `POST /api/reporters/`
* **Purpose:** Registers a new engineering contributor team profile.
* **Payload Request Body Example:**
  ```json
  {
      "name": "Alice Dev",
      "email": "alice@company.com",
      "team": "backend"
  }
  ```
* **Success Response (`201 Created`):**
  ```json
  {
      "id": 1,
      "name": "Alice Dev",
      "email": "alice@company.com",
      "team": "backend"
  }
  ```
* **Validation Bounds:** Throws a `400 Bad Request` if the `name` field is omitted or empty, or if the `email` string does not contain a valid `@` symbol delimiter character.

<img width="659" height="407" alt="image" src="https://github.com/user-attachments/assets/9edfe90f-4997-4fc9-b31b-10434357241b" />

#### `GET /api/reporters/`
* **Purpose:** Extracts a full array list containing all engineers registered across the workspace.
* **Success Response (`200 OK`):** A JSON array populated with all existing reporter profiles.

---

### 🐛 Issue Tracking

#### `POST /api/issues/`
* **Purpose:** Creates a tracking ticket bound to an existing reporter profile.
  <img width="669" height="428" alt="image" src="https://github.com/user-attachments/assets/d82a082c-999f-4e3e-b255-484bed83558d" />

* **Success Response (`201 Created`):**
  ```json
  {
      "id": 1,
      "title": "Database Connection Drop",
      "description": "Connection pool overflow caught under high stress.",
      "status": "open",
      "priority": "critical",
      "reporter_id": 1,
      "created_at": "2026-10-17 21:30:15.123456",
      "description_text": "[URGENT] Database Connection Drop — needs immediate attention"
  }
  ```
* **Validation Bounds:** Verifies that the requested `reporter_id` matches an existing record in `reporters.json`. Throws a `400 Bad Request` if `title` or `description` are missing, or if invalid choice limits are sent for `status` or `priority`.

#### `GET /api/issues/`
* **Purpose:** Reconstructs and reads a list of all tracked tickets.
* **Success Response (`200 OK`):** Returns an array list where each item includes its dynamically evaluated `description_text` message string based on its concrete priority classification.

#### `GET /api/issues/<int:pk>/`
* **Purpose:** Inspects and returns a single tracked issue based on its unique primary integer index identifier (`pk`).
* **Success Response (`200 OK`):** Returns the matching individual issue object structure layout containing its custom polymorphic description parameters. Returns a `404 Not Found` payload error structure if the index target does not exist.

---

## 🏗️ Core Design Decisions

### 🌟 Explict Polymorphic Instantiation in View Handlers
Rather than hiding class selection logic within abstract factory layers or mapping methods, we made the explicit choice to **instantiate priority subclasses (`CriticalIssue` and `LowPriorityIssue`) directly inside the Django route controller view functions**. 

#### **Why I Made This Decision:**
1. **Plain-Text Data Storage Limitations:** Because flat JSON storage structures (`issues.json`) can only read and write basic data models (dictionaries/strings), they lose all native Python subclass identities when saved to disk.
2. **Maximum Code Transparency:** Placing the branching structure (`if priority == 'critical':`) directly in the view functions makes the code exceptionally easy to trace. A developer reading the `POST` or `GET` paths can immediately see how a incoming string like `"critical"` transforms into a specific `CriticalIssue` instance.
3. **Decoupled Architecture:** This approach separates our data storage functions from our application logic. The storage manager functions solely as a reader and writer for our JSON files, while our views explicitly enforce our Object-Oriented object behaviors right before executing `.validate()` and `.describe()`.
