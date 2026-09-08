"use client";

import React, { useState } from "react";
import { VisualizerShell } from "./VisualizerShell";
import { VisualizerStep } from "./types";
import { Database, Key, Search, ArrowRight, Lock, Check, AlertCircle } from "lucide-react";

// =========================================================================
// LEVEL 1: RELATIONAL TABLES & PRIMARY KEYS
// =========================================================================
export function RelationalTableVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Relational Schema Definition",
      description: "A table enforces strict column types: `id` (INTEGER PK), `name` (VARCHAR), `score` (INTEGER).",
      codeSnippet: "CREATE TABLE users (id SERIAL PRIMARY KEY, ...)",
    },
    {
      title: "Step 2: Inserting Valid Row",
      description: "Row #1 inserted. `id=1` is assigned by sequence. All type constraints pass.",
      codeSnippet: "INSERT INTO users VALUES (1, 'Alice', 95)",
    },
    {
      title: "Step 3: Primary Key Uniqueness Enforced",
      description: "Attempting to insert another row with `id=1` raises `duplicate key value violates unique constraint`! Primary keys must be unique.",
      codeSnippet: "ERROR: duplicate key value violates unique constraint 'users_pkey'",
    },
  ];

  return (
    <VisualizerShell
      title="Relational Tables & Primary Key Guarantees"
      subtitle="How database schemas enforce column types and entity uniqueness"
      tag="Database • Level 1"
      accentColor="#f5a623"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-3 py-2">
        <div className="rounded-xl border border-slate-800 bg-slate-900 overflow-hidden shadow-lg">
          <table className="w-full text-left font-mono text-xs">
            <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
              <tr>
                <th className="p-2.5 flex items-center gap-1 text-amber-400">
                  <Key className="w-3 h-3" /> id (PK)
                </th>
                <th className="p-2.5">name (VARCHAR)</th>
                <th className="p-2.5">score (INT)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              <tr className="bg-slate-900/80 text-white">
                <td className="p-2.5 font-bold text-amber-300">1</td>
                <td className="p-2.5">&quot;Alice&quot;</td>
                <td className="p-2.5">95</td>
              </tr>
              {step >= 1 && (
                <tr className="bg-slate-900/80 text-white">
                  <td className="p-2.5 font-bold text-amber-300">2</td>
                  <td className="p-2.5">&quot;Bob&quot;</td>
                  <td className="p-2.5">80</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {step === 2 && (
          <div className="p-3 rounded-xl bg-red-950/70 border border-red-500 font-mono text-xs text-red-300 flex items-center gap-2 animate-in slide-in-from-top-2">
            <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
            <span>INSERT id=1 REJECTED: Duplicate Primary Key!</span>
          </div>
        )}
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 2: SQL QUERY EXECUTION PIPELINE
// =========================================================================
export function SqlPipelineVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: FROM (Load Table)",
      description: "Database opens the `employees` table on disk.",
      codeSnippet: "FROM employees",
    },
    {
      title: "Step 2: WHERE (Filter Rows)",
      description: "Filters individual rows: keeps only employees where `active = true`.",
      codeSnippet: "WHERE active = true",
    },
    {
      title: "Step 3: GROUP BY & HAVING (Aggregate)",
      description: "Groups remaining rows by department, then filters aggregated groups: `HAVING count(*) >= 2`.",
      codeSnippet: "GROUP BY dept HAVING count(*) >= 2",
    },
    {
      title: "Step 4: SELECT & ORDER BY (Project & Sort)",
      description: "Picks requested columns and sorts final rows in descending order.",
      codeSnippet: "SELECT dept, count(*) ORDER BY count DESC",
    },
  ];

  return (
    <VisualizerShell
      title="SQL Query Execution Pipeline"
      subtitle="The exact logical order in which databases evaluate queries"
      tag="Database • Level 2"
      accentColor="#f5a623"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="flex items-center justify-center gap-2 max-w-lg mx-auto py-2 flex-wrap">
        {[
          { name: "1. FROM", desc: "Scan table", idx: 0 },
          { name: "2. WHERE", desc: "Filter rows", idx: 1 },
          { name: "3. GROUP BY", desc: "Aggregate", idx: 2 },
          { name: "4. SELECT", desc: "Output", idx: 3 },
        ].map((stage) => {
          const isActive = step === stage.idx;
          const isDone = step > stage.idx;
          return (
            <div
              key={stage.name}
              className={`p-3 rounded-xl border text-center font-mono text-xs transition-all duration-300 ${
                isActive
                  ? "bg-amber-950/80 border-amber-400 text-white ring-2 ring-amber-500/40 scale-105 shadow-lg shadow-amber-500/20"
                  : isDone
                  ? "bg-emerald-950/40 border-emerald-500/50 text-emerald-300"
                  : "bg-slate-900 border-slate-800 text-slate-500"
              }`}
            >
              <div className="font-bold text-xs">{stage.name}</div>
              <div className="text-[10px] text-slate-400 mt-0.5">{stage.desc}</div>
            </div>
          );
        })}
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 3: INNER JOIN vs LEFT JOIN
// =========================================================================
export function JoinsVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Inspecting Tables",
      description: "Table Users (Alice id=1, Bob id=2, Charlie id=3). Table Orders (Order #101 user_id=1, Order #102 user_id=2). Charlie has NO orders!",
      codeSnippet: "users (1, 2, 3) vs orders (1, 2)",
    },
    {
      title: "Step 2: INNER JOIN (Only Matches)",
      description: "Only rows with matching keys in BOTH tables are returned. Charlie is excluded completely.",
      codeSnippet: "SELECT * FROM users INNER JOIN orders ON orders.user_id = users.id",
    },
    {
      title: "Step 3: LEFT JOIN (Preserve All Left Rows)",
      description: "All users are preserved! Charlie appears with order columns set to NULL.",
      codeSnippet: "SELECT * FROM users LEFT JOIN orders ON orders.user_id = users.id",
    },
  ];

  return (
    <VisualizerShell
      title="Relational JOINs: INNER vs LEFT JOIN"
      subtitle="How relational databases combine tables across Foreign Key relationships"
      tag="Database • Level 3"
      accentColor="#f5a623"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-3 py-2 font-mono text-xs">
        <div className="flex items-center justify-between text-[11px] text-slate-400 uppercase font-bold">
          <span>Users</span>
          <span>Orders</span>
        </div>

        {/* Alice (Match) */}
        <div className="p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-500/50 flex items-center justify-between text-white">
          <span>1: Alice</span>
          <span>──►</span>
          <span>Order #101 ($50)</span>
        </div>

        {/* Bob (Match) */}
        <div className="p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-500/50 flex items-center justify-between text-white">
          <span>2: Bob</span>
          <span>──►</span>
          <span>Order #102 ($90)</span>
        </div>

        {/* Charlie (No match) */}
        <div className={`p-2.5 rounded-lg border flex items-center justify-between transition-all ${
          step === 1
            ? "bg-slate-950 border-slate-900 opacity-20 line-through"
            : step === 2
            ? "bg-amber-950/60 border-amber-400 text-amber-200 ring-2 ring-amber-500/30"
            : "bg-slate-900 border-slate-800 text-slate-400"
        }`}>
          <span>3: Charlie</span>
          <span>──►</span>
          <span>{step === 2 ? "NULL (Preserved in LEFT JOIN)" : "(No Order)"}</span>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 4: B-TREE INDEX vs SEQ SCAN
// =========================================================================
export function BTreeVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Sequential Scan (No Index): O(n)",
      description: "Database must read every single disk block from start to finish. On 10M rows, takes 15 seconds!",
      codeSnippet: "Seq Scan on users (cost=0.00..184200.00)",
    },
    {
      title: "B-Tree Index Hop 1: Root Node",
      description: "Search for target id=82. Root node (50) indicates target > 50. Jumps to right child block.",
      codeSnippet: "Root: 82 > 50 -> branch right",
    },
    {
      title: "B-Tree Index Hop 2: Branch Node",
      description: "Branch node (75) indicates target > 75. Jumps directly to leaf node.",
      codeSnippet: "Branch: 82 > 75 -> leaf",
    },
    {
      title: "B-Tree Index Hop 3: Direct Row Read",
      description: "Target id=82 found in leaf block! Finds row in 0.2ms after only 3 disk reads!",
      codeSnippet: "Index Scan using idx_users_id: 0.2ms",
    },
  ];

  return (
    <VisualizerShell
      title="B-Tree Index vs Sequential Table Scan"
      subtitle="How balanced tree indexes jump to records in 3 disk hops"
      tag="Database • Level 4"
      accentColor="#f5a623"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-3 py-2 text-center font-mono">
        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs">
          Target Query: <span className="text-amber-400 font-bold">SELECT * WHERE id = 82</span>
        </div>

        {step === 0 ? (
          <div className="p-4 rounded-xl bg-red-950/60 border border-red-500 text-xs text-red-300">
            <div className="font-bold mb-1">Sequential Full Table Scan</div>
            <p className="text-[11px] text-slate-400">Scanning 10,000,000 rows block-by-block on disk... (15 seconds)</p>
          </div>
        ) : (
          <div className="space-y-2 text-xs">
            <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
              Root Node: [50] (target 82 &gt; 50 ──► go right)
            </div>
            {step >= 2 && (
              <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
                Branch Node: [75] (target 82 &gt; 75 ──► go right)
              </div>
            )}
            {step >= 3 && (
              <div className="p-2.5 rounded-lg bg-emerald-950 border border-emerald-400 text-emerald-300 font-bold ring-2 ring-emerald-500/40 animate-pulse">
                Leaf Node: [82] Found row! (0.2 ms)
              </div>
            )}
          </div>
        )}
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 5: ACID & ROW LOCKING
// =========================================================================
export function AcidVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: BEGIN Transaction",
      description: "Alice has $100, Bob has $50. Transaction begins.",
      codeSnippet: "BEGIN;",
    },
    {
      title: "Step 2: Pessimistic Row Lock",
      description: "`SELECT ... FOR UPDATE` acquires an exclusive row lock on Alice's record. Other transactions are blocked from modifying it.",
      codeSnippet: "SELECT balance FROM accounts WHERE id=1 FOR UPDATE;",
    },
    {
      title: "Step 3: Transfer Balance",
      description: "Deduct $30 from Alice ($70), credit $30 to Bob ($80).",
      codeSnippet: "UPDATE accounts SET balance = balance - 30 WHERE id=1;",
    },
    {
      title: "Step 4: COMMIT & Durability",
      description: "Changes are committed to the Write-Ahead Log (WAL) on disk. Lock is released!",
      codeSnippet: "COMMIT;  # Changes are durable and permanent",
    },
  ];

  return (
    <VisualizerShell
      title="ACID Transactions & Row-Level Locking"
      subtitle="Ensuring all-or-nothing balance transfers under high concurrency"
      tag="Database • Level 5"
      accentColor="#f5a623"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="grid grid-cols-2 gap-4 max-w-md mx-auto py-2 font-mono text-xs">
        {/* Alice */}
        <div className={`p-4 rounded-xl border text-center transition-all ${
          step === 1 || step === 2
            ? "bg-amber-950/70 border-amber-400 ring-2 ring-amber-500/40 shadow-lg"
            : "bg-slate-900 border-slate-800"
        }`}>
          <div className="flex items-center justify-center gap-1.5 text-slate-400 mb-1">
            {step === 1 || step === 2 ? <Lock className="w-3.5 h-3.5 text-amber-400" /> : null}
            <span>Alice (id=1)</span>
          </div>
          <div className="text-2xl font-black text-white">
            ${step >= 3 ? "70" : "100"}
          </div>
          {step === 1 && (
            <span className="text-[10px] text-amber-300 font-bold mt-1 block">
              🔒 Row Locked FOR UPDATE
            </span>
          )}
        </div>

        {/* Bob */}
        <div className="p-4 rounded-xl border bg-slate-900 border-slate-800 text-center">
          <div className="text-slate-400 mb-1">Bob (id=2)</div>
          <div className="text-2xl font-black text-white">
            ${step >= 3 ? "80" : "50"}
          </div>
          {step >= 3 && (
            <span className="text-[10px] text-emerald-400 font-bold mt-1 block">
              +$30 Credited
            </span>
          )}
        </div>
      </div>
    </VisualizerShell>
  );
}
