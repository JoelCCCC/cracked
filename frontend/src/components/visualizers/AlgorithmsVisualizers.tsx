"use client";

import React, { useState } from "react";
import { VisualizerShell } from "./VisualizerShell";
import { VisualizerStep } from "./types";
import { ChevronDown, ArrowDown, Check, X, ShieldAlert } from "lucide-react";

// =========================================================================
// LEVEL 1: BIG-O COMPLEXITY COMPARISON
// =========================================================================
export function BigOVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: O(1) Constant Time",
      description: "Hash map lookups or array indexing: takes the exact same 1 operation whether n = 10 or n = 1,000,000.",
      codeSnippet: "dict[key]  # O(1)",
    },
    {
      title: "Step 2: O(log n) Logarithmic Time",
      description: "Binary search: halving the space on each step. On 1,000,000 items, takes only ~20 steps!",
      codeSnippet: "binary_search(nums, target)  # O(log n)",
    },
    {
      title: "Step 3: O(n) Linear Time",
      description: "Single for loop scanning items: operations scale 1:1 directly with input size.",
      codeSnippet: "for item in items:  # O(n)",
    },
    {
      title: "Step 4: O(n²) Quadratic Time (Danger Zone!)",
      description: "Nested loops comparing each item to all others: on 1,000,000 items, requires 1,000,000,000,000 operations!",
      codeSnippet: "for i in n: for j in n:  # O(n^2)",
    },
  ];

  return (
    <VisualizerShell
      title="Big-O Complexity Operations Growth"
      subtitle="How execution steps scale as dataset size n expands"
      tag="Algorithms • Level 1"
      accentColor="#22c1a4"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-3 py-2">
        <div className="text-[11px] font-mono text-slate-400 text-center mb-1">
          Steps required on input size: <span className="text-white font-bold font-mono">n = 1,000,000</span>
        </div>

        {/* O(1) */}
        <div
          className={`p-3 rounded-xl border transition-all duration-300 flex items-center justify-between ${
            step === 0
              ? "bg-emerald-950/80 border-emerald-400 shadow-lg shadow-emerald-500/20 ring-2 ring-emerald-500/30 scale-102"
              : "bg-slate-900 border-slate-800 opacity-60"
          }`}
        >
          <div>
            <span className="font-mono text-xs font-black text-emerald-300">O(1) Constant</span>
            <div className="text-[10px] text-slate-400">Instant lookup</div>
          </div>
          <div className="text-sm font-mono font-bold text-white">1 step</div>
        </div>

        {/* O(log n) */}
        <div
          className={`p-3 rounded-xl border transition-all duration-300 flex items-center justify-between ${
            step === 1
              ? "bg-cyan-950/80 border-cyan-400 shadow-lg shadow-cyan-500/20 ring-2 ring-cyan-500/30 scale-102"
              : "bg-slate-900 border-slate-800 opacity-60"
          }`}
        >
          <div>
            <span className="font-mono text-xs font-black text-cyan-300">O(log n) Logarithmic</span>
            <div className="text-[10px] text-slate-400">Binary halving</div>
          </div>
          <div className="text-sm font-mono font-bold text-white">~20 steps</div>
        </div>

        {/* O(n) */}
        <div
          className={`p-3 rounded-xl border transition-all duration-300 flex items-center justify-between ${
            step === 2
              ? "bg-purple-950/80 border-purple-400 shadow-lg shadow-purple-500/20 ring-2 ring-purple-500/30 scale-102"
              : "bg-slate-900 border-slate-800 opacity-60"
          }`}
        >
          <div>
            <span className="font-mono text-xs font-black text-purple-300">O(n) Linear</span>
            <div className="text-[10px] text-slate-400">Single linear pass</div>
          </div>
          <div className="text-sm font-mono font-bold text-white">1,000,000 steps</div>
        </div>

        {/* O(n^2) */}
        <div
          className={`p-3 rounded-xl border transition-all duration-300 flex items-center justify-between ${
            step === 3
              ? "bg-red-950/80 border-red-500 shadow-lg shadow-red-500/30 ring-2 ring-red-500/40 scale-102"
              : "bg-slate-900 border-slate-800 opacity-60"
          }`}
        >
          <div>
            <span className="font-mono text-xs font-black text-red-400">O(n²) Quadratic</span>
            <div className="text-[10px] text-slate-400">Nested double loops</div>
          </div>
          <div className="text-sm font-mono font-bold text-red-300">1,000,000,000,000 steps!</div>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 2: TWO POINTERS CONVERGENCE
// =========================================================================
export function TwoPointersVisualizer() {
  const [step, setStep] = useState(0);
  const chars = ["r", "a", "c", "e", "c", "a", "r"];

  const steps: VisualizerStep[] = [
    {
      title: "Step 0: Initialize Pointers at Ends",
      description: "Place `left = 0` (index 0) and `right = 6` (last element). Word: 'racecar'.",
      codeSnippet: "left = 0; right = len(s) - 1",
    },
    {
      title: "Step 1: Check Outermost Characters",
      description: "Compare chars[0] ('r') == chars[6] ('r'). Match! Increment left += 1, decrement right -= 1.",
      codeSnippet: "s[left] == s[right] -> Match!",
    },
    {
      title: "Step 2: Check Next Inward Pair",
      description: "Compare chars[1] ('a') == chars[5] ('a'). Match! Advance pointers inward.",
      codeSnippet: "left = 2; right = 4",
    },
    {
      title: "Step 3: Check Inner Pair",
      description: "Compare chars[2] ('c') == chars[4] ('c'). Match! Advance pointers inward.",
      codeSnippet: "left = 3; right = 3",
    },
    {
      title: "Step 4: Pointers Meet (Palindrome Verified)",
      description: "Left and right meet at index 3 ('e'). Loop terminates: `left >= right`. Returns True in O(n) time!",
      codeSnippet: "return True  # Palindrome verified!",
    },
  ];

  const leftPtr = [0, 1, 2, 3, 3][step];
  const rightPtr = [6, 5, 4, 3, 3][step];

  return (
    <VisualizerShell
      title="Two Pointers: Converging Palindrome"
      subtitle="Testing symmetry from both ends with O(1) extra space"
      tag="Algorithms • Level 2"
      accentColor="#22c1a4"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="space-y-4 max-w-lg mx-auto py-2">
        <div className="flex items-center justify-center gap-2">
          {chars.map((char, idx) => {
            const isLeft = idx === leftPtr;
            const isRight = idx === rightPtr;
            const isBetween = idx > leftPtr && idx < rightPtr;
            const isDone = (idx < leftPtr && idx > rightPtr) || (step === 4);

            return (
              <div key={idx} className="flex flex-col items-center">
                {/* Pointer indicator above */}
                <div className="h-5 text-[10px] font-mono font-bold">
                  {isLeft && isRight ? (
                    <span className="text-emerald-400">L+R</span>
                  ) : isLeft ? (
                    <span className="text-cyan-400">Left</span>
                  ) : isRight ? (
                    <span className="text-purple-400">Right</span>
                  ) : null}
                </div>

                {/* Character Cell */}
                <div
                  className={`w-11 h-12 rounded-xl border flex items-center justify-center font-mono text-lg font-black transition-all duration-300 ${
                    isLeft || isRight
                      ? "bg-cyan-950/80 border-cyan-400 ring-2 ring-cyan-500/40 text-white scale-105 shadow-lg shadow-cyan-500/20"
                      : isDone
                      ? "bg-emerald-950/40 border-emerald-500/60 text-emerald-300"
                      : "bg-slate-900 border-slate-800 text-slate-300"
                  }`}
                >
                  {char}
                </div>

                {/* Index below */}
                <span className="text-[10px] font-mono text-slate-500 mt-1">
                  {idx}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 3: BINARY SEARCH HALVER
// =========================================================================
export function BinarySearchVisualizer() {
  const [step, setStep] = useState(0);
  const arr = [1, 3, 5, 7, 9, 11, 13, 15, 17];
  const target = 13;

  const steps: VisualizerStep[] = [
    {
      title: "Step 0: Initial Range [0..8]",
      description: "Search target 13 in sorted array. `lo = 0`, `hi = 8`.",
      codeSnippet: "lo = 0; hi = 8",
    },
    {
      title: "Step 1: First Midpoint (mid = 4, val = 9)",
      description: "mid = (0 + 8) // 2 = 4. arr[4] = 9. Since 9 < 13, target is in RIGHT half. Discard [0..4]!",
      codeSnippet: "lo = mid + 1 (5)",
    },
    {
      title: "Step 2: Second Midpoint (mid = 6, val = 13)",
      description: "mid = (5 + 8) // 2 = 6. arr[6] = 13. MATCH FOUND! Return index 6 in only 2 steps!",
      codeSnippet: "return 6  # Found target!",
    },
  ];

  const loIdx = [0, 5, 5][step];
  const hiIdx = [8, 8, 8][step];
  const midIdx = [null, 4, 6][step];

  return (
    <VisualizerShell
      title="Binary Search: Halving the Space"
      subtitle="Eliminating half the remaining elements at every step"
      tag="Algorithms • Level 3"
      accentColor="#22c1a4"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="space-y-4 max-w-xl mx-auto py-2">
        <div className="text-[11px] font-mono text-slate-400 text-center mb-1">
          Target: <span className="text-cyan-400 font-bold font-mono">13</span>
        </div>

        <div className="flex items-center justify-center gap-1.5 flex-wrap sm:flex-nowrap">
          {arr.map((val, idx) => {
            const isMid = idx === midIdx;
            const isInRange = idx >= loIdx && idx <= hiIdx;
            const isTargetMatch = step === 2 && val === 13;

            return (
              <div key={idx} className="flex flex-col items-center">
                {/* Pointer marker */}
                <div className="h-5 text-[10px] font-mono font-bold">
                  {isTargetMatch ? (
                    <span className="text-emerald-400 animate-bounce">HIT!</span>
                  ) : isMid ? (
                    <span className="text-purple-400">MID</span>
                  ) : idx === loIdx ? (
                    <span className="text-cyan-400">LO</span>
                  ) : idx === hiIdx ? (
                    <span className="text-cyan-400">HI</span>
                  ) : null}
                </div>

                {/* Array Block */}
                <div
                  className={`w-10 h-11 rounded-lg border flex items-center justify-center font-mono text-xs font-bold transition-all duration-300 ${
                    isTargetMatch
                      ? "bg-emerald-950 border-emerald-400 ring-2 ring-emerald-500 text-emerald-300 scale-110 shadow-lg shadow-emerald-500/40"
                      : isMid
                      ? "bg-purple-950/80 border-purple-400 ring-2 ring-purple-500 text-white scale-105"
                      : isInRange
                      ? "bg-slate-900 border-slate-700 text-slate-200"
                      : "bg-slate-950/60 border-slate-900 text-slate-600 line-through opacity-40"
                  }`}
                >
                  {val}
                </div>

                <span className="text-[9px] font-mono text-slate-600 mt-1">
                  {idx}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 4: SLIDING WINDOW MAX SUM
// =========================================================================
export function SlidingWindowVisualizer() {
  const [step, setStep] = useState(0);
  const nums = [2, 1, 5, 1, 3, 2];
  const k = 3;

  const steps: VisualizerStep[] = [
    {
      title: "Step 0: Initial Window [0..2]",
      description: "Calculate initial sum of first k=3 elements: 2 + 1 + 5 = 8. Max sum = 8.",
      codeSnippet: "window_sum = 8",
    },
    {
      title: "Step 1: Slide Window Right (Indices 1..3)",
      description: "O(1) update: subtract outgoing nums[0] (2), add incoming nums[3] (1). sum = 8 - 2 + 1 = 7.",
      codeSnippet: "window_sum += nums[3] - nums[0]  # 7",
    },
    {
      title: "Step 2: Slide Window Right (Indices 2..4)",
      description: "Subtract outgoing nums[1] (1), add incoming nums[4] (3). sum = 7 - 1 + 3 = 9. New Max = 9!",
      codeSnippet: "max_sum = max(8, 9) -> 9",
    },
    {
      title: "Step 3: Final Window (Indices 3..5)",
      description: "Subtract outgoing nums[2] (5), add incoming nums[5] (2). sum = 9 - 5 + 2 = 6. Complete!",
      codeSnippet: "return 9",
    },
  ];

  const windowStart = [0, 1, 2, 3][step];
  const currentSum = [8, 7, 9, 6][step];
  const maxSum = [8, 8, 9, 9][step];

  return (
    <VisualizerShell
      title="Sliding Window: Subarray Sum of Size K"
      subtitle="Maintaining running totals in O(1) time per slide"
      tag="Algorithms • Level 4"
      accentColor="#22c1a4"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="space-y-5 max-w-lg mx-auto py-2">
        <div className="flex items-center justify-center gap-2">
          {nums.map((val, idx) => {
            const inWindow = idx >= windowStart && idx < windowStart + k;
            return (
              <div key={idx} className="flex flex-col items-center">
                <div
                  className={`w-12 h-14 rounded-xl border flex items-center justify-center font-mono text-base font-bold transition-all duration-300 ${
                    inWindow
                      ? "bg-purple-950/80 border-purple-400 ring-2 ring-purple-500/40 text-white scale-105 shadow-lg shadow-purple-500/20"
                      : "bg-slate-900/60 border-slate-800 text-slate-500"
                  }`}
                >
                  {val}
                </div>
                <span className="text-[10px] font-mono text-slate-600 mt-1">
                  [{idx}]
                </span>
              </div>
            );
          })}
        </div>

        {/* Status bar */}
        <div className="flex items-center justify-around p-3 rounded-xl bg-slate-900 border border-slate-800 font-mono text-xs">
          <div>
            <span className="text-slate-400">Current Window Sum: </span>
            <span className="text-cyan-400 font-bold">{currentSum}</span>
          </div>
          <div className="h-4 w-px bg-slate-800" />
          <div>
            <span className="text-slate-400">Max Sum: </span>
            <span className="text-emerald-400 font-bold">{maxSum}</span>
          </div>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 5: DP & MEMOIZATION CACHE
// =========================================================================
export function DynamicProgrammingVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 0: Initial Recursive Call",
      description: "We want to compute `fib(4) = fib(3) + fib(2)`. Call tree branches down.",
      codeSnippet: "fib(4)",
    },
    {
      title: "Step 1: Compute and Cache fib(2)",
      description: "fib(2) = fib(1) + fib(0) = 1 + 0 = 1. We store `{2: 1}` in the memoization cache!",
      codeSnippet: "memo[2] = 1",
    },
    {
      title: "Step 2: Compute and Cache fib(3)",
      description: "fib(3) = fib(2) + fib(1) = 1 + 1 = 2. We store `{3: 2}` in the memoization cache!",
      codeSnippet: "memo[3] = 2",
    },
    {
      title: "Step 3: Cache Hit Prunes Redundant Subtree!",
      description: "The right branch now needs `fib(2)`. Instead of recomputing, it hits `memo[2]` instantly in O(1)!",
      codeSnippet: "return memo[2]  # Instant Cache Hit!",
    },
  ];

  return (
    <VisualizerShell
      title="Dynamic Programming: Memoization Cache"
      subtitle="How caching intermediate results prunes exponential subtrees into linear O(n)"
      tag="Algorithms • Level 5"
      accentColor="#22c1a4"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="space-y-4 max-w-md mx-auto py-2">
        {/* Memoization Cache Table */}
        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
          <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold mb-1.5 flex items-center justify-between">
            <span>Memoization Cache (Dictionary)</span>
            <span className="text-emerald-400 font-bold">O(1) Access</span>
          </div>
          <div className="flex items-center gap-2 font-mono text-xs">
            <div className={`px-2.5 py-1 rounded border ${step >= 1 ? "bg-purple-900/60 border-purple-500 text-white" : "bg-slate-950 border-slate-800 text-slate-600"}`}>
              fib(2) = 1
            </div>
            <div className={`px-2.5 py-1 rounded border ${step >= 2 ? "bg-purple-900/60 border-purple-500 text-white" : "bg-slate-950 border-slate-800 text-slate-600"}`}>
              fib(3) = 2
            </div>
          </div>
        </div>

        {/* Tree status */}
        <div className="text-center p-4 rounded-xl bg-slate-950 border border-slate-800">
          <div className="font-mono text-xs text-slate-400 mb-2">Recursive Call Tree</div>
          <div className="flex items-center justify-center gap-4">
            <div className="px-3 py-1.5 rounded-lg bg-cyan-950 border border-cyan-500 text-cyan-300 font-mono text-xs font-bold">
              Left: fib(3) (computed)
            </div>
            <span className="text-slate-600 font-mono">+</span>
            <div className={`px-3 py-1.5 rounded-lg border font-mono text-xs font-bold ${
              step >= 3
                ? "bg-emerald-950 border-emerald-400 text-emerald-300 ring-2 ring-emerald-500/40 animate-pulse"
                : "bg-slate-900 border-slate-800 text-slate-500"
            }`}>
              Right: fib(2) {step >= 3 ? "⚡ CACHE HIT!" : "(pending)"}
            </div>
          </div>
        </div>
      </div>
    </VisualizerShell>
  );
}
