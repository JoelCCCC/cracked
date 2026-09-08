"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import { TrackSummary } from "@/types";
import {
  Zap,
  ArrowRight,
  Code2,
  Cpu,
  Layers,
  Terminal,
  Database,
  Server,
  Sparkles,
  Archive,
  Flame,
  CheckCircle,
  Play,
  Lock,
} from "lucide-react";

export default function LandingPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [tracks, setTracks] = useState<TrackSummary[]>([]);

  useEffect(() => {
    api.curriculum.getPublicTracks().then(setTracks).catch(console.error);
  }, []);

  const getTrackIcon = (slug: string) => {
    switch (slug) {
      case "coding":
        return <Code2 className="w-5 h-5 text-purple-400" />;
      case "algorithms":
        return <Layers className="w-5 h-5 text-cyan-400" />;
      case "web":
        return <Terminal className="w-5 h-5 text-emerald-400" />;
      case "databases":
        return <Database className="w-5 h-5 text-amber-400" />;
      case "devops":
        return <Server className="w-5 h-5 text-rose-400" />;
      case "ai":
        return <Cpu className="w-5 h-5 text-fuchsia-400" />;
      default:
        return <Zap className="w-5 h-5 text-purple-400" />;
    }
  };

  return (
    <div className="relative min-h-screen bg-[#090a10] bg-grid-pattern">
      {/* Glow gradient blobs */}
      <div className="absolute top-10 left-1/2 -translate-x-1/2 w-[600px] h-[350px] bg-purple-600/15 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute top-40 right-10 w-[400px] h-[300px] bg-cyan-500/10 blur-[130px] rounded-full pointer-events-none" />

      {/* Hero Section */}
      <section className="relative max-w-6xl mx-auto px-4 pt-20 pb-16 sm:pt-28 sm:pb-24 text-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-purple-950/60 border border-purple-500/30 text-purple-300 text-xs font-mono font-medium mb-8">
          <Sparkles className="w-3.5 h-3.5 text-purple-400" />
          <span>The 6-Tier Engineering Progression Engine</span>
        </div>

        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight text-white max-w-4xl mx-auto leading-[1.1]">
          Stop watching tutorials.{" "}
          <span className="bg-gradient-to-r from-purple-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent">
            Get genuinely cracked.
          </span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Level up sequentially through 6 disciplines: Coding Foundations, Algorithms, Web Architecture, Database Internals, DevOps, and AI Engineering.
        </p>

        {/* CTA Buttons */}
        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-sm transition shadow-lg shadow-purple-600/30"
          >
            <span>Open Dashboard</span>
            <ArrowRight className="w-4 h-4" />
          </Link>

          <Link
            href="/tracks"
            className="flex items-center gap-2 px-5 py-3.5 rounded-xl border border-slate-800 bg-slate-900/60 hover:bg-slate-900 text-slate-300 hover:text-white font-medium text-sm transition"
          >
            <span>Curriculum Roadmap</span>
          </Link>

          <Link
            href="/history"
            className="flex items-center gap-2 px-5 py-3.5 rounded-xl border border-cyan-500/30 bg-cyan-950/30 hover:bg-cyan-950/60 text-cyan-300 font-medium text-sm transition"
          >
            <Archive className="w-4 h-4" />
            <span>Solution Vault</span>
          </Link>
        </div>

        {/* Quick Highlights Bar */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
          <div className="p-4 rounded-xl bg-[#0f1120]/80 border border-slate-800/80">
            <div className="text-2xl font-bold font-mono text-purple-400">6</div>
            <div className="text-xs text-slate-400 mt-0.5">Core Disciplines</div>
          </div>
          <div className="p-4 rounded-xl bg-[#0f1120]/80 border border-slate-800/80">
            <div className="text-2xl font-bold font-mono text-cyan-400">18</div>
            <div className="text-xs text-slate-400 mt-0.5">Skill Levels</div>
          </div>
          <div className="p-4 rounded-xl bg-[#0f1120]/80 border border-slate-800/80">
            <div className="text-2xl font-bold font-mono text-emerald-400">72</div>
            <div className="text-xs text-slate-400 mt-0.5">Scored Challenges</div>
          </div>
          <div className="p-4 rounded-xl bg-[#0f1120]/80 border border-slate-800/80">
            <div className="text-2xl font-bold font-mono text-amber-400">&lt; 50ms</div>
            <div className="text-xs text-slate-400 mt-0.5">Sandboxed Evaluation</div>
          </div>
        </div>
      </section>

      {/* Interactive Code Preview Terminal */}
      <section className="max-w-5xl mx-auto px-4 py-12">
        <div className="rounded-2xl border border-slate-800 bg-[#0c0e1a] p-1 shadow-2xl">
          <div className="flex items-center justify-between px-4 py-3 bg-[#111425] rounded-t-xl border-b border-slate-800 text-xs text-slate-400">
            <div className="flex items-center gap-2">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-rose-500/80" />
                <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
              </div>
              <span className="font-mono text-slate-300 ml-2 font-semibold">
                coding/level-1/dedupe.py
              </span>
            </div>
            <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono text-[11px]">
              ALL 5 CASES PASSED ✓
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-800">
            <div className="p-4 font-mono text-xs text-slate-300 leading-relaxed bg-[#090b14]">
              <div className="text-slate-500"># Deduplicate preserving order in O(n)</div>
              <div><span className="text-purple-400">def</span> <span className="text-cyan-300">dedupe</span>(items):</div>
              <div className="pl-4">seen = <span className="text-amber-300">set</span>()</div>
              <div className="pl-4">out = []</div>
              <div className="pl-4"><span className="text-purple-400">for</span> x <span className="text-purple-400">in</span> items:</div>
              <div className="pl-8"><span className="text-purple-400">if</span> x <span className="text-purple-400">not in</span> seen:</div>
              <div className="pl-12">seen.add(x)</div>
              <div className="pl-12">out.append(x)</div>
              <div className="pl-4"><span className="text-purple-400">return</span> out</div>
            </div>

            <div className="p-4 font-mono text-xs bg-[#0b0e1c] flex flex-col justify-between">
              <div>
                <div className="text-slate-500 mb-2">// Automated Test Harness Verdict:</div>
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2 text-emerald-400">
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>case 1: [3, 1, 3, 2, 1] ➔ [3, 1, 2] (passed)</span>
                  </div>
                  <div className="flex items-center gap-2 text-emerald-400">
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>case 2: [] ➔ [] (passed)</span>
                  </div>
                  <div className="flex items-center gap-2 text-emerald-400">
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>case 3: [1, 1, 1] ➔ [1] (passed)</span>
                  </div>
                  <div className="flex items-center gap-2 text-emerald-400">
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>case 4: ["a", "b", "a", "c"] ➔ ["a", "b", "c"] (passed)</span>
                  </div>
                  <div className="flex items-center gap-2 text-emerald-400">
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>case 5: [Hidden 1,000 items benchmark] (passed 2.1ms)</span>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-[11px]">
                <span className="text-purple-300 font-semibold">+35 XP Awarded</span>
                <span className="text-slate-500">Streak Maintained: 3 Days</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* The 6 Disciplines Progression Grid */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="text-2xl sm:text-4xl font-bold text-white tracking-tight">
            The Six Cracked Disciplines
          </h2>
          <p className="mt-3 text-sm text-slate-400">
            A linear progression tree designed to eliminate engineering blind spots. Clear tier by tier.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {tracks.map((track, i) => (
            <Link
              key={track.slug}
              href={`/tracks/${track.slug}`}
              className="group relative rounded-2xl border border-slate-800 bg-[#0e1120] p-6 hover:border-purple-500/50 transition-all hover:shadow-xl hover:shadow-purple-500/10 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-10 h-10 rounded-xl bg-slate-800/80 border border-slate-700/60 flex items-center justify-center group-hover:scale-105 transition">
                    {getTrackIcon(track.slug)}
                  </div>
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">
                    {track.required_xp === 0 ? (
                      <span className="text-emerald-400 font-semibold">Tier 1 • Open</span>
                    ) : (
                      `Req: ${track.required_xp} XP`
                    )}
                  </span>
                </div>

                <div className="text-[11px] font-mono text-purple-400 font-semibold uppercase tracking-wider mb-1">
                  Discipline 0{i + 1}
                </div>
                <h3 className="text-lg font-bold text-white group-hover:text-purple-300 transition">
                  {track.name}
                </h3>
                <p className="mt-2 text-xs text-slate-400 line-clamp-3 leading-relaxed">
                  {track.description || track.tagline}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-800/70 flex items-center justify-between text-xs text-slate-400">
                <span className="font-mono">3 Levels • 12 Challenges</span>
                <span className="flex items-center gap-1 text-purple-400 group-hover:translate-x-1 transition font-medium">
                  Enter Track <ArrowRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Personal Learning Features */}
      <section className="max-w-5xl mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="rounded-2xl border border-slate-800 bg-[#0e1122] p-6">
            <div className="w-10 h-10 rounded-xl bg-purple-950/60 border border-purple-500/30 flex items-center justify-center text-purple-400 mb-4">
              <Archive className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white mb-2">Personal Solution Vault</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Every working solution you submit is automatically archived. Review and compare your implementations anytime as your skills deepen.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-[#0e1122] p-6">
            <div className="w-10 h-10 rounded-xl bg-cyan-950/60 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-4">
              <Terminal className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white mb-2">Automated Code Grading</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Test your code instantly in an isolated sandbox. Receive immediate feedback with full argument inputs, return values, and tracebacks.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-[#0e1122] p-6">
            <div className="w-10 h-10 rounded-xl bg-emerald-950/60 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-4">
              <Sparkles className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white mb-2">Disciplined Progression</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Eliminate software engineering blind spots. Progress steadily from data structures to distributed databases and neural architectures.
            </p>
          </div>
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <section className="max-w-5xl mx-auto px-4 py-20 text-center">
        <div className="relative rounded-3xl border border-purple-500/30 bg-gradient-to-b from-[#14122b] to-[#0d0f1c] p-8 sm:p-12 overflow-hidden shadow-2xl">
          <div className="absolute top-0 right-0 -translate-y-12 translate-x-12 w-64 h-64 bg-purple-500/20 blur-3xl rounded-full pointer-events-none" />

          <h2 className="text-2xl sm:text-4xl font-extrabold text-white">
            Ready to test your limits?
          </h2>
          <p className="mt-3 text-sm text-slate-300 max-w-xl mx-auto">
            Zero setup required. Start right in the browser, write code against real unit tests, and advance your rank from Script Kiddie to Cracked.
          </p>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <Link
              href="/dashboard"
              className="px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs transition shadow-lg shadow-purple-600/30"
            >
              Open Dashboard
            </Link>
            <Link
              href="/tracks"
              className="px-6 py-3 rounded-xl border border-slate-700 bg-slate-800/80 hover:bg-slate-800 text-slate-200 text-xs font-semibold transition"
            >
              Curriculum Roadmap
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
