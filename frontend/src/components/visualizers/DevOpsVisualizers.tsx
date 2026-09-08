"use client";

import React, { useState } from "react";
import { VisualizerShell } from "./VisualizerShell";
import { VisualizerStep } from "./types";
import { Terminal, GitBranch, Box, RefreshCw, Activity, Check, AlertTriangle } from "lucide-react";

// =========================================================================
// LEVEL 1: LINUX PIPES & STREAMS
// =========================================================================
export function LinuxPipesVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Command 1 (cat access.log)",
      description: "Reads raw log file lines and emits them to Standard Output (stdout, stream 1).",
      codeSnippet: "cat access.log",
    },
    {
      title: "Step 2: The Unix Pipe (|)",
      description: "The pipe connects stdout of Command 1 directly into Standard Input (stdin, stream 0) of Command 2 in memory!",
      codeSnippet: "cat access.log | grep 500",
    },
    {
      title: "Step 3: Filtered Output & Error Routing",
      description: "grep filters only HTTP 500 error lines. Any process errors route to stderr (stream 2) without mixing with stdout.",
      codeSnippet: "cat access.log | grep 500 2> errors.txt",
    },
  ];

  return (
    <VisualizerShell
      title="Linux Standard Streams & Pipes"
      subtitle="How Unix processes chain stdout, stdin, and stderr together"
      tag="DevOps • Level 1"
      accentColor="#52c41a"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="flex items-center justify-center gap-3 max-w-lg mx-auto py-2 font-mono text-xs">
        {/* Cmd 1 */}
        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center">
          <div className="text-slate-400 text-[10px] mb-1">Process 1</div>
          <div className="text-emerald-400 font-bold">cat access.log</div>
        </div>

        {/* Pipe */}
        <div className="flex flex-col items-center">
          <span className="text-xs text-slate-500">stdout (1)</span>
          <div className={`px-2.5 py-1 rounded-lg border font-bold text-sm transition-all ${
            step >= 1 ? "bg-emerald-950 border-emerald-400 text-emerald-300 ring-2 ring-emerald-500/40 animate-pulse" : "bg-slate-950 border-slate-800 text-slate-600"
          }`}>
            |
          </div>
          <span className="text-xs text-slate-500">stdin (0)</span>
        </div>

        {/* Cmd 2 */}
        <div className={`p-3 rounded-xl border text-center transition-all ${
          step >= 1 ? "bg-slate-900 border-slate-800" : "bg-slate-950 border-slate-900 opacity-40"
        }`}>
          <div className="text-slate-400 text-[10px] mb-1">Process 2</div>
          <div className="text-cyan-400 font-bold">grep 500</div>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 2: GIT THREE TREES & DAG
// =========================================================================
export function GitTreesVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Working Directory",
      description: "You edit `auth.py` on your laptop. The file is modified in the Working Directory (unstaged).",
      codeSnippet: "git status  # Changes not staged for commit",
    },
    {
      title: "Step 2: Staging Area (Index)",
      description: "`git add auth.py` stages the exact diff for the next snapshot. Staging area is now green!",
      codeSnippet: "git add auth.py",
    },
    {
      title: "Step 3: Permanent Commit (HEAD)",
      description: "`git commit -m 'feat: auth'` writes a permanent, cryptographic SHA commit node to the repository history DAG!",
      codeSnippet: "git commit -m 'feat: auth'  # [main 94ef329]",
    },
  ];

  return (
    <VisualizerShell
      title="Git: The Three Tree Architecture"
      subtitle="Working Directory ──► Staging Area ──► Commit History (HEAD)"
      tag="DevOps • Level 2"
      accentColor="#52c41a"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="grid grid-cols-3 gap-3 max-w-lg mx-auto py-2 font-mono text-xs">
        {/* Working Dir */}
        <div className={`p-3.5 rounded-xl border text-center transition-all ${
          step === 0 ? "bg-amber-950/70 border-amber-400 text-amber-200 ring-2 ring-amber-500/30" : "bg-slate-900 border-slate-800 text-slate-400"
        }`}>
          <span className="text-[10px] uppercase font-bold block mb-1">Working Tree</span>
          <div className="font-bold">auth.py</div>
          <span className="text-[9px] text-slate-500">{step === 0 ? "Modified" : "Clean"}</span>
        </div>

        {/* Staging */}
        <div className={`p-3.5 rounded-xl border text-center transition-all ${
          step === 1 ? "bg-emerald-950/80 border-emerald-400 text-emerald-200 ring-2 ring-emerald-500/40" : "bg-slate-900 border-slate-800 text-slate-400"
        }`}>
          <span className="text-[10px] uppercase font-bold block mb-1">Staging Area</span>
          <div className="font-bold">{step >= 1 ? "auth.py staged" : "(Empty)"}</div>
          <span className="text-[9px] text-slate-500">{step === 1 ? "Ready to commit" : "Idle"}</span>
        </div>

        {/* Repository */}
        <div className={`p-3.5 rounded-xl border text-center transition-all ${
          step === 2 ? "bg-purple-950/80 border-purple-400 text-purple-200 ring-2 ring-purple-500/40 shadow-lg" : "bg-slate-900 border-slate-800 text-slate-400"
        }`}>
          <span className="text-[10px] uppercase font-bold block mb-1">HEAD Commit</span>
          <div className="font-bold">{step === 2 ? "commit 94ef329" : "commit 9890229"}</div>
          <span className="text-[9px] text-slate-500">Immutable snapshot</span>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 3: DOCKER CONTAINERS vs VMs
// =========================================================================
export function DockerVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Heavyweight Virtual Machine",
      description: "Each VM runs a full guest OS kernel (4-10 GB), requiring a hypervisor and taking 60 seconds to boot.",
      codeSnippet: "VM: Hypervisor -> Guest OS Kernel -> App",
    },
    {
      title: "Lightweight Docker Container",
      description: "Containers share the host Linux kernel directly! Isolated via Linux Namespaces (PID, Net) and cgroups (RAM limits).",
      codeSnippet: "Docker: Shared Kernel -> Namespaces -> App",
    },
    {
      title: "Instant Startup & Layer Caching",
      description: "Boots in 300 milliseconds. Image layers are cached, reusing dependencies across builds!",
      codeSnippet: "docker run -d -p 8000:8000 app:v1 (0.3s)",
    },
  ];

  return (
    <VisualizerShell
      title="Docker Containers vs Virtual Machines"
      subtitle="How kernel sharing and Linux namespaces enable instant, isolated containers"
      tag="DevOps • Level 3"
      accentColor="#52c41a"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="grid grid-cols-2 gap-4 max-w-md mx-auto py-2 font-mono text-xs">
        {/* VM */}
        <div className={`p-4 rounded-xl border text-center ${
          step === 0 ? "bg-amber-950/60 border-amber-500 ring-2 ring-amber-500/30" : "bg-slate-900 border-slate-800 opacity-60"
        }`}>
          <div className="font-bold text-amber-400 mb-2">Virtual Machine</div>
          <div className="space-y-1 text-[11px]">
            <div className="p-1 rounded bg-slate-950">App Code</div>
            <div className="p-1 rounded bg-slate-950">Full Guest OS (4GB)</div>
            <div className="p-1 rounded bg-slate-950">Hypervisor</div>
          </div>
          <span className="text-[10px] text-slate-500 mt-2 block">Boot: 60 seconds</span>
        </div>

        {/* Container */}
        <div className={`p-4 rounded-xl border text-center ${
          step >= 1 ? "bg-emerald-950/80 border-emerald-400 ring-2 ring-emerald-500/40 shadow-lg" : "bg-slate-900 border-slate-800 opacity-60"
        }`}>
          <div className="font-bold text-emerald-400 mb-2">Docker Container</div>
          <div className="space-y-1 text-[11px]">
            <div className="p-1 rounded bg-emerald-900/60 text-white font-bold">App Code (Isolated)</div>
            <div className="p-1 rounded bg-slate-950 text-slate-400">cgroups + Namespaces</div>
            <div className="p-1 rounded bg-cyan-950 text-cyan-300">Shared Linux Kernel</div>
          </div>
          <span className="text-[10px] text-emerald-400 font-bold mt-2 block">Boot: 0.3 seconds!</span>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 4: BLUE/GREEN DEPLOYMENTS
// =========================================================================
export function DeploymentVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Live Production on Blue (v1.0)",
      description: "Router directs 100% of live user traffic to Blue environment (v1.0).",
      codeSnippet: "Traffic: 100% -> Blue (v1.0)",
    },
    {
      title: "Deploy & Warm Up Green (v2.0)",
      description: "Green environment spins up v2.0 in parallel. Automated health checks run without touching users.",
      codeSnippet: "Health check Green /healthz: 200 OK",
    },
    {
      title: "Instant Zero-Downtime Router Switch",
      description: "Router flips all traffic to Green! Blue stays on standby in case an instant rollback is required.",
      codeSnippet: "Traffic: 100% -> Green (v2.0) [Zero downtime]",
    },
  ];

  return (
    <VisualizerShell
      title="Blue/Green Zero-Downtime Deployment"
      subtitle="How load balancers switch traffic seamlessly between parallel environments"
      tag="DevOps • Level 4"
      accentColor="#52c41a"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-4 py-2 font-mono text-xs text-center">
        <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300">
          Load Balancer Router: <span className="font-bold text-white">{step === 2 ? "Routed to GREEN" : "Routed to BLUE"}</span>
        </div>

        <div className="grid grid-cols-2 gap-4">
          {/* Blue */}
          <div className={`p-4 rounded-xl border transition-all ${
            step < 2 ? "bg-cyan-950/70 border-cyan-400 ring-2 ring-cyan-500/40 shadow-lg text-white" : "bg-slate-900 border-slate-800 text-slate-500 opacity-50"
          }`}>
            <span className="font-bold block text-sm mb-1 text-cyan-400">BLUE (v1.0)</span>
            <span>{step < 2 ? "100% Live Traffic" : "Idle Standby"}</span>
          </div>

          {/* Green */}
          <div className={`p-4 rounded-xl border transition-all ${
            step === 2 ? "bg-emerald-950/80 border-emerald-400 ring-2 ring-emerald-500/40 shadow-lg text-white" : "bg-slate-900 border-slate-800 text-slate-500 opacity-50"
          }`}>
            <span className="font-bold block text-sm mb-1 text-emerald-400">GREEN (v2.0)</span>
            <span>{step === 2 ? "100% Live Traffic" : step === 1 ? "Health Checking..." : "Offline"}</span>
          </div>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 5: OBSERVABILITY & GOLDEN SIGNALS
// =========================================================================
export function ObservabilityVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Healthy System State",
      description: "Latency: 45ms, Traffic: 1,200 req/s, Errors: 0.01%, Saturation: 35%. All monitors green!",
      codeSnippet: "Status: 200 OK across all pods",
    },
    {
      title: "Latency & Error Spike Detected",
      description: "Database connection pool saturated. Latency jumps to 420ms, 5xx error rate spikes to 3.2%!",
      codeSnippet: "ALERT: 5xx Error Rate > 1% (PagerDuty alert triggered)",
    },
    {
      title: "Automated Healing & Recovery",
      description: "Autoscaler spins up 3 database replicas. Metrics normalize back into SLO safety bounds.",
      codeSnippet: "SLO Restored: Error rate < 0.05%",
    },
  ];

  return (
    <VisualizerShell
      title="Observability & The 4 Golden Signals"
      subtitle="Monitoring Latency, Traffic, Errors, and Saturation in real time"
      tag="DevOps • Level 5"
      accentColor="#52c41a"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 max-w-lg mx-auto py-2 font-mono text-xs text-center">
        {/* Latency */}
        <div className={`p-3 rounded-xl border ${step === 1 ? "bg-red-950/80 border-red-500 text-red-300" : "bg-slate-900 border-slate-800 text-white"}`}>
          <div className="text-[10px] text-slate-400 mb-1">Latency (P99)</div>
          <div className="text-base font-bold">{step === 1 ? "420ms" : "45ms"}</div>
        </div>

        {/* Traffic */}
        <div className="p-3 rounded-xl border bg-slate-900 border-slate-800 text-white">
          <div className="text-[10px] text-slate-400 mb-1">Traffic</div>
          <div className="text-base font-bold">1,200 rps</div>
        </div>

        {/* Errors */}
        <div className={`p-3 rounded-xl border ${step === 1 ? "bg-red-950/80 border-red-500 text-red-300 animate-pulse" : "bg-slate-900 border-slate-800 text-white"}`}>
          <div className="text-[10px] text-slate-400 mb-1">5xx Errors</div>
          <div className="text-base font-bold">{step === 1 ? "3.2%" : "0.01%"}</div>
        </div>

        {/* Saturation */}
        <div className={`p-3 rounded-xl border ${step === 1 ? "bg-amber-950/80 border-amber-500 text-amber-300" : "bg-slate-900 border-slate-800 text-white"}`}>
          <div className="text-[10px] text-slate-400 mb-1">CPU Load</div>
          <div className="text-base font-bold">{step === 1 ? "92%" : "35%"}</div>
        </div>
      </div>
    </VisualizerShell>
  );
}
