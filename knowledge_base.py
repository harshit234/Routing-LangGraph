"""
Parishiksha Course Knowledge Base
Simulated vector store with week-by-week AI/ML course notes.
"""

COURSE_NOTES = {
    1: {
        "title": "Introduction to AI & Random Prediction",
        "topics": ["What is AI?", "History of AI", "Random Prediction", "Baseline Models"],
        "content": (
            "Week 1: Introduction to AI & Random Prediction\n\n"
            "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. "
            "The field was formally founded at the Dartmouth Conference in 1956.\n\n"
            "Random Prediction serves as a baseline model. For binary classification, random prediction "
            "yields ~50% accuracy. For k classes, it yields ~1/k accuracy. This baseline helps us "
            "understand if our models are actually learning meaningful patterns.\n\n"
            "Key evaluation metrics: Accuracy = (TP+TN)/Total, Precision = TP/(TP+FP), "
            "Recall = TP/(TP+FN), F1 = harmonic mean of Precision and Recall.\n\n"
            "We also discussed supervised, unsupervised, and reinforcement learning paradigms."
        ),
    },
    2: {
        "title": "Linear Models & Regression",
        "topics": ["Linear Regression", "Gradient Descent", "Loss Functions", "Regularization"],
        "content": (
            "Week 2: Linear Models & Regression\n\n"
            "Linear Regression: y = wX + b. Gradient Descent minimizes loss iteratively.\n\n"
            "Variants: Batch GD (full dataset), SGD (one sample), Mini-batch GD (32-256 samples).\n\n"
            "MSE Loss: L = (1/n) * sum((y_pred - y_true)^2).\n\n"
            "Regularization prevents overfitting: L1 (Lasso) promotes sparsity, "
            "L2 (Ridge) prevents large weights, Dropout zeroes random neurons during training."
        ),
    },
    3: {
        "title": "Neural Networks Fundamentals",
        "topics": ["Perceptron", "MLP", "Activation Functions", "Backpropagation"],
        "content": (
            "Week 3: Neural Networks Fundamentals\n\n"
            "Perceptron (Rosenblatt, 1958): output = activation(w*x + b). Only learns linearly separable functions.\n\n"
            "Multi-Layer Perceptrons (MLPs) stack layers with non-linear activations.\n\n"
            "Activation Functions: Sigmoid (0,1), ReLU max(0,x), Tanh (-1,1), Softmax (probabilities).\n\n"
            "Backpropagation computes gradients via the chain rule. "
            "Universal Approximation Theorem: one hidden layer can approximate any continuous function."
        ),
    },
    4: {
        "title": "Convolutional Neural Networks",
        "topics": ["Convolution", "Pooling", "CNN Architectures", "Transfer Learning"],
        "content": (
            "Week 4: Convolutional Neural Networks (CNNs)\n\n"
            "CNNs are specialized for grid-like data. Convolution slides a kernel across input "
            "to produce feature maps. Pooling reduces spatial dimensions.\n\n"
            "Notable architectures: LeNet-5 (1998), AlexNet (2012), VGG (2014), ResNet (2015).\n\n"
            "Transfer Learning uses pre-trained ImageNet models as feature extractors for new tasks."
        ),
    },
    5: {
        "title": "Recurrent Neural Networks",
        "topics": ["Sequence Modeling", "LSTM", "GRU", "Bidirectional RNNs"],
        "content": (
            "Week 5: Recurrent Neural Networks (RNNs)\n\n"
            "RNNs process sequences via hidden state: h_t = f(W_hh*h_{t-1} + W_xh*x_t + b).\n\n"
            "Vanishing Gradient Problem: gradients shrink over long sequences.\n\n"
            "LSTM solves this with forget, input, and output gates. "
            "GRU is a simplified variant with reset and update gates.\n\n"
            "Bidirectional RNNs process sequences in both directions for richer context."
        ),
    },
    6: {
        "title": "Word Embeddings & NLP",
        "topics": ["Word2Vec", "GloVe", "Tokenization", "Language Modeling"],
        "content": (
            "Week 6: Word Embeddings & NLP Foundations\n\n"
            "Word2Vec (Mikolov, 2013): CBOW predicts target from context, Skip-gram predicts context from target. "
            "Famous property: king - man + woman = queen.\n\n"
            "GloVe combines co-occurrence statistics with prediction.\n\n"
            "Tokenization: word-level, subword (BPE), character-level.\n\n"
            "Language Modeling predicts P(w_t | w_1..w_{t-1}). Perplexity measures quality."
        ),
    },
    7: {
        "title": "Sequence-to-Sequence Models",
        "topics": ["Encoder-Decoder", "Machine Translation", "Beam Search", "BLEU Score"],
        "content": (
            "Week 7: Sequence-to-Sequence Models\n\n"
            "Seq2Seq (Sutskever, 2014): Encoder compresses input into context vector, "
            "Decoder generates output from it.\n\n"
            "Bottleneck: single vector loses info for long sequences.\n\n"
            "Beam Search maintains top-k candidates instead of greedy decoding.\n\n"
            "BLEU Score measures translation quality via n-gram overlap (0 to 1)."
        ),
    },
    8: {
        "title": "Attention Mechanisms",
        "topics": ["Bahdanau Attention", "Self-Attention", "Multi-Head Attention", "Positional Encoding"],
        "content": (
            "Week 8: Attention Mechanisms\n\n"
            "Attention lets the decoder look at ALL encoder states, solving the bottleneck.\n\n"
            "Bahdanau (2015): Additive attention with alignment scores.\n"
            "Luong (2015): Multiplicative attention, simpler and faster.\n\n"
            "Self-Attention: each token attends to all others in O(1) steps vs O(n) for RNNs.\n\n"
            "Multi-Head Attention runs multiple attention computations in parallel. "
            "Each head learns different relationship patterns.\n\n"
            "Positional Encoding adds position info since attention is permutation-invariant: "
            "PE(pos,2i) = sin(pos/10000^(2i/d))."
        ),
    },
    9: {
        "title": "Transformers & BERT",
        "topics": ["Transformer Architecture", "BERT", "GPT", "Pre-training", "Fine-tuning"],
        "content": (
            "Week 9: Transformers & BERT\n\n"
            "Transformer (Vaswani, 2017) - 'Attention Is All You Need': "
            "Encoder (6 layers of MHA + FFN), Decoder (6 layers of Masked MHA + Cross-Attention + FFN).\n\n"
            "BERT (Devlin, 2019): Bidirectional encoder, pre-trained on MLM + NSP. "
            "BERT-base: 12 layers, 110M params. Fine-tune by adding task-specific heads.\n\n"
            "GPT: Decoder-only, autoregressive. GPT-2: 1.5B params, GPT-3: 175B params. "
            "Enables in-context learning with few-shot prompting."
        ),
    },
    10: {
        "title": "Agentic AI & LLM Applications",
        "topics": ["LLM Agents", "RAG", "Tool Use", "Chain-of-Thought", "Multi-Agent Systems"],
        "content": (
            "Week 10: Agentic AI & LLM Applications\n\n"
            "Agentic AI: systems that autonomously plan, execute, and verify tasks.\n\n"
            "Components: Planning (ReAct, Plan-and-Execute), Memory (context window + vector stores), "
            "Tool Use (function calling, web search), Reflection (self-critique).\n\n"
            "RAG: Retrieve relevant docs, augment prompt with context, generate grounded answers. "
            "Reduces hallucination.\n\n"
            "Chain-of-Thought: 'Let's think step by step' for better reasoning.\n\n"
            "Multi-Agent Systems: specialized agents collaborating via routers and orchestrators. "
            "LangGraph enables stateful, multi-actor applications with conditional routing."
        ),
    },
}


def get_notes_for_week(week: int) -> str | None:
    """Get notes for a specific week."""
    if week in COURSE_NOTES:
        return COURSE_NOTES[week]["content"]
    return None


def get_all_notes() -> str:
    """Get all course notes concatenated."""
    return "\n\n---\n\n".join(n["content"] for n in COURSE_NOTES.values())


def get_available_weeks() -> list[dict]:
    """Get list of available week numbers and titles."""
    return [
        {"week": w, "title": d["title"], "topics": d["topics"]}
        for w, d in COURSE_NOTES.items()
    ]
