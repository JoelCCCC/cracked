"use client";

import React, { useState } from "react";
import { VisualizerShell } from "./VisualizerShell";
import { VisualizerStep } from "./types";
import { Globe, Server, Shield, Lock, Laptop, Check, AlertTriangle } from "lucide-react";

// =========================================================================
// LEVEL 1: HTTP REQUEST & DNS PACKET LIFECYCLE
// =========================================================================
export function HttpLifecycleVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: DNS Domain Resolution",
      description: "Client queries DNS server: 'Where is api.example.com?' DNS answers with IP address: 93.184.216.34.",
      codeSnippet: "DNS: api.example.com -> 93.184.216.34",
    },
    {
      title: "Step 2: TCP 3-Way Handshake",
      description: "SYN (Client asks to connect) ──► SYN-ACK (Server accepts) ──► ACK (Connection established).",
      codeSnippet: "TCP: SYN -> SYN-ACK -> ACK",
    },
    {
      title: "Step 3: TLS Cryptographic Handshake",
      description: "Client and Server exchange certificates and agree on a symmetric AES encryption key. Traffic is now secure!",
      codeSnippet: "TLS: HTTPS session key established",
    },
    {
      title: "Step 4: HTTP Request & 200 OK Response",
      description: "Client sends `POST /orders` with JSON payload. Server processes logic and responds with `200 OK`!",
      codeSnippet: "HTTP/1.1 200 OK (Content-Type: application/json)",
    },
  ];

  return (
    <VisualizerShell
      title="The HTTP & TLS Network Lifecycle"
      subtitle="From DNS resolution and TCP handshakes to the HTTP response"
      tag="Web Dev • Level 1"
      accentColor="#ff7a45"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="flex items-center justify-between max-w-xl mx-auto py-4 relative">
        {/* Client */}
        <div className="flex flex-col items-center z-10">
          <div className="w-14 h-14 rounded-2xl bg-cyan-950 border border-cyan-500 flex items-center justify-center text-cyan-300 shadow-lg shadow-cyan-500/20">
            <Laptop className="w-7 h-7" />
          </div>
          <span className="text-xs font-mono font-bold text-white mt-2">Browser Client</span>
          <span className="text-[10px] font-mono text-slate-500">192.168.1.5</span>
        </div>

        {/* Network Packet Animation in between */}
        <div className="flex-1 mx-4 flex flex-col items-center">
          <div className="w-full h-1 bg-slate-800 rounded-full relative">
            <div
              className={`absolute top-1/2 -translate-y-1/2 w-4 h-4 rounded-full bg-gradient-to-r from-orange-400 to-amber-300 shadow-lg shadow-orange-500/50 transition-all duration-700 ${
                step === 0
                  ? "left-1/4"
                  : step === 1
                  ? "left-1/2 animate-pulse"
                  : step === 2
                  ? "left-3/4"
                  : "left-full -translate-x-4"
              }`}
            />
          </div>

          <span className="mt-3 px-3 py-1 rounded-full text-[10px] font-mono font-bold bg-slate-900 border border-slate-800 text-orange-400">
            {step === 0 && "DNS Query: IP 93.184.216.34"}
            {step === 1 && "TCP 3-Way SYN / ACK"}
            {step === 2 && "TLS Encryption Key Exchange"}
            {step === 3 && "HTTP POST -> 200 OK"}
          </span>
        </div>

        {/* Server */}
        <div className="flex flex-col items-center z-10">
          <div className="w-14 h-14 rounded-2xl bg-purple-950 border border-purple-500 flex items-center justify-center text-purple-300 shadow-lg shadow-purple-500/20">
            <Server className="w-7 h-7" />
          </div>
          <span className="text-xs font-mono font-bold text-white mt-2">API Server</span>
          <span className="text-[10px] font-mono text-slate-500">93.184.216.34</span>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 2: DOM TREE & EVENT BUBBLING
// =========================================================================
export function DomTreeVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Document Root",
      description: "The browser parses HTML and instantiates the Document Object Model tree root.",
      codeSnippet: "document.documentElement",
    },
    {
      title: "Step 2: Body & Container Nodes",
      description: "Child nodes `<body>` and `<main>` are appended to the tree hierarchy.",
      codeSnippet: "<body> -> <main>",
    },
    {
      title: "Step 3: Target Element & Event Trigger",
      description: "User clicks `<button id='btn'>`. An event object is dispatched at the target element!",
      codeSnippet: "button.addEventListener('click')",
    },
    {
      title: "Step 4: Event Bubbling Upwards",
      description: "The event bubbles upwards through `<main>` -> `<body>` -> `document`. Parents can intercept with event delegation!",
      codeSnippet: "event.stopPropagation() to halt",
    },
  ];

  return (
    <VisualizerShell
      title="The DOM Tree & Event Bubbling"
      subtitle="How HTML transforms into an in-memory tree and propagates user events"
      tag="Web Dev • Level 2"
      accentColor="#ff7a45"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-sm mx-auto space-y-2 py-2">
        {/* Document */}
        <div className={`p-2.5 rounded-xl border text-center font-mono text-xs transition-all duration-300 ${
          step === 3 ? "bg-orange-950 border-orange-400 text-orange-200 ring-2 ring-orange-500/40" : "bg-slate-900 border-slate-800 text-white"
        }`}>
          #document (Root)
        </div>
        <div className="w-0.5 h-3 bg-slate-700 mx-auto" />

        {/* Body */}
        <div className={`p-2.5 rounded-xl border text-center font-mono text-xs transition-all duration-300 ${
          step === 3 ? "bg-orange-950 border-orange-400 text-orange-200 ring-2 ring-orange-500/40" : "bg-slate-900 border-slate-800 text-white"
        }`}>
          &lt;body&gt;
        </div>
        <div className="w-0.5 h-3 bg-slate-700 mx-auto" />

        {/* Main */}
        <div className={`p-2.5 rounded-xl border text-center font-mono text-xs transition-all duration-300 ${
          step === 3 ? "bg-orange-950 border-orange-400 text-orange-200 ring-2 ring-orange-500/40" : "bg-slate-900 border-slate-800 text-white"
        }`}>
          &lt;main class=&quot;container&quot;&gt;
        </div>
        <div className="w-0.5 h-3 bg-slate-700 mx-auto" />

        {/* Button */}
        <div className={`p-3 rounded-xl border text-center font-mono text-xs font-bold transition-all duration-300 ${
          step >= 2 ? "bg-purple-950 border-purple-400 text-purple-200 ring-2 ring-purple-500/50 scale-105 shadow-lg shadow-purple-500/30" : "bg-slate-900 border-slate-800 text-slate-300"
        }`}>
          &lt;button id=&quot;btn&quot;&gt;Click Me!&lt;/button&gt;
          {step >= 2 && (
            <div className="text-[10px] text-cyan-400 font-normal mt-0.5 animate-pulse">
              {step === 2 ? "⚡ Click Event Dispatched!" : "▲ Bubbling Event Up"}
            </div>
          )}
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 3: ASYNC EVENT LOOP & FETCH
// =========================================================================
export function EventLoopVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Step 1: Synchronous Call Stack",
      description: "`fetch('/api/data')` is invoked on the JavaScript Call Stack.",
      codeSnippet: "await fetch('/api/data')",
    },
    {
      title: "Step 2: Offloaded to Web API Worker",
      description: "Network I/O is handed off to browser background threads. The main Call Stack stays completely free and non-blocking!",
      codeSnippet: "Web APIs handling HTTP bytes in background",
    },
    {
      title: "Step 3: Response Arrives in Microtask Queue",
      description: "When network bytes arrive, the Promise resolution callback is placed in the Microtask Queue.",
      codeSnippet: "Promise.then() queued",
    },
    {
      title: "Step 4: Event Loop Ticks",
      description: "The Event Loop checks: Call stack is empty! Pushes the callback back to the Call Stack for immediate execution.",
      codeSnippet: "const data = await res.json()",
    },
  ];

  return (
    <VisualizerShell
      title="The JavaScript Async Event Loop"
      subtitle="How non-blocking network calls execute without freezing the browser UI"
      tag="Web Dev • Level 3"
      accentColor="#ff7a45"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="grid grid-cols-3 gap-3 max-w-lg mx-auto py-2">
        {/* Call Stack */}
        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center">
          <span className="text-[10px] font-mono text-slate-400 uppercase font-bold block mb-2">Call Stack</span>
          <div className={`p-2 rounded-lg font-mono text-[11px] border ${
            step === 0 || step === 3 ? "bg-purple-950 border-purple-400 text-purple-300 font-bold" : "bg-slate-950 border-slate-900 text-slate-600"
          }`}>
            {step === 0 ? "fetch()" : step === 3 ? "handleData()" : "(Idle)"}
          </div>
        </div>

        {/* Web APIs */}
        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center">
          <span className="text-[10px] font-mono text-slate-400 uppercase font-bold block mb-2">Web APIs (Background)</span>
          <div className={`p-2 rounded-lg font-mono text-[11px] border ${
            step === 1 ? "bg-cyan-950 border-cyan-400 text-cyan-300 font-bold animate-pulse" : "bg-slate-950 border-slate-900 text-slate-600"
          }`}>
            {step === 1 ? "HTTP Network I/O" : "(Idle)"}
          </div>
        </div>

        {/* Task Queue */}
        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center">
          <span className="text-[10px] font-mono text-slate-400 uppercase font-bold block mb-2">Microtask Queue</span>
          <div className={`p-2 rounded-lg font-mono text-[11px] border ${
            step === 2 ? "bg-emerald-950 border-emerald-400 text-emerald-300 font-bold" : "bg-slate-950 border-slate-900 text-slate-600"
          }`}>
            {step === 2 ? "resolvePromise" : "(Empty)"}
          </div>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 4: RENDERING STRATEGIES (CSR vs SSR vs SSG)
// =========================================================================
export function RenderingVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "CSR (Client-Side Rendering)",
      description: "Server sends empty HTML (<div id='root'></div>) + large 1MB JS bundle. Browser compiles JS before painting content. Blank first paint!",
      codeSnippet: "CSR: Slow First Contentful Paint",
    },
    {
      title: "SSR (Server-Side Rendering)",
      description: "Server executes component per-request, injects data, and sends pre-rendered HTML. Fast First Paint, but runs server compute on every request.",
      codeSnippet: "SSR: Dynamic per-request HTML",
    },
    {
      title: "SSG & ISR (Incremental Static Revalidation)",
      description: "HTML built once at build time and cached on CDN edge. Serves in 15ms globally with background revalidation!",
      codeSnippet: "export const revalidate = 60; // ISR",
    },
  ];

  return (
    <VisualizerShell
      title="Web Rendering Strategies Compared"
      subtitle="CSR vs SSR vs Static Generation (SSG / ISR)"
      tag="Web Dev • Level 4"
      accentColor="#ff7a45"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-3 py-2">
        <div className={`p-3 rounded-xl border transition-all ${
          step === 0 ? "bg-purple-950/80 border-purple-400 ring-2 ring-purple-500/30 shadow-lg" : "bg-slate-900 border-slate-800 opacity-60"
        }`}>
          <div className="flex items-center justify-between text-xs font-bold font-mono text-white mb-1">
            <span>CSR (Client-Side)</span>
            <span className="text-amber-400 text-[10px]">Blank Initial Paint</span>
          </div>
          <div className="text-[11px] text-slate-300 font-mono">
            HTML: Empty ──► Download JS ──► Execute React ──► Paint UI
          </div>
        </div>

        <div className={`p-3 rounded-xl border transition-all ${
          step === 1 ? "bg-cyan-950/80 border-cyan-400 ring-2 ring-cyan-500/30 shadow-lg" : "bg-slate-900 border-slate-800 opacity-60"
        }`}>
          <div className="flex items-center justify-between text-xs font-bold font-mono text-white mb-1">
            <span>SSR (Server-Side)</span>
            <span className="text-cyan-400 text-[10px]">Fresh Real-Time Data</span>
          </div>
          <div className="text-[11px] text-slate-300 font-mono">
            Server Renders HTML ──► Sends Ready HTML ──► Hydrates
          </div>
        </div>

        <div className={`p-3 rounded-xl border transition-all ${
          step === 2 ? "bg-emerald-950/80 border-emerald-400 ring-2 ring-emerald-500/30 shadow-lg" : "bg-slate-900 border-slate-800 opacity-60"
        }`}>
          <div className="flex items-center justify-between text-xs font-bold font-mono text-white mb-1">
            <span>SSG / ISR (Edge Cached)</span>
            <span className="text-emerald-400 text-[10px]">15ms Global Edge CDN</span>
          </div>
          <div className="text-[11px] text-slate-300 font-mono">
            Pre-built HTML ──► Served Instantly ──► Background Revalidate
          </div>
        </div>
      </div>
    </VisualizerShell>
  );
}

// =========================================================================
// LEVEL 5: WEB SECURITY (XSS & SAMESITE)
// =========================================================================
export function WebSecurityVisualizer() {
  const [step, setStep] = useState(0);

  const steps: VisualizerStep[] = [
    {
      title: "Vulnerability: Unescaped User Input",
      description: "Attacker submits `<script>stealCookie()</script>`. If inserted directly with innerHTML, browser executes malicious JS!",
      codeSnippet: "innerHTML = userInput; // DANGER!",
    },
    {
      title: "Mitigation 1: HTML Entity Sanitization",
      description: "Replace `<` with `&lt;` and `>` with `&gt;`. The browser displays text safely without executing it as code!",
      codeSnippet: "&lt;script&gt; (safe text string)",
    },
    {
      title: "Mitigation 2: HttpOnly & SameSite=Lax Cookies",
      description: "Tokens stored in `HttpOnly` cookies cannot be accessed by JavaScript, preventing token theft even if an XSS flaw exists!",
      codeSnippet: "Set-Cookie: token=...; HttpOnly; SameSite=Lax",
    },
  ];

  return (
    <VisualizerShell
      title="Web Security: XSS Sanitization & Cookie Flags"
      subtitle="Defending against Cross-Site Scripting and token hijacking"
      tag="Web Dev • Level 5"
      accentColor="#ff7a45"
      steps={steps}
      currentStep={step}
      onStepChange={setStep}
    >
      <div className="max-w-md mx-auto space-y-4 py-2">
        <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800">
          <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold mb-1">
            Attacker Payload
          </div>
          <code className="text-xs font-mono text-red-400 block bg-slate-950 p-2 rounded border border-slate-900">
            &lt;script&gt;stealTokens()&lt;/script&gt;
          </code>
        </div>

        <div className={`p-4 rounded-xl border transition-all ${
          step === 0
            ? "bg-red-950/60 border-red-500 shadow-lg shadow-red-500/20"
            : "bg-emerald-950/60 border-emerald-400 shadow-lg shadow-emerald-500/20"
        }`}>
          <div className="flex items-center gap-2 font-mono text-xs font-bold mb-1">
            {step === 0 ? (
              <>
                <AlertTriangle className="w-4 h-4 text-red-400" />
                <span className="text-red-300">Vulnerable: Script Executes in Browser!</span>
              </>
            ) : (
              <>
                <Shield className="w-4 h-4 text-emerald-400" />
                <span className="text-emerald-300">Protected: Rendered Safely as Pure Text</span>
              </>
            )}
          </div>
          <div className="text-[11px] font-mono text-slate-300 mt-1">
            {step === 0 ? "window.localStorage.getItem('token') stolen!" : "&lt;script&gt;stealTokens()&lt;/script&gt;"}
          </div>
        </div>
      </div>
    </VisualizerShell>
  );
}
