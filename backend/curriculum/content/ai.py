TRACK = {
    "slug": "ai",
    "name": "AI Engineering",
    "tagline": "How LLMs, embeddings, RAG, and autonomous agents actually work under the hood.",
    "description": (
        "Start from absolute zero. Learn machine learning fundamentals, how vectors power semantic search, "
        "how LLMs generate tokens, prompt engineering strategies, and build RAG pipelines and AI agents."
    ),
    "icon": "✦",
    "accent": "#b37feb",
    "order": 6,
    "required_xp": 1500,
    "levels": [
        # =========================================================================
        # LEVEL 1: AI & MACHINE LEARNING FOUNDATIONS
        # =========================================================================
        {
            "index": 1,
            "title": "AI & Machine Learning Foundations from Zero",
            "summary": "Rules vs learning from data, supervised vs unsupervised, weights, loss functions, and inference.",
            "xp_reward": 85,
            "lessons": [
                {
                    "title": "Rules vs Learning: A Paradigm Shift",
                    "minutes": 6,
                    "body": """In traditional programming, human engineers write explicit rules:
$$\\text{Rules} + \\text{Data} \\longrightarrow \\text{Answers}$$

```python
# Traditional rules-based approach:
if "free money" in email and "click here" in email:
    return "SPAM"
```
This fails the moment spammers write `"fr3e m0ney"` or new attack patterns emerge.

### The Machine Learning Paradigm
In Machine Learning (ML), we invert the equation:
$$\\text{Data} + \\text{Answers (Labels)} \\longrightarrow \\text{Learned Model (Rules)}$$

We feed the computer 500,000 example emails labeled as *spam* or *ham*. The algorithm automatically discovers mathematical patterns that distinguish them.""",
                },
                {
                    "title": "How Models Learn: Weights, Loss & Gradient Descent",
                    "minutes": 6,
                    "body": """At its core, a neural network is a giant mathematical function:
$$\\hat{y} = f(W \\cdot X + b)$$
- $X$: The input data (e.g. pixels, words).
- $W$: **Weights** (parameters that determine the strength of connections).
- $b$: **Biases** (offsets).
- **Loss Function**: A metric calculating how wrong the model's prediction is compared to the true answer.

### Training vs Inference
- **Training Phase**: The model makes guesses, calculates loss, and adjusts its millions (or billions) of weights using **Gradient Descent** until the error is minimized. This takes hours or weeks on clusters of GPUs.
- **Inference Phase**: The weights are locked (frozen). The model accepts a new input and calculates an output prediction in milliseconds.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Supervised Learning Definition",
                    "prompt": "What defines Supervised Learning compared to other branches of Machine Learning?",
                    "hint": "What does the model have access to during training?",
                    "explanation": "Supervised learning trains models on labeled datasets consisting of input-output pairs.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "Training on labeled examples consisting of input-target pairs",
                            "Letting the computer learn without any data",
                            "A human watching the computer screen while it runs",
                            "Rules written entirely with if/else statements",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "multi",
                    "difficulty": "easy",
                    "title": "Core Components of a Neural Network",
                    "prompt": "Which of the following are foundational mathematical components that define a neural network?",
                    "hint": "Parameters adjusted during training to minimize error.",
                    "explanation": "Weights, biases, and loss functions are core elements of neural networks.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Weights (learnable parameters)",
                            "Biases (learnable offsets)",
                            "Loss function (measures prediction error)",
                            "HDMI monitor refresh rates",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Production Prediction Phase",
                    "prompt": "What is the technical term for the production phase where a pre-trained model generates predictions on new data with frozen weights?",
                    "hint": "Starts with 'inf...'",
                    "explanation": "Inference is the phase where a trained model processes inputs to generate predictions.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. inference"},
                    "solution": {"regex": True, "accept": [r"^inference$"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Threshold Sentiment Classifier",
                    "prompt": "Write `classify_sentiment(score, threshold)` simulating a binary classification decision boundary:\n- If `score >= threshold`: return `\"positive\"`\n- If `score <= -threshold`: return `\"negative\"`\n- Otherwise: return `\"neutral\"`\n\n```python\nclassify_sentiment(0.8, 0.5) -> \"positive\"\nclassify_sentiment(-0.9, 0.5) -> \"negative\"\nclassify_sentiment(0.2, 0.5) -> \"neutral\"\n```",
                    "hint": "Check greater than or equal to positive threshold, then less than or equal to negative threshold.",
                    "explanation": "Decision boundaries turn raw numerical model outputs into discrete categorical classifications.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def classify_sentiment(score, threshold):\n    # Return 'positive', 'negative', or 'neutral'\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "classify_sentiment",
                        "cases": [
                            {"args": [0.8, 0.5], "expect": "positive"},
                            {"args": [-0.9, 0.5], "expect": "negative"},
                            {"args": [0.2, 0.5], "expect": "neutral"},
                            {"args": [0.5, 0.5], "expect": "positive"},
                            {"args": [-0.5, 0.5], "expect": "negative", "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 2: EMBEDDINGS & VECTOR SEARCH
        # =========================================================================
        {
            "index": 2,
            "title": "Embeddings & Vector Semantic Search",
            "summary": "Dense vectors, high-dimensional space, cosine similarity, and why keyword search fails.",
            "xp_reward": 95,
            "lessons": [
                {
                    "title": "Why Computers Can't Read: Embeddings from Zero",
                    "minutes": 6,
                    "body": """Computers cannot understand the concept of a "cat" or "queen". They only operate on numbers.

### The Failure of Keyword Search
If a user searches for `"canine veterinarian"`, traditional keyword search looks for exact character matches. Documents containing `"dog doctor"` will be completely missed!

### What is an Embedding?
An **embedding model** (such as `text-embedding-3-small`) transforms any text into a **dense vector** (a list of 1,536 floating-point numbers):
```python
"puppy" -> [0.021, -0.045, 0.812, ... 1536 dimensions]
"dog"   -> [0.019, -0.043, 0.805, ... 1536 dimensions]
"apple" -> [-0.512, 0.221, -0.091, ... 1536 dimensions]
```
Words with similar meanings point in the **exact same direction** in high-dimensional space!""",
                },
                {
                    "title": "Measuring Semantic Closeness: Cosine Similarity",
                    "minutes": 6,
                    "body": """To find documents relevant to a search query:
1. Convert the user's query into a vector $\\vec{u}$.
2. Convert all database documents into vectors $\\vec{v}_1, \\vec{v}_2, \\dots$.
3. Measure the **angle** between the query vector and document vectors using **Cosine Similarity**:

$$\\text{Cosine Similarity} = \\frac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{u}\\| \\|\\vec{v}\\|} = \\frac{\\sum_{i} u_i v_i}{\\sqrt{\\sum_i u_i^2} \\sqrt{\\sum_i v_i^2}}$$

- Value is **+1.0**: Pointing in the exact same direction (identical meaning).
- Value is **0.0**: Orthogonal (completely unrelated).
- Value is **-1.0**: Opposite meaning.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Semantic Vector Search Advantage",
                    "prompt": "Why does vector semantic search outperform traditional keyword matching (like SQL LIKE or grep)?",
                    "hint": "What happens when words have different spelling but identical meaning?",
                    "explanation": "Vector search captures conceptual meaning and synonyms, matching queries to documents even when they share no identical words.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "It matches conceptual meaning and synonyms rather than exact word spellings",
                            "It runs without needing an internet connection or RAM",
                            "It converts text into MP3 audio files",
                            "It guarantees 100% correct factual answers",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Vector Similarity Metric",
                    "prompt": "What common trigonometric similarity metric computes the cosine of the angle between two embedding vectors?",
                    "hint": "Cosine ...",
                    "explanation": "Cosine similarity measures vector directional alignment.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. cosine similarity"},
                    "solution": {"regex": True, "accept": [r"cosine(\s+similarity)?", r"COSINE(\s+SIMILARITY)?"]},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Vector Embedding Properties",
                    "prompt": "Which of the following statements are true about modern text embeddings?",
                    "hint": "Think about dimensionality, vector lengths, and semantic relationships.",
                    "explanation": "Embeddings represent text as fixed-dimension arrays of floats where semantically similar texts are geometrically close.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "They represent text as a fixed-length list of floating-point numbers",
                            "Texts with similar semantic meanings produce vectors that are close in space",
                            "Every English word has exactly 1 character in an embedding",
                            "They can be indexed in vector databases like pgvector for fast retrieval",
                        ]
                    },
                    "solution": {"answers": [0, 1, 3]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Calculate Cosine Similarity",
                    "prompt": "Write `cosine_similarity(vec_a, vec_b)` that computes the cosine similarity between two lists of floats.\nFormula:\n`dot_product / (norm_a * norm_b)`\n- `norm = sqrt(sum(x**2 for x in vec))`\n- If either norm is 0, return `0.0`\n- Return the result rounded to 4 decimal places\n\n```python\ncosine_similarity([1.0, 0.0], [1.0, 0.0]) -> 1.0\ncosine_similarity([1.0, 0.0], [0.0, 1.0]) -> 0.0\n```",
                    "hint": "Import math and use `math.sqrt`. Compute dot product as `sum(a * b for a, b in zip(vec_a, vec_b))`.",
                    "explanation": "Cosine similarity measures directional alignment between high-dimensional vector representations.",
                    "xp": 45,
                    "config": {
                        "language": "python",
                        "starter": "import math\n\ndef cosine_similarity(vec_a, vec_b):\n    # Return cosine similarity rounded to 4 decimal places\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "cosine_similarity",
                        "cases": [
                            {"args": [[1.0, 0.0], [1.0, 0.0]], "expect": 1.0},
                            {"args": [[1.0, 0.0], [0.0, 1.0]], "expect": 0.0},
                            {"args": [[0.0, 0.0], [1.0, 1.0]], "expect": 0.0},
                            {"args": [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]], "expect": 1.0},
                            {"args": [[1.0, 2.0], [2.0, 1.0]], "expect": 0.8, "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 3: HOW LARGE LANGUAGE MODELS WORK
        # =========================================================================
        {
            "index": 3,
            "title": "How Large Language Models (LLMs) Work",
            "summary": "Tokens and BPE, autoregressive next-token prediction, temperature, and hallucinations.",
            "xp_reward": 105,
            "lessons": [
                {
                    "title": "Tokens & The Autoregressive Loop",
                    "minutes": 6,
                    "body": """LLMs (like GPT-4 or Claude) do not read words or sentences. They operate on **Tokens**.

### Tokenization (Byte-Pair Encoding)
A tokenizer breaks text into chunks of letters:
- Common words are single tokens: `"the"` $\\rightarrow$ `[262]`
- Rare words are split into subwords: `"unbelievable"` $\\rightarrow$ `["un", "believ", "able"]`
- On average in English, 1 token $\\approx$ 4 characters (or ~0.75 words).

### The Autoregressive Engine
An LLM has one fundamental job:
**Given a sequence of tokens, predict the probability distribution over all possible next tokens.**

```
Prompt: "The capital of France is"
Model computes probabilities:
- "Paris": 92.4%
- "a": 2.1%
- "not": 0.8%
```
The model picks one token, appends it to the prompt, and repeats! This is why it is called **autoregressive**.""",
                },
                {
                    "title": "Sampling: Temperature, Top-P & Hallucination",
                    "minutes": 6,
                    "body": """How does the model choose which token to output from its probability distribution?

### Temperature ($T$)
- **$T = 0.0$ (Greedy Decoding)**: Always pick the #1 most probable token. 100% deterministic and repetitive. Best for math, code, and structured JSON.
- **$T = 0.7$ (Balanced)**: Balances accuracy with natural phrasing.
- **$T = 1.5$ (High Randomness)**: Flattens probabilities, making rare words much more likely. Creative, but prone to incoherence.

### Why Do LLMs Hallucinate?
LLMs are **next-token statistical simulators**, not verified knowledge databases. If asked about a fictional book, they generate tokens that sound syntactically and stylistically convincing, even if completely fabricated.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "The Autoregressive Primitive",
                    "prompt": "What is the core prediction task performed by an autoregressive Large Language Model on every step?",
                    "hint": "What does the model predict next?",
                    "explanation": "LLMs predict the probability distribution of the single next token given the preceding sequence of tokens.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "Predicting the probability distribution of the next token",
                            "Rendering an entire document all at once as an image",
                            "Executing SQL queries directly on disk",
                            "Compiling C++ code into machine assembly",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Temperature Setting for JSON Extraction",
                    "prompt": "You are building a pipeline that extracts structured JSON data from legal contracts. What temperature setting should you use?",
                    "hint": "Do you want creativity or maximum determinism?",
                    "explanation": "Temperature 0 (or near 0) eliminates random variation and guarantees deterministic, consistent outputs.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "0.0 (maximum determinism and consistency)",
                            "1.5 (maximum creativity and poetic variance)",
                            "100.0 (uniform random sampling)",
                            "Negative temperature (-1.0)",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Deterministic Decoding Name",
                    "prompt": "What is the name of the decoding strategy where the model always picks the single token with the highest probability (equivalent to Temperature 0)?",
                    "hint": "Greedy ...",
                    "explanation": "Greedy decoding selects the argmax token at each step.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. greedy"},
                    "solution": {"regex": True, "accept": [r"greedy(\s+decoding)?", r"GREEDY(\s+DECODING)?"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Compute Softmax Probabilities",
                    "prompt": "Write `softmax(logits)` that converts a list of float logits into normalized probabilities summing to 1.0.\nFormula:\n`p_i = exp(l_i - max(logits)) / sum(exp(l_j - max(logits)))`\n- Subtracting `max(logits)` prevents exponential overflow\n- Round each probability to 4 decimal places\n\n```python\nsoftmax([0.0, 0.0]) -> [0.5, 0.5]\nsoftmax([10.0, 10.0]) -> [0.5, 0.5]\n```",
                    "hint": "Import math, compute `max_l = max(logits)`, `exps = [math.exp(x - max_l) for x in logits]`, and divide by sum.",
                    "explanation": "Softmax transforms raw unnormalized neural network logit outputs into valid probability distributions.",
                    "xp": 45,
                    "config": {
                        "language": "python",
                        "starter": "import math\n\ndef softmax(logits):\n    # Return list of probabilities rounded to 4 decimals\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "softmax",
                        "cases": [
                            {"args": [[0.0, 0.0]], "expect": [0.5, 0.5]},
                            {"args": [[10.0, 10.0]], "expect": [0.5, 0.5]},
                            {"args": [[1.0]], "expect": [1.0]},
                            {"args": [[0.0, 1.0]], "expect": [0.2689, 0.7311], "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 4: PROMPT ENGINEERING & STRUCTURED OUTPUTS
        # =========================================================================
        {
            "index": 4,
            "title": "Prompt Engineering & Structured Outputs",
            "summary": "System prompts, zero-shot vs few-shot, Chain-of-Thought reasoning, and extracting reliable JSON.",
            "xp_reward": 115,
            "lessons": [
                {
                    "title": "Prompt Anatomy: System, User & Few-Shot",
                    "minutes": 6,
                    "body": """A prompt is not just a query; it is a program written in natural language.

### Modern Chat Roles
- **System Prompt**: Sets global personality, behavioral boundaries, and output format rules:
  `"You are a strict data extraction engine. Output valid JSON only."`
- **User Prompt**: The dynamic query or document to process.
- **Assistant**: Past turns in the conversation.

### Zero-Shot vs Few-Shot Prompting
- **Zero-Shot**: Asking the model to perform a task with zero prior examples.
- **Few-Shot**: Providing 2 or 3 input/output demonstrations in the prompt:
```
Input: "Great battery life!" -> Sentiment: POSITIVE
Input: "Broke after 2 days."  -> Sentiment: NEGATIVE
Input: "Arrived on Tuesday."  -> Sentiment:
```
Few-shot examples drastically boost accuracy and enforce exact formatting!""",
                },
                {
                    "title": "Chain-of-Thought (CoT) & JSON Extraction",
                    "minutes": 6,
                    "body": """When an LLM answers immediately, it must commit to the first token without having computed intermediate reasoning steps.

### Chain-of-Thought Reasoning
Instructing the model to:
`"Think step-by-step and show your reasoning before emitting the final answer."`
allows the model to use previous generated tokens as an extended "scratchpad", drastically improving math, logic, and code generation performance!

### The Markdown Code Fence Trap
LLMs love wrapping JSON in markdown fences:
````
```json
{"user_id": 42}
```
````
In production, your parser must safely extract the inner JSON string before calling `json.loads()`.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Few-Shot Prompting Definition",
                    "prompt": "What differentiates Few-Shot prompting from Zero-Shot prompting?",
                    "hint": "What is included in the prompt text?",
                    "explanation": "Few-shot prompting provides example input-output demonstrations directly inside the prompt context.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "Including 2 or more input-output examples directly in the prompt",
                            "Sending 5 requests simultaneously to the API",
                            "Retraining the model on 10,000 new documents",
                            "Prompting with fewer than 5 words",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "multi",
                    "difficulty": "easy",
                    "title": "Techniques That Boost LLM Accuracy",
                    "prompt": "Which of the following prompt engineering techniques have been proven to improve reasoning and output quality?",
                    "hint": "Think about step-by-step thinking, examples, and role definition.",
                    "explanation": "Chain-of-Thought reasoning, few-shot examples, and clear system instructions significantly boost performance.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Chain-of-Thought prompting ('think step-by-step')",
                            "Providing few-shot input/output examples",
                            "Clearly defining constraints and persona in the system prompt",
                            "Typing in all capital letters with multiple exclamation marks",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Reasoning Prompt Acronym",
                    "prompt": "What 3-letter acronym refers to the 'Chain-of-Thought' prompting methodology?",
                    "hint": "C... T...",
                    "explanation": "CoT stands for Chain of Thought.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. CoT"},
                    "solution": {"regex": True, "accept": [r"^CoT$", r"^COT$", r"^cot$"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Extract JSON from LLM Output",
                    "prompt": "Write `extract_json(raw_text)` that extracts a clean JSON string from LLM responses that may be wrapped in ```` ```json ```` and ```` ``` ```` fences.\n\n- If fences exist, strip ```` ```json ```` and ```` ``` ```` and trim whitespace\n- If no fences exist, return the stripped string\n\n```python\nextract_json('```json\\n{\"a\": 1}\\n```') -> '{\"a\": 1}'\nextract_json('  {\"x\": 2}  ') -> '{\"x\": 2}'\n```",
                    "hint": "Check if text starts with '```json' or '```' and ends with '```', then slice.",
                    "explanation": "Cleaning markdown wrappers is essential for reliable JSON parsing from LLM completions.",
                    "xp": 40,
                    "config": {
                        "language": "python",
                        "starter": "def extract_json(raw_text):\n    # Strip markdown code fences if present and return clean text\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "extract_json",
                        "cases": [
                            {"args": ["```json\n{\"a\": 1}\n```"], "expect": "{\"a\": 1}"},
                            {"args": ["  {\"x\": 2}  "], "expect": "{\"x\": 2}"},
                            {"args": ["```\n[1, 2, 3]\n```"], "expect": "[1, 2, 3]"},
                            {"args": ["{}"], "expect": "{}"},
                            {"args": ["```json\n{\"status\": \"ok\"}\n```\n"], "expect": "{\"status\": \"ok\"}", "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 5: RAG & AI AGENTS
        # =========================================================================
        {
            "index": 5,
            "title": "RAG & Autonomous AI Agents",
            "summary": "Retrieval-Augmented Generation architectures, vector retrieval, ReAct agent loops, and tool execution.",
            "xp_reward": 125,
            "lessons": [
                {
                    "title": "Retrieval-Augmented Generation (RAG) Architecture",
                    "minutes": 7,
                    "body": """Why can't you just paste your entire company handbook into an LLM?
1. **Context Window Limits**: Even 1M token contexts become slow and expensive when querying thousands of pages.
2. **Stale Knowledge**: Pre-trained models know nothing about events or documents created yesterday.

### The 5-Step RAG Pipeline
1. **Chunking**: Split long documents into small paragraphs (e.g. 500 characters with 50-character overlap).
2. **Embedding**: Compute vector embeddings for each chunk and save them in a vector database (`pgvector`, Pinecone, Qdrant).
3. **Retrieval**: When a user asks a question, embed their query and retrieve the top-3 most similar chunks using cosine similarity.
4. **Augmentation**: Inject the retrieved text chunks directly into the prompt context:
   `"Answer using ONLY the following verified context: {chunks}"`
5. **Generation**: The LLM answers factually with zero hallucinations!""",
                },
                {
                    "title": "Autonomous AI Agents: The ReAct Pattern",
                    "minutes": 7,
                    "body": """An **Agent** is an LLM equipped with tools (calculators, web search, database queries, bash execution) and an iterative loop:

### The ReAct (Reason + Act) Loop
1. **Thought**: The model reasons about the goal and decides what information it lacks.
2. **Action**: The model outputs a structured tool call (e.g. `query_database(user_id=42)`).
3. **Observation**: The host system executes the tool and injects the result back into the conversation context.
4. **Repeat**: The model analyzes the observation and either calls another tool or outputs the final answer to the user.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Core Motivation for RAG",
                    "prompt": "What is the primary architectural purpose of Retrieval-Augmented Generation (RAG)?",
                    "hint": "How do we ground an LLM in private, up-to-date data?",
                    "explanation": "RAG retrieves relevant private or fresh external documents and injects them into the prompt to ground the LLM's answer in verified facts.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "To ground the model in verified external or private data without fine-tuning",
                            "To make the model run 10x faster on mobile devices",
                            "To replace Python with C++ in web applications",
                            "To avoid needing an embedding model",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Key Steps of a RAG Pipeline",
                    "prompt": "Which of the following are essential stages in a standard RAG pipeline?",
                    "hint": "Chunking, embedding, retrieving...",
                    "explanation": "Chunking documents, generating vector embeddings, and retrieving relevant context via similarity search are the core steps of RAG.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Chunking long documents into smaller segments",
                            "Generating vector embeddings for chunks and queries",
                            "Retrieving top-k most similar chunks using vector similarity",
                            "Deleting the database on every query",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Reasoning and Acting Pattern",
                    "prompt": "What 5-letter name refers to the agentic paradigm combining Reasoning and Action execution in an iterative loop?",
                    "hint": "Reason + Act = ...",
                    "explanation": "ReAct (Reason + Act) is the standard agent reasoning architecture.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. ReAct"},
                    "solution": {"regex": True, "accept": [r"^ReAct$", r"^react$", r"^REACT$"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Build RAG Augmented Prompt",
                    "prompt": "Write `build_rag_prompt(query, chunks)` that formats an augmented RAG prompt string:\n\nFormat:\n```\nContext:\n- chunk1\n- chunk2\n\nQuestion: {query}\n```\n\nIf `chunks` is empty:\n```\nContext:\n(no context available)\n\nQuestion: {query}\n```\n\n```python\nbuild_rag_prompt(\"What is X?\", [\"X is 10\"]) \n# -> \"Context:\\n- X is 10\\n\\nQuestion: What is X?\"\n```",
                    "hint": "Format chunks with `'- ' + c` joined by newline, or use `'(no context available)'` if empty.",
                    "explanation": "Constructing clean context-injected prompts is the heart of RAG pipeline engineering.",
                    "xp": 45,
                    "config": {
                        "language": "python",
                        "starter": "def build_rag_prompt(query, chunks):\n    # Return formatted RAG prompt string\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "build_rag_prompt",
                        "cases": [
                            {
                                "args": ["What is X?", ["X is 10"]],
                                "expect": "Context:\n- X is 10\n\nQuestion: What is X?",
                            },
                            {
                                "args": ["Where is Paris?", ["Paris is in France.", "Population is 2M."]],
                                "expect": "Context:\n- Paris is in France.\n- Population is 2M.\n\nQuestion: Where is Paris?",
                            },
                            {
                                "args": ["Hello?", []],
                                "expect": "Context:\n(no context available)\n\nQuestion: Hello?",
                            },
                            {
                                "args": ["Query", ["Only one"]],
                                "expect": "Context:\n- Only one\n\nQuestion: Query",
                                "hidden": True,
                            },
                        ],
                    },
                },
            ],
        },
    ],
}
