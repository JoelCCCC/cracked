"use client";

import React, { useState } from "react";
import { VisualizerShell } from "./VisualizerShell";
import { VisualizerStep } from "./types";
import { ArrowRight, Box, Cpu, Database, Layers, Check, AlertCircle } from "lucide-react";

// =========================================================================
// LEVEL 1: VARIABLES & MEMORY BOXES
// =========================================================================
export function VariablesVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Declaration & Assignment",
      description: "Python evaluates the right side `100`, allocates a memory cell in RAM at address 0x7F2A, and binds label 'score' to it.",
      codeSnippet: "score = 100",
    },
    {
      title: "Step 2: String Assignment with Quotes",
      description: "Quotes declare text ('Alex'). Python identifies this as a `str` type and stores it in cell 0x7F2B with label 'player_name'.",
      codeSnippet: "player_name = 'Alex'",
    },
    {
      title: "Step 3: Reassignment & Pointer Update",
      description: "Variables are not permanent boxes! Reassigning `score = score + 25` computes `125` and points 'score' to the new value.",
      codeSnippet: "score = score + 25  # now 125",
    },
    {
      title: "Step 4: Dynamic Typing in Action",
      description: "Python is dynamically typed: `score` can point to a float `125.5` without declaring types upfront.",
      codeSnippet: "score = 125.5  # type is now float",
    },
  ];

  return (
    <VisualizerShell
      title="Variables & Memory in RAM"
      subtitle="How Python binds variable labels to values in computer memory"
      tag="Coding • Level 1"
      accentColor="#7c5cff"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="flex flex-col md:flex-row items-center justify-center gap-8 py-4">
        {/* Left: Variable Name Labels */}
        <div className="space-y-4 w-44">
          <div className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold">
            Variable Labels
          </div>
          
          <div
            className={`p-3 rounded-xl border transition-all duration-300 flex items-center justify-between ${
              step === 0 || step >= 2
                ? "bg-purple-950/60 border-purple-500 shadow-lg shadow-purple-500/20"
                : "bg-slate-900 border-slate-800"
            }`}
          >
            <span className="font-mono text-xs font-bold text-white">score</span>
            <span className="text-[10px] font-mono text-purple-400">
              {step >= 3 ? "float" : "int"}
            </span>
          </div>

          <div
            className={`p-3 rounded-xl border transition-all duration-300 flex items-center justify-between ${
              step >= 1
                ? "bg-cyan-950/60 border-cyan-500 shadow-lg shadow-cyan-500/20"
                : "bg-slate-900/40 border-slate-800 opacity-40"
            }`}
          >
            <span className="font-mono text-xs font-bold text-white">player_name</span>
            <span className="text-[10px] font-mono text-cyan-400">str</span>
          </div>
        </div>

        {/* Center: Glowing Connecting Pointers */}
        <div className="hidden md:flex flex-col justify-around h-28 text-slate-500">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono text-purple-400 animate-pulse">────►</span>
          </div>
          {step >= 1 && (
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono text-cyan-400 animate-pulse">────►</span>
            </div>
          )}
        </div>

        {/* Right: RAM Memory Cells */}
        <div className="space-y-3 w-56">
          <div className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold flex items-center gap-2">
            <Cpu className="w-3.5 h-3.5 text-purple-400" />
            <span>RAM Addresses</span>
          </div>

          <div
            className={`p-3 rounded-xl border transition-all duration-500 ${
              step === 0 || step === 1
                ? "bg-purple-900/40 border-purple-400 shadow-md ring-2 ring-purple-500/30"
                : step >= 2
                ? "bg-slate-900/30 border-slate-800 opacity-40 line-through"
                : "bg-slate-900 border-slate-800"
            }`}
          >
            <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 mb-1">
              <span>0x7F2A</span>
              <span>int</span>
            </div>
            <div className="text-lg font-mono font-black text-white">100</div>
          </div>

          {step >= 2 && (
            <div
              className={`p-3 rounded-xl border transition-all duration-500 animate-in zoom-in-95 ${
                step === 2
                  ? "bg-emerald-950/60 border-emerald-400 shadow-md ring-2 ring-emerald-500/30"
                  : "bg-purple-900/40 border-purple-400"
              }`}
            >
              <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 mb-1">
                <span>0x7F2C</span>
                <span>{step === 3 ? "float" : "int"}</span>
              </div>
              <div className="text-lg font-mono font-black text-emerald-300">
                {step === 3 ? "125.5" : "125"}
              </div>
            </div>
          )}

          {step >= 1 && (
            <div className="p-3 rounded-xl border bg-cyan-950/40 border-cyan-500 shadow-md ring-2 ring-cyan-500/20">
              <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 mb-1">
                <span>0x7F2B</span>
                <span>str</span>
              </div>
              <div className="text-lg font-mono font-black text-cyan-300">&quot;Alex&quot;</div>
            </div>
          )}
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 2: CONDITIONALS & LOGIC FORKS
// =========================================================================
export function ConditionalsVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Input Value Arrives",
      description: "We are testing `score = 85` through a conditional grading branch.",
      codeSnippet: "score = 85",
    },
    {
      title: "Step 2: First Condition (if score >= 90)",
      description: "Python evaluates `85 >= 90`. Result is FALSE. The block is skipped completely.",
      codeSnippet: "if score >= 90:  # FALSE (85 < 90)",
    },
    {
      title: "Step 3: Second Condition (elif score >= 80)",
      description: "Python evaluates `85 >= 80`. Result is TRUE! Python enters this branch immediately.",
      codeSnippet: "elif score >= 80:  # TRUE -> return 'B'",
    },
    {
      title: "Step 4: Short-Circuiting & Exit",
      description: "Once a matching branch executes, Python skips all remaining `elif` and `else` branches!",
      codeSnippet: "grade = 'B' (Done)",
    },
  ];

  return (
    <VisualizerShell
      title="Conditional Execution Branches"
      subtitle="How Python branches logic and skips unmatched branches"
      tag="Coding • Level 2"
      accentColor="#7c5cff"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-3 py-2">
        {/* Input box */}
        <div className="flex items-center justify-center gap-3 p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-white">
          <span className="text-slate-400">Input:</span>
          <span className="px-2 py-0.5 rounded bg-purple-900/60 text-purple-300 font-bold">score = 85</span>
        </div>

        {/* Branch 1 */}
        <div
          className={`p-3 rounded-xl border transition-all duration-300 flex items-center justify-between ${
            step >= 1
              ? "bg-red-950/40 border-red-500/60 opacity-60"
              : "bg-slate-900/60 border-slate-800"
          }`}
        >
          <div className="font-mono text-xs text-slate-300">if score &gt;= 90:</div>
          <div className="text-xs font-bold">
            {step >= 1 ? (
              <span className="text-red-400 flex items-center gap-1 font-mono text-[11px]">
                <AlertCircle className="w-3.5 h-3.5" /> False (Skip)
              </span>
            ) : (
              <span className="text-slate-500 text-[11px] font-mono">Pending</span>
            )}
          </div>
        </div>

        {/* Branch 2 (Match) */}
        <div
          className={`p-3 rounded-xl border transition-all duration-300 flex items-center justify-between ${
            step >= 2
              ? "bg-emerald-950/70 border-emerald-400 ring-2 ring-emerald-500/30 shadow-lg shadow-emerald-500/20"
              : "bg-slate-900/60 border-slate-800"
          }`}
        >
          <div className="font-mono text-xs text-white">elif score &gt;= 80:</div>
          <div className="text-xs font-bold">
            {step >= 2 ? (
              <span className="text-emerald-400 flex items-center gap-1 font-mono text-[11px]">
                <Check className="w-3.5 h-3.5" /> True (Enter Branch: &apos;B&apos;)
              </span>
            ) : (
              <span className="text-slate-500 text-[11px] font-mono">Pending</span>
            )}
          </div>
        </div>

        {/* Branch 3 (Skipped due to short circuit) */}
        <div
          className={`p-3 rounded-xl border transition-all duration-300 flex items-center justify-between ${
            step >= 3
              ? "bg-slate-950 border-slate-800 opacity-40 line-through"
              : "bg-slate-900/60 border-slate-800"
          }`}
        >
          <div className="font-mono text-xs text-slate-400">else:</div>
          <div className="text-[11px] font-mono text-slate-500">
            {step >= 3 ? "Skipped" : "Pending"}
          </div>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 3: LOOPS & ACCUMULATOR MACHINE
// =========================================================================
export function LoopsVisualizer() {
  const [step, setStep] = useState(0);
  const items = [10, 20, 30, 40];
  const accumulated = [0, 10, 30, 60, 100];

  const steps: VisualizerStep[] = [
    {
      title: "Step 0: Initialize Accumulator",
      description: "Before loop starts, accumulator `total = 0`. List has 4 numbers: [10, 20, 30, 40].",
      codeSnippet: "total = 0",
    },
    {
      title: "Step 1: First Iteration (x = 10)",
      description: "Loop picks item 0 (10). Adds to total: total = 0 + 10 = 10.",
      codeSnippet: "total += 10  # total is 10",
    },
    {
      title: "Step 2: Second Iteration (x = 20)",
      description: "Loop advances to item 1 (20). Adds to total: total = 10 + 20 = 30.",
      codeSnippet: "total += 20  # total is 30",
    },
    {
      title: "Step 3: Third Iteration (x = 30)",
      description: "Loop advances to item 2 (30). Adds to total: total = 30 + 30 = 60.",
      codeSnippet: "total += 30  # total is 60",
    },
    {
      title: "Step 4: Final Iteration & Loop Exit",
      description: "Loop finishes last item (40). total = 60 + 40 = 100. Loop terminates cleanly!",
      codeSnippet: "total += 40  # final sum is 100",
    },
  ];

  return (
    <VisualizerShell
      title="The Loop Conveyor & Accumulator Pattern"
      subtitle="How Python processes items one-by-one and aggregates results"
      tag="Coding • Level 3"
      accentColor="#7c5cff"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="space-y-6 max-w-lg mx-auto py-2">
        {/* List Conveyor Belt */}
        <div>
          <div className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold mb-2">
            Input List: items = [10, 20, 30, 40]
          </div>
          <div className="grid grid-cols-4 gap-2">
            {items.map((val, idx) => {
              const isCurrent = step === idx + 1;
              const isDone = step > idx + 1;
              return (
                <div
                  key={idx}
                  className={`p-3 rounded-xl border text-center transition-all duration-300 ${
                    isCurrent
                      ? "bg-purple-950/80 border-purple-400 ring-2 ring-purple-500/50 scale-105 shadow-lg shadow-purple-500/30"
                      : isDone
                      ? "bg-slate-900/40 border-slate-800 opacity-50"
                      : "bg-slate-900 border-slate-800"
                  }`}
                >
                  <div className="text-[10px] font-mono text-slate-500 mb-1">
                    Index {idx}
                  </div>
                  <div className="text-base font-mono font-bold text-white">
                    {val}
                  </div>
                  {isCurrent && (
                    <span className="inline-block mt-1 px-1.5 py-0.5 rounded text-[9px] font-mono bg-purple-500 text-white font-bold animate-pulse">
                      Active
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Accumulator Register */}
        <div className="flex items-center justify-between p-4 rounded-xl bg-gradient-to-r from-slate-900 via-purple-950/30 to-slate-900 border border-purple-500/30 shadow-lg">
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-purple-400 font-bold">
              Accumulator Register
            </span>
            <div className="text-xs text-slate-300 font-mono mt-0.5">
              total = {step > 0 ? `${accumulated[step - 1]} + ${items[step - 1]}` : "0"}
            </div>
          </div>
          <div className="text-3xl font-mono font-black text-cyan-400">
            {accumulated[step]}
          </div>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 4: COLLECTIONS & HASH TABLES
// =========================================================================
export function CollectionsVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: List with 0-Based Indices",
      description: "Lists are contiguous memory cells indexed from 0. Accessing `fruits[0]` jumps to index 0 instantly.",
      codeSnippet: "fruits = ['apple', 'banana', 'cherry']",
    },
    {
      title: "Step 2: Slice Notation [start:stop]",
      description: "`fruits[1:3]` extracts a sublist from index 1 up to (but not including) index 3: ['banana', 'cherry'].",
      codeSnippet: "fruits[1:3]  # ['banana', 'cherry']",
    },
    {
      title: "Step 3: Hash Table (Dictionary / Set) Lookups",
      description: "Instead of scanning like a list, Python hashes key 'apple' -> bucket #2. Instant O(1) direct lookup!",
      codeSnippet: "prices['apple']  # O(1) hash bucket",
    },
  ];

  return (
    <VisualizerShell
      title="Collections: Lists vs Hash Maps"
      subtitle="Contiguous array indexing vs instant O(1) hash table buckets"
      tag="Coding • Level 4"
      accentColor="#7c5cff"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="space-y-5 max-w-lg mx-auto py-2">
        {/* List representation */}
        <div>
          <div className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold mb-2">
            Contiguous List: fruits
          </div>
          <div className="grid grid-cols-3 gap-2">
            {["apple", "banana", "cherry"].map((fruit, idx) => {
              const isSlice = step === 1 && (idx === 1 || idx === 2);
              const isFirst = step === 0 && idx === 0;
              return (
                <div
                  key={idx}
                  className={`p-3 rounded-xl border text-center transition-all duration-300 ${
                    isSlice
                      ? "bg-cyan-950/70 border-cyan-400 shadow-lg shadow-cyan-500/20 scale-105"
                      : isFirst
                      ? "bg-purple-950/70 border-purple-400 shadow-lg shadow-purple-500/20"
                      : "bg-slate-900 border-slate-800"
                  }`}
                >
                  <div className="text-[10px] font-mono text-slate-500 mb-0.5">
                    [{idx}]
                  </div>
                  <div className="text-sm font-mono font-bold text-white">
                    &quot;{fruit}&quot;
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Hash Table Bucket */}
        {step === 2 && (
          <div className="p-4 rounded-xl bg-slate-900/90 border border-purple-500/40 animate-in zoom-in-95">
            <div className="text-[11px] font-mono uppercase tracking-wider text-purple-400 font-bold mb-2">
              Hash Map (Dictionary Buckets)
            </div>
            <div className="flex items-center gap-2 font-mono text-xs text-slate-300 bg-slate-950 p-2 rounded-lg border border-slate-800">
              <span className="text-cyan-400 font-bold">hash(&apos;apple&apos;) % 4</span>
              <span>──►</span>
              <span className="bg-purple-600 px-2 py-0.5 rounded text-white font-bold">
                Bucket #2: $1.50
              </span>
              <span className="ml-auto text-[10px] text-emerald-400 font-bold">O(1)</span>
            </div>
          </div>
        )}
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 5: FUNCTIONS & CALL STACK
// =========================================================================
export function FunctionsVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Main Program Frame",
      description: "Python starts executing. The base `__main__` frame is pushed onto the Call Stack.",
      codeSnippet: "def main(): calculate(10)",
    },
    {
      title: "Step 2: Function Call (Push Stack Frame)",
      description: "Calling `calculate(10)` creates a new isolated stack frame with its own local variables.",
      codeSnippet: "calculate(x=10)  # Pushed to stack",
    },
    {
      title: "Step 3: Nested Function Call (Double Push)",
      description: "Inside `calculate`, `double(10)` is called. Another stack frame is pushed on top!",
      codeSnippet: "double(n=10) -> returns 20",
    },
    {
      title: "Step 4: Return & Pop Frame",
      description: "Function finishes and returns 20. Its frame is popped off the stack and memory is freed!",
      codeSnippet: "return 20  # Frame popped",
    },
  ];

  return (
    <VisualizerShell
      title="Function Execution & The Call Stack"
      subtitle="How Python tracks nested function calls and local variables"
      tag="Coding • Level 5"
      accentColor="#7c5cff"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-xs mx-auto space-y-2 py-2">
        <div className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold text-center mb-3">
          Call Stack (LIFO: Last In, First Out)
        </div>

        {/* Top of Stack */}
        {step === 2 && (
          <div className="p-3 rounded-xl bg-purple-950/80 border border-purple-400 text-center font-mono text-xs shadow-lg shadow-purple-500/30 animate-in slide-in-from-top-3">
            <span className="text-purple-300 font-bold">double(n=10)</span>
            <div className="text-[10px] text-slate-400 mt-0.5">Top Frame (Active)</div>
          </div>
        )}

        {step >= 1 && step !== 3 && (
          <div className="p-3 rounded-xl bg-cyan-950/80 border border-cyan-400 text-center font-mono text-xs shadow-lg shadow-cyan-500/20">
            <span className="text-cyan-300 font-bold">calculate(x=10)</span>
            <div className="text-[10px] text-slate-400 mt-0.5">Local scope: x = 10</div>
          </div>
        )}

        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center font-mono text-xs">
          <span className="text-slate-200 font-bold">__main__</span>
          <div className="text-[10px] text-slate-500 mt-0.5">Global Program Scope</div>
        </div>
      </div>
    </VisualizerShell>
  );
}
