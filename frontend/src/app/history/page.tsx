"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import { HistoryData, VaultItem } from "@/types";
import {
  Archive,
  Search,
  Code2,
  Calendar,
  Sparkles,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  ArrowRight,
  Copy,
  Check,
  Loader2,
  Terminal,
  BookOpen,
} from "lucide-react";

export default function SolutionVaultPage() {
  const { user } = useAuth();
  const [data, setData] = useState<HistoryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [trackFilter, setTrackFilter] = useState("all");
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [copiedId, setCopiedId] = useState<number | null>(null);

  useEffect(() => {
    api.progress
      .getHistory()
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const handleCopy = (id: number, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
        <span className="text-xs text-slate-400 font-mono">Opening solution vault...</span>
      </div>
    );
  }

  const items = (data?.vault || []).filter((item) => {
    const matchesSearch =
      item.title.toLowerCase().includes(search.toLowerCase()) ||
      item.track_name.toLowerCase().includes(search.toLowerCase());
    const matchesTrack = trackFilter === "all" || item.track_slug === trackFilter;
    return matchesSearch && matchesTrack;
  });

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 mb-8">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-950/60 border border-purple-500/30 text-purple-300 text-xs font-mono font-medium mb-3">
            <Archive className="w-3.5 h-3.5 text-purple-400" />
            <span>Personal Revision Vault</span>
          </div>
          <h1 className="text-2xl sm:text-4xl font-black text-white tracking-tight">
            Saved Solutions & Code Archive
          </h1>
          <p className="mt-1 text-xs sm:text-sm text-slate-400">
            Review your working solutions, code implementations, and revision notes anytime.
          </p>
        </div>

        {/* Quick Stats Pill */}
        <div className="flex items-center gap-3 font-mono text-xs">
          <div className="p-3 rounded-xl bg-[#0e1122] border border-slate-800 text-center">
            <div className="text-purple-400 font-bold text-lg">
              {data?.total_solved || 0}
            </div>
            <div className="text-[10px] text-slate-500">SOLUTIONS SAVED</div>
          </div>
          <div className="p-3 rounded-xl bg-[#0e1122] border border-slate-800 text-center">
            <div className="text-cyan-400 font-bold text-lg">
              {data?.total_attempts || 0}
            </div>
            <div className="text-[10px] text-slate-500">TOTAL ATTEMPTS</div>
          </div>
        </div>
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search saved solutions by title or concept..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[#0e1122] border border-slate-800 text-white text-xs focus:outline-none focus:border-purple-500 transition"
          />
        </div>

        <select
          value={trackFilter}
          onChange={(e) => setTrackFilter(e.target.value)}
          className="px-4 py-2.5 rounded-xl bg-[#0e1122] border border-slate-800 text-white text-xs focus:outline-none focus:border-purple-500 font-mono"
        >
          <option value="all">All Disciplines</option>
          <option value="coding">Coding Foundations</option>
          <option value="algorithms">Algorithms & Data Structures</option>
          <option value="web">Web Development</option>
          <option value="databases">Database Design</option>
          <option value="devops">DevOps & Infrastructure</option>
          <option value="ai">AI Engineering</option>
        </select>
      </div>

      {/* Solutions List */}
      {items.length === 0 ? (
        <div className="text-center py-20 rounded-2xl border border-slate-800 bg-[#0e1122] p-8">
          <Code2 className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <h3 className="text-sm font-bold text-slate-300">No solutions found</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            {search || trackFilter !== "all"
              ? "Try adjusting your search query or discipline filter."
              : "Solve challenges in any track to automatically archive your solutions here."}
          </p>
          <Link
            href="/tracks"
            className="inline-flex items-center gap-2 mt-4 px-4 py-2 rounded-xl bg-purple-600 text-white text-xs font-semibold hover:bg-purple-500 transition"
          >
            <span>Browse Curriculum</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {items.map((item) => {
            const isExpanded = expandedId === item.challenge_id;
            const hasSource = Boolean(item.submission.source);

            return (
              <div
                key={item.challenge_id}
                className="rounded-2xl border border-slate-800 bg-[#0e1122] overflow-hidden shadow-md transition-all hover:border-slate-700"
              >
                {/* Header Row */}
                <div
                  onClick={() => setExpandedId(isExpanded ? null : item.challenge_id)}
                  className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 cursor-pointer hover:bg-slate-800/30 transition"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2 text-[11px] font-mono">
                      <span className="font-semibold text-purple-400">
                        {item.track_name}
                      </span>
                      <span className="text-slate-600">•</span>
                      <span className="text-slate-400">
                        L{item.level_index}: {item.level_title}
                      </span>
                      <span className="text-slate-600">•</span>
                      <span className="text-emerald-400 flex items-center gap-1 font-semibold">
                        <CheckCircle2 className="w-3 h-3" /> Solved
                      </span>
                    </div>

                    <h3 className="text-base font-bold text-white flex items-center gap-2">
                      <span>{item.title}</span>
                    </h3>

                    <div className="flex items-center gap-3 text-[11px] font-mono text-slate-500">
                      <span className="capitalize">{item.kind} challenge</span>
                      <span>•</span>
                      <span>+{item.xp} XP</span>
                      <span>•</span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {new Date(item.solved_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-xs font-mono text-purple-400 font-semibold flex items-center gap-1">
                      {isExpanded ? "Hide Code" : "Inspect Solution"}
                      {isExpanded ? (
                        <ChevronUp className="w-4 h-4" />
                      ) : (
                        <ChevronDown className="w-4 h-4" />
                      )}
                    </span>
                  </div>
                </div>

                {/* Expanded Solution Drawer */}
                {isExpanded && (
                  <div className="px-5 pb-5 pt-2 border-t border-slate-800/80 bg-[#090b14]">
                    {hasSource ? (
                      <div>
                        <div className="flex items-center justify-between py-2 text-xs text-slate-400 font-mono">
                          <span className="flex items-center gap-1.5">
                            <Terminal className="w-3.5 h-3.5 text-cyan-400" />
                            <span>Your Accepted Python Implementation:</span>
                          </span>
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleCopy(item.challenge_id, item.submission.source || "");
                            }}
                            className="flex items-center gap-1 px-2.5 py-1 rounded hover:bg-slate-800 text-slate-300 transition text-[11px]"
                          >
                            {copiedId === item.challenge_id ? (
                              <>
                                <Check className="w-3 h-3 text-emerald-400" />
                                <span className="text-emerald-400">Copied</span>
                              </>
                            ) : (
                              <>
                                <Copy className="w-3 h-3" />
                                <span>Copy Code</span>
                              </>
                            )}
                          </button>
                        </div>
                        <pre className="p-4 rounded-xl border border-slate-800 bg-[#07080f] text-slate-100 font-mono text-xs overflow-x-auto leading-relaxed">
                          <code>{item.submission.source}</code>
                        </pre>
                      </div>
                    ) : (
                      <div className="py-2 text-xs font-mono text-slate-300">
                        <div className="text-slate-500 mb-1">// Submitted Answer:</div>
                        <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
                          {item.submission.text ? (
                            <span>&gt; {item.submission.text}</span>
                          ) : item.submission.choice !== undefined ? (
                            <span>Selected Option #{item.submission.choice + 1}</span>
                          ) : (
                            <span>Selected Options: {JSON.stringify(item.submission.choices)}</span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
