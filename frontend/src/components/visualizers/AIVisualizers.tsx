"use client";

import React, { useState } from "react";
import { VisualizerShell } from "./VisualizerShell";
import { VisualizerStep } from "./types";
import { Brain, Cpu, Search, Sparkles, MessageSquare, Database, Check } from "lucide-react";

// =========================================================================
// LEVEL 1: NEURAL NETWORK FORWARD PASS & LOSS
// =========================================================================
export function NeuralNetVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Input Vector (X)",
      description: "Inputs $x_1 = 0.5$ and $x_2 = 0.8$ are fed into the input layer nodes.",
      codeSnippet: "X = [0.5, 0.8]",
    },
    {
      title: "Step 2: Weighted Sum (W · X + b)",
      description: "Each input is multiplied by its connection weight $w$ and summed with bias $b$.",
      codeSnippet: "z = w1*x1 + w2*x2 + b",
    },
    {
      title: "Step 3: Non-Linear Activation (ReLU / Sigmoid)",
      description: "Activation function introduces non-linearity, mapping values to output prediction $\\hat{y} = 0.88$.",
      codeSnippet: "y_hat = sigmoid(z) -> 0.88",
    },
    {
      title: "Step 4: Loss Calculation & Gradient Update",
      description: "Compares prediction (0.88) with true label (1.0). Loss = 0.12. Gradients adjust weights backwards!",
      codeSnippet: "Loss = 0.12 (Backprop gradient update)",
    },
  ];

  return (
    <VisualizerShell
      title="Neural Network Forward Pass & Loss"
      subtitle="How inputs pass through weights and activations to compute loss"
      tag="AI • Level 1"
      accentColor="#b37feb"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="flex items-center justify-around max-w-md mx-auto py-2 font-mono text-xs">
        {/* Input layer */}
        <div className="space-y-3 text-center">
          <div className="p-2.5 rounded-xl bg-purple-950 border border-purple-500 text-purple-300 font-bold">
            x₁: 0.5
          </div>
          <div className="p-2.5 rounded-xl bg-purple-950 border border-purple-500 text-purple-300 font-bold">
            x₂: 0.8
          </div>
        </div>

        {/* Weights & Hidden Neuron */}
        <div className="flex flex-col items-center">
          <span className="text-[10px] text-slate-500 mb-1">w₁=0.4, w₂=0.7</span>
          <div className={`w-16 h-16 rounded-2xl border flex items-center justify-center font-bold text-sm transition-all ${
            step >= 1 ? "bg-cyan-950/80 border-cyan-400 text-cyan-300 ring-2 ring-cyan-500/40 shadow-lg" : "bg-slate-900 border-slate-800 text-slate-500"
          }`}>
            <Cpu className="w-6 h-6" />
          </div>
          <span className="text-[10px] text-slate-500 mt-1">Σ(W·X) + b</span>
        </div>

        {/* Output */}
        <div className="text-center">
          <div className={`p-3 rounded-xl border font-bold transition-all ${
            step >= 2 ? "bg-emerald-950/80 border-emerald-400 text-emerald-300 ring-2 ring-emerald-500/40 shadow-lg" : "bg-slate-900 border-slate-800 text-slate-500"
          }`}>
            ŷ = {step >= 2 ? "0.88" : "?"}
          </div>
          {step === 3 && (
            <span className="text-[10px] text-amber-400 font-bold mt-1 block">
              Loss: 0.12 (Backprop)
            </span>
          )}
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 2: VECTOR EMBEDDING SPACE & COSINE SIMILARITY
// =========================================================================
export function EmbeddingVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Text to Dense Vector",
      description: "Words 'puppy' and 'dog' are converted into high-dimensional vectors by the embedding model.",
      codeSnippet: "embed('puppy') -> [0.82, 0.79, ...]",
    },
    {
      title: "Step 2: Semantic Angle θ in Space",
      description: "'puppy' and 'dog' point in almost the exact same direction (angle θ = 4°). 'apple' points in an unrelated direction.",
      codeSnippet: "cos(θ) between 'dog' & 'puppy' ≈ 0.98",
    },
    {
      title: "Step 3: Vector Semantic Retrieval",
      description: "Cosine similarity ranks 'puppy' as the top semantic match for query 'canine', even with 0 shared keywords!",
      codeSnippet: "Top match: 'puppy' (score: 0.98)",
    },
  ];

  return (
    <VisualizerShell
      title="Vector Embeddings & Cosine Similarity"
      subtitle="How geometric angles between vectors capture semantic meaning"
      tag="AI • Level 2"
      accentColor="#b37feb"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-3 py-2 font-mono text-xs">
        <div className="text-[11px] text-slate-400 text-center mb-1">
          Query: <span className="text-cyan-400 font-bold">&quot;canine pet&quot;</span>
        </div>

        {/* Dog */}
        <div className={`p-3 rounded-xl border flex items-center justify-between transition-all ${
          step >= 1 ? "bg-emerald-950/70 border-emerald-400 text-white ring-2 ring-emerald-500/40 shadow-lg" : "bg-slate-900 border-slate-800 text-slate-400"
        }`}>
          <div>
            <span className="font-bold text-emerald-300">&quot;puppy&quot;</span>
            <div className="text-[10px] text-slate-400">Vector: [0.82, 0.79, 0.11]</div>
          </div>
          <div className="text-sm font-bold text-emerald-400">Cosine: 0.98 (Match!)</div>
        </div>

        {/* Dog */}
        <div className={`p-3 rounded-xl border flex items-center justify-between transition-all ${
          step >= 1 ? "bg-emerald-950/40 border-emerald-500/50 text-white" : "bg-slate-900 border-slate-800 text-slate-400"
        }`}>
          <div>
            <span className="font-bold text-emerald-300">&quot;dog&quot;</span>
            <div className="text-[10px] text-slate-400">Vector: [0.80, 0.77, 0.15]</div>
          </div>
          <div className="text-sm font-bold text-emerald-400">Cosine: 0.96</div>
        </div>

        {/* Apple */}
        <div className="p-3 rounded-xl border bg-slate-900/40 border-slate-800/80 opacity-50 flex items-center justify-between text-slate-500">
          <div>
            <span>&quot;apple fruit&quot;</span>
            <div className="text-[10px]">Vector: [-0.60, 0.12, 0.88]</div>
          </div>
          <div className="text-sm">Cosine: 0.08 (Unrelated)</div>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 3: AUTOREGRESSIVE TOKEN GENERATION
// =========================================================================
export function AutoregressiveVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Input Tokens Processed",
      description: "Prompt tokens: ['The', 'capital', 'of', 'France', 'is']. Passed through transformer self-attention blocks.",
      codeSnippet: "tokens = [464, 3124, 286, 4881, 318]",
    },
    {
      title: "Step 2: Probability Distribution Computed",
      description: "Model predicts next token logits over its 100,000 token vocabulary: 'Paris' 92.4%, 'a' 3.1%, 'not' 0.8%.",
      codeSnippet: "softmax(logits / T)",
    },
    {
      title: "Step 3: Token Sampled & Appended",
      description: "'Paris' is chosen. Appended to prompt: 'The capital of France is Paris'. Cycle repeats for next token!",
      codeSnippet: "prompt += ' Paris' (Autoregressive Loop)",
    },
  ];

  return (
    <VisualizerShell
      title="Autoregressive Next-Token Prediction"
      subtitle="How LLMs predict probability distributions and generate text token-by-token"
      tag="AI • Level 3"
      accentColor="#b37feb"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-4 py-2 font-mono text-xs">
        {/* Token sequence */}
        <div className="flex items-center gap-1.5 flex-wrap p-3 rounded-xl bg-slate-900 border border-slate-800">
          {["The", "capital", "of", "France", "is"].map((token, i) => (
            <span key={i} className="px-2 py-1 rounded bg-slate-800 text-slate-200">
              {token}
            </span>
          ))}
          {step === 2 && (
            <span className="px-2 py-1 rounded bg-purple-600 text-white font-bold ring-2 ring-purple-400 animate-pulse">
              Paris
            </span>
          )}
        </div>

        {/* Probabilities bar chart */}
        <div className="space-y-1.5 p-3 rounded-xl bg-slate-950 border border-slate-800">
          <div className="text-[10px] uppercase font-bold text-slate-400 mb-2">
            Next Token Probability Distribution
          </div>
          
          <div className="space-y-1">
            <div className="flex items-center justify-between text-[11px]">
              <span className="text-purple-300 font-bold">&quot;Paris&quot;</span>
              <span className="text-purple-400 font-bold">92.4%</span>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div className="bg-gradient-to-r from-purple-500 to-cyan-400 h-full w-[92.4%]" />
            </div>
          </div>

          <div className="space-y-1 pt-1">
            <div className="flex items-center justify-between text-[11px] text-slate-500">
              <span>&quot;a&quot;</span>
              <span>3.1%</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
              <div className="bg-slate-600 h-full w-[3.1%]" />
            </div>
          </div>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 4: CHAIN-OF-THOUGHT REASONING
// =========================================================================
export function ChainOfThoughtVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Direct Prompting (High Error Rate)",
      description: "Prompt: 'If John has 5 apples and eats 2, then gets 3 boxes of 4, how many apples does he have?'",
      codeSnippet: "Direct output: '14' (Often hallucinated without scratchpad)",
    },
    {
      title: "Chain-of-Thought (Step 1: Unfold Reasoning)",
      description: "Instruct model: 'Think step-by-step.' Model generates token scratchpad: '5 - 2 = 3 remaining apples.'",
      codeSnippet: "Thought: 5 - 2 = 3 apples",
    },
    {
      title: "Chain-of-Thought (Step 2: Sub-Computation)",
      description: "Model computes next intermediate tokens: '3 boxes of 4 = 12 apples.'",
      codeSnippet: "Thought: 3 * 4 = 12 apples",
    },
    {
      title: "Chain-of-Thought (Step 3: Final Verified Answer)",
      description: "Total = 3 + 12 = 15 apples. Guaranteed mathematically correct answer!",
      codeSnippet: "Final Answer: 15 apples (100% verified)",
    },
  ];

  return (
    <VisualizerShell
      title="Chain-of-Thought (CoT) Reasoning"
      subtitle="How generating intermediate reasoning tokens unlocks complex logic and math"
      tag="AI • Level 4"
      accentColor="#b37feb"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-3 py-2 font-mono text-xs">
        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-slate-300">
          <span className="text-[10px] text-slate-500 uppercase font-bold block mb-1">Problem</span>
          5 apples - 2 eaten + 3 boxes of 4 = ?
        </div>

        {step === 0 ? (
          <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-500">
            Direct answer without scratchpad often fails on multi-step reasoning.
          </div>
        ) : (
          <div className="p-3.5 rounded-xl bg-purple-950/60 border border-purple-500/60 shadow-lg space-y-1.5 text-purple-200">
            <span className="text-[10px] text-purple-400 uppercase font-bold block mb-1">
              CoT Reasoning Scratchpad Tokens
            </span>
            <div>1. 5 - 2 = 3 apples left</div>
            {step >= 2 && <div>2. 3 boxes * 4 = 12 new apples</div>}
            {step >= 3 && (
              <div className="text-emerald-300 font-bold pt-1 border-t border-purple-800/60 flex items-center gap-1">
                <Check className="w-3.5 h-3.5" /> 3 + 12 = 15 apples (Correct!)
              </div>
            )}
          </div>
        )}
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 5: RAG PIPELINE VISUALIZER
// =========================================================================
export function RagVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: User Query Arrives",
      description: "User asks: 'What is our company refund window?' Raw LLM does not have this private data.",
      codeSnippet: "query = 'What is our refund window?'",
    },
    {
      title: "Step 2: Vector Search on Vector DB",
      description: "Query is embedded. Searches pgvector database with cosine similarity to find top matching chunks.",
      codeSnippet: "pgvector: SELECT * ORDER BY embedding <=> query_vec LIMIT 2",
    },
    {
      title: "Step 3: Prompt Augmentation with Context",
      description: "Retrieved chunk ('Refunds are granted within 30 days of purchase') is injected into the prompt!",
      codeSnippet: "Prompt: Context: {chunk} -> Answer question.",
    },
    {
      title: "Step 4: Grounded, Hallucination-Free Answer",
      description: "LLM reads verified context: 'Your refund window is 30 days.' 100% grounded in company facts!",
      codeSnippet: "Response: 'Refunds are available within 30 days.'",
    },
  ];

  return (
    <VisualizerShell
      title="Retrieval-Augmented Generation (RAG)"
      subtitle="How vector search grounds LLM answers in verified private data"
      tag="AI • Level 5"
      accentColor="#b37feb"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="flex items-center justify-between max-w-lg mx-auto py-2 font-mono text-xs gap-3">
        {/* User Query */}
        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center flex-1">
          <MessageSquare className="w-5 h-5 text-cyan-400 mx-auto mb-1" />
          <div className="font-bold text-white">User Query</div>
          <span className="text-[10px] text-slate-500">&quot;Refund policy?&quot;</span>
        </div>

        {/* Vector DB */}
        <div className={`p-3 rounded-xl border text-center flex-1 transition-all ${
          step >= 1 ? "bg-purple-950/80 border-purple-400 text-purple-200 ring-2 ring-purple-500/40 shadow-lg" : "bg-slate-900 border-slate-800 text-slate-500"
        }`}>
          <Database className="w-5 h-5 text-purple-400 mx-auto mb-1" />
          <div className="font-bold text-white">Vector DB</div>
          <span className="text-[10px] text-purple-300">Chunk: &quot;30 days&quot;</span>
        </div>

        {/* LLM Generation */}
        <div className={`p-3 rounded-xl border text-center flex-1 transition-all ${
          step >= 3 ? "bg-emerald-950/80 border-emerald-400 text-emerald-200 ring-2 ring-emerald-500/40 shadow-lg" : "bg-slate-900 border-slate-800 text-slate-500"
        }`}>
          <Sparkles className="w-5 h-5 text-emerald-400 mx-auto mb-1" />
          <div className="font-bold text-white">Grounded LLM</div>
          <span className="text-[10px] text-emerald-300">100% Fact Verified</span>
        </div>
      </div>
    </VisualizerShell>
  );
}
