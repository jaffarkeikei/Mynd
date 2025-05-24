# Mynd - Component Architecture

**Detailed visual guide to how each component works and interacts**

## 🏗️ Component Overview

### Core Components Structure
```mermaid
graph TB
    subgraph "User Interface Layer"
        CLI["💻 CLI Interface<br/>(src/cli.py)"]
        API["🌐 MCP API<br/>(Future: FastAPI)"]
    end
    
    subgraph "Application Layer"
        Main["🎯 Main Orchestrator<br/>(src/main.py)"]
        Extractor["🧠 Semantic Extractor<br/>(src/semantic_extractor.py)"]
        Privacy["🔒 Privacy Filter<br/>(Built into Extractor)"]
    end
    
    subgraph "Storage Layer"
        DB["📊 SQLite Database<br/>(src/database.py)"]
        Vector["🧠 Vector Storage<br/>(src/vector_storage.py)"]
        Files["📁 File System<br/>(.myndai/ directory)"]
    end
    
    subgraph "Data Models"
        Models["🗂️ Data Models<br/>(src/models.py)"]
    end
    
    CLI --> Main
    API --> Main
    Main --> Extractor
    Extractor --> Privacy
    Main --> DB
    Main --> Vector
    
    DB --> Files
    Vector --> Files
    
    Models -.-> Main
    Models -.-> DB
    Models -.-> Vector
    Models -.-> Extractor
    
    style Main fill:#f39c12,stroke:#333,stroke-width:3px
    style Extractor fill:#ff6b6b,stroke:#333,stroke-width:2px
    style Models fill:#4ecdc4,stroke:#333,stroke-width:2px
```

## 🔄 Component Interactions

### 1. CLI Command Flow
```mermaid
sequenceDiagram
    participant User as 👤 User
    participant CLI as 💻 CLI
    participant Main as 🎯 Main
    participant DB as 📊 Database
    participant Vector as 🧠 Vector Store
    participant Extractor as 🔍 Extractor
    
    User->>CLI: mynd demo
    CLI->>Main: initialize()
    Main->>DB: init_database()
    Main->>Vector: init_vector_store()
    Main->>Extractor: init_extractor()
    
    CLI->>Main: create_demo_data()
    Main->>Extractor: create_semantic_event()
    Extractor->>Extractor: extract_meaning()
    Extractor->>Main: return SemanticEvent
    Main->>DB: store_event()
    Main->>Vector: store_event()
    
    CLI->>User: ✅ Demo data created!
```

### 2. Query Processing Flow
```mermaid
sequenceDiagram
    participant User as 👤 User
    participant CLI as 💻 CLI
    participant Main as 🎯 Main
    participant Vector as 🧠 Vector Store
    participant DB as 📊 Database
    
    User->>CLI: mynd query "authentication"
    CLI->>Main: get_context_for_query()
    Main->>Vector: get_context_for_query()
    Vector->>Vector: semantic_search()
    Vector->>Vector: format_results()
    Vector->>Main: return formatted_context
    Main->>CLI: return context
    CLI->>User: 🔍 Display results
    
    Note over Vector: ChromaDB performs<br/>semantic similarity search
    Note over CLI: Results formatted with<br/>source info and tokens used
```

### 3. Data Storage Architecture
```mermaid
graph TB
    subgraph "Event Creation"
        Raw["📝 Raw Content"]
        Extract["🧠 Semantic Extraction"]
        Event["📋 SemanticEvent Object"]
    end
    
    subgraph "Dual Storage System"
        SQLite["📊 SQLite Database<br/>• Event metadata<br/>• Source information<br/>• Timestamps<br/>• Statistics"]
        
        ChromaDB["🧠 ChromaDB Vector Store<br/>• Semantic embeddings<br/>• Similarity search<br/>• Context retrieval<br/>• Smart ranking"]
    end
    
    subgraph "File System"
        UserDir["🏠 ~/.myndai/"]
        DBFile["📄 mynd.db"]
        VectorDir["📁 chroma_db/"]
        
        UserDir --> DBFile
        UserDir --> VectorDir
    end
    
    Raw --> Extract
    Extract --> Event
    Event --> SQLite
    Event --> ChromaDB
    
    SQLite --> DBFile
    ChromaDB --> VectorDir
    
    style Event fill:#f39c12,stroke:#333,stroke-width:2px
    style SQLite fill:#3498db,stroke:#333,stroke-width:2px
    style ChromaDB fill:#e74c3c,stroke:#333,stroke-width:2px
```

## 🧠 Semantic Extractor Deep Dive

### Semantic Processing Pipeline
```mermaid
graph LR
    subgraph "Input Processing"
        Content["📝 Raw Content"]
        PII["🔒 PII Detection"]
        Clean["✨ Cleaned Content"]
    end
    
    subgraph "LLM Processing"
        Local["🏠 Local LLM<br/>(Ollama)"]
        Fallback["🔧 Fallback Heuristics<br/>(If LLM unavailable)"]
    end
    
    subgraph "Output Generation"
        Summary["📋 Semantic Summary"]
        Concepts["🏷️ Key Concepts"]
        Decision["🤔 Decision Context"]
        Event["📦 SemanticEvent"]
    end
    
    Content --> PII
    PII --> Clean
    Clean --> Local
    Clean --> Fallback
    
    Local --> Summary
    Local --> Concepts
    Local --> Decision
    Fallback --> Summary
    Fallback --> Concepts
    Fallback --> Decision
    
    Summary --> Event
    Concepts --> Event
    Decision --> Event
    
    style PII fill:#ff6b6b,stroke:#333,stroke-width:2px
    style Local fill:#4ecdc4,stroke:#333,stroke-width:2px
    style Event fill:#f39c12,stroke:#333,stroke-width:2px
```

### Privacy Protection Flow
```mermaid
graph TB
    subgraph "Privacy Filter System"
        Input["📝 Raw Input"]
        
        subgraph "PII Detection"
            Email["📧 Email Addresses"]
            Phone["📞 Phone Numbers"]
            SSN["🆔 Social Security"]
            Cards["💳 Credit Cards"]
            Keys["🔑 API Keys"]
            Passwords["🔐 Passwords"]
        end
        
        Sanitized["✨ Sanitized Content"]
        
        subgraph "Safe Output"
            Summary["📋 Summary (No PII)"]
            Concepts["🏷️ Concepts Only"]
            Context["🤔 Decision Context"]
        end
    end
    
    Input --> Email
    Input --> Phone
    Input --> SSN
    Input --> Cards
    Input --> Keys
    Input --> Passwords
    
    Email --> Sanitized
    Phone --> Sanitized
    SSN --> Sanitized
    Cards --> Sanitized
    Keys --> Sanitized
    Passwords --> Sanitized
    
    Sanitized --> Summary
    Sanitized --> Concepts
    Sanitized --> Context
    
    style Input fill:#ff6b6b,stroke:#333,stroke-width:2px
    style Sanitized fill:#27ae60,stroke:#333,stroke-width:2px
```

## 📊 Database Schema & Relationships

### SQLite Database Structure
```mermaid
erDiagram
    EVENTS {
        string id PK
        string timestamp
        string source_type
        string source_path
        string semantic_summary
        string concepts
        string decision_context
        string metadata
    }
    
    AUDIT_LOG {
        int id PK
        string timestamp
        string event_type
        string ai_client
        string query_hash
        int context_tokens
        string capability_token_hash
        string ip_address
    }
    
    CAPABILITY_TOKENS {
        string token_id PK
        string client_id
        string scope
        string expires_at
        int max_tokens
        string created_at
        boolean is_active
    }
    
    EVENTS ||--o{ AUDIT_LOG : "referenced_in"
    CAPABILITY_TOKENS ||--o{ AUDIT_LOG : "used_for"
```

### Vector Storage Structure
```mermaid
graph TB
    subgraph "ChromaDB Collection"
        Collection["📚 semantic_events"]
        
        subgraph "Document Structure"
            Doc["📄 Document"]
            Embedding["🧮 Vector Embedding"]
            Metadata["📋 Metadata"]
        end
        
        subgraph "Metadata Fields"
            Source["source_type"]
            Path["source_path"]
            Time["timestamp"]
            Concepts["concepts"]
            Meta["meta_*"]
        end
    end
    
    Collection --> Doc
    Doc --> Embedding
    Doc --> Metadata
    
    Metadata --> Source
    Metadata --> Path
    Metadata --> Time
    Metadata --> Concepts
    Metadata --> Meta
    
    style Collection fill:#e74c3c,stroke:#333,stroke-width:2px
    style Embedding fill:#9b59b6,stroke:#333,stroke-width:2px
    style Metadata fill:#3498db,stroke:#333,stroke-width:2px
```

## 🔍 Query Processing Deep Dive

### Semantic Search Process
```mermaid
sequenceDiagram
    participant Q as 🔍 Query
    participant V as 🧠 Vector Store
    participant C as 📚 ChromaDB
    participant F as 🎯 Formatter
    
    Q->>V: search_similar(query, limit=20)
    V->>C: collection.query(query_texts=[query])
    C->>C: Generate query embedding
    C->>C: Compute similarity scores
    C->>C: Rank by relevance
    V->>V: Format results with metadata
    V->>F: get_context_for_query()
    F->>F: Optimize for token limits
    F->>F: Add source information
    F->>Q: Return formatted context
    
    Note over C: Semantic similarity search<br/>using sentence embeddings
    Note over F: Token optimization ensures<br/>results fit in AI context window
```

### Context Optimization Process
```mermaid
graph LR
    subgraph "Input"
        Query["🔍 User Query"]
        Limit["📏 Token Limit<br/>(4000 default)"]
    end
    
    subgraph "Processing"
        Search["🔍 Semantic Search"]
        Rank["📊 Relevance Ranking"]
        Compress["🗜️ Token Optimization"]
    end
    
    subgraph "Output"
        Context["📋 Formatted Context"]
        Sources["📚 Source Attribution"]
        Stats["📈 Token Usage Stats"]
    end
    
    Query --> Search
    Limit --> Compress
    Search --> Rank
    Rank --> Compress
    
    Compress --> Context
    Compress --> Sources
    Compress --> Stats
    
    style Search fill:#3498db,stroke:#333,stroke-width:2px
    style Compress fill:#f39c12,stroke:#333,stroke-width:2px
    style Context fill:#27ae60,stroke:#333,stroke-width:2px
```

## 🔧 CLI Interface Structure

### Command Architecture
```mermaid
graph TB
    subgraph "CLI Commands"
        Demo["🎬 mynd demo"]
        Query["🔍 mynd query"]
        Status["📊 mynd status"] 
        Init["🎯 mynd init"]
        Start["🚀 mynd start"]
        Capture["📥 mynd capture"]
    end
    
    subgraph "Core Functions"
        Main["🏗️ Main.py"]
        DB["📊 Database"]
        Vector["🧠 Vector Store"]
        Extract["🔍 Extractor"]
    end
    
    Demo --> Main
    Query --> Vector
    Status --> DB
    Init --> Main
    Start --> Main
    Capture --> Main
    
    Main --> DB
    Main --> Vector
    Main --> Extract
    
    style Demo fill:#f39c12,stroke:#333,stroke-width:2px
    style Query fill:#e74c3c,stroke:#333,stroke-width:2px
    style Status fill:#3498db,stroke:#333,stroke-width:2px
```

## 🚀 Future MCP Server Architecture

### Planned MCP Integration
```mermaid
graph TB
    subgraph "AI Clients"
        ChatGPT["💬 ChatGPT"]
        Claude["🤖 Claude"]
        Copilot["👨‍💻 Copilot"]
    end
    
    subgraph "MCP Server (FastAPI)"
        Auth["🔐 Authentication"]
        Capabilities["🎫 Capability Tokens"]
        Context["🔍 Context API"]
        Audit["📋 Audit Logging"]
    end
    
    subgraph "Mynd Core"
        Vector["🧠 Vector Store"]
        DB["📊 Database"]
        Security["🛡️ Security Layer"]
    end
    
    ChatGPT --> Auth
    Claude --> Auth
    Copilot --> Auth
    
    Auth --> Capabilities
    Capabilities --> Context
    Context --> Audit
    
    Context --> Vector
    Context --> DB
    Audit --> Security
    
    style Auth fill:#ff6b6b,stroke:#333,stroke-width:2px
    style Context fill:#4ecdc4,stroke:#333,stroke-width:2px
    style Security fill:#f39c12,stroke:#333,stroke-width:2px
```

## 🔒 Security Architecture

### Data Protection Layers
```mermaid
graph TB
    subgraph "Security Layers"
        L1["🏠 Local Processing<br/>All LLM inference on-device"]
        L2["🔒 PII Filtering<br/>Remove sensitive data"]
        L3["🔐 Encrypted Storage<br/>Local database encryption"]
        L4["🎫 Capability Tokens<br/>Time-limited access"]
        L5["📋 Audit Logging<br/>Track all access"]
    end
    
    subgraph "Threat Protection"
        External["🌐 External Threats<br/>Data never leaves device"]
        Internal["🏠 Internal Threats<br/>PII automatically removed"]
        Access["🔑 Unauthorized Access<br/>Token-based permissions"]
        Audit["📊 Forensics<br/>Complete access logs"]
    end
    
    L1 --> External
    L2 --> Internal
    L3 --> Internal
    L4 --> Access
    L5 --> Audit
    
    style L1 fill:#27ae60,stroke:#333,stroke-width:2px
    style L2 fill:#f39c12,stroke:#333,stroke-width:2px
    style L4 fill:#e74c3c,stroke:#333,stroke-width:2px
```

---

## 📚 Component File Reference

| Component | File | Purpose |
|-----------|------|---------|
| **Data Models** | `src/models.py` | Core data structures and types |
| **Database** | `src/database.py` | SQLite operations and schema |
| **Vector Store** | `src/vector_storage.py` | ChromaDB semantic search |
| **Semantic Extractor** | `src/semantic_extractor.py` | LLM processing and privacy |
| **Main Orchestrator** | `src/main.py` | Application coordination |
| **CLI Interface** | `src/cli.py` | Command-line interface |

Each component is designed to be **modular**, **testable**, and **independently maintainable** while working together seamlessly to provide the universal AI memory experience. 