"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import { TrackSummary } from "@/types";
import {
  Zap,
  Lock,
  CheckCircle2,
  ArrowRight,
  Code2,
  Layers,
  Terminal,
  Database,
  Server,
  Cpu,
  Loader2,
  Sparkles,
} from "lucide-react";

export default function TracksRoadmapPage() {
  const { user } = useAuth();
  const [tracks, setTracks] = useState<TrackSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetcher = user ? api.curriculum.getTracks() : api.curriculum.getPublicTracks();
    fetcher
      .then((res) => {
        setTracks(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [user]);

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

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
        <span className="text-xs text-slate-400 font-mono">Loading curriculum roadmap...</span>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto mb-14">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-950/60 border border-purple-500/30 text-purple-300 text-xs font-mono font-medium mb-4">
          <Sparkles className="w-3.5 h-3.5 text-purple-400" />
          <span>Curriculum Skill Tree</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight">
          The Engineering Progression
        </h1>
        <p className="mt-3 text-sm sm:text-base text-slate-400 leading-relaxed">
          Master computer science and modern software engineering in sequential order. Each track unlocks as your total XP crosses key milestones.
        </p>
      </div>

      {/* Tracks Progression Timeline */}
      <div className="relative space-y-8 before:absolute before:inset-0 before:left-7 md:before:left-1/2 before:-translate-x-px before:w-0.5 before:bg-gradient-to-b before:from-purple-500 before:via-cyan-500 before:to-slate-800 before:z-0">
        {tracks.map((track, index) => {
          const isUnlocked = track.unlocked !== undefined ? track.unlocked : track.required_xp === 0;
          const isCompleted = track.completed;
          const isEven = index % 2 === 0;

          return (
            <div
              key={track.slug}
              className={`relative z-10 flex flex-col md:flex-row items-center gap-6 ${
                isEven ? "md:flex-row-reverse" : ""
              }`}
            >
              {/* Card Container */}
              <div className="w-full md:w-[calc(50%-2rem)] pl-16 md:pl-0">
                <div
                  className={`rounded-2xl border p-6 transition-all ${
                    isUnlocked
                      ? "bg-[#0e1122] border-slate-800 hover:border-purple-500/60 hover:shadow-xl hover:shadow-purple-500/10"
                      : "bg-[#090b14]/70 border-slate-800/40 opacity-75"
                  }`}
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-purple-400">
                      Tier 0{index + 1}
                    </span>
                    {isCompleted ? (
                      <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-semibold flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        Mastered
                      </span>
                    ) : isUnlocked ? (
                      <span className="px-2.5 py-0.5 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-300 text-xs font-mono font-semibold">
                        Available
                      </span>
                    ) : (
                      <span className="px-2.5 py-0.5 rounded-full bg-slate-900 border border-slate-800 text-slate-400 text-xs font-mono flex items-center gap-1">
                        <Lock className="w-3 h-3" />
                        Req: {track.required_xp} XP
                      </span>
                    )}
                  </div>

                  <h3 className="text-xl font-bold text-white mb-1.5">{track.name}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed mb-4">
                    {track.description || track.tagline}
                  </p>

                  {/* Level pills preview */}
                  {track.levels && (
                    <div className="space-y-1.5 mb-5">
                      {track.levels.map((lvl) => (
                        <div
                          key={lvl.id}
                          className="flex items-center justify-between p-2 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs"
                        >
                          <div className="flex items-center gap-2">
                            {lvl.completed ? (
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                            ) : lvl.unlocked ? (
                              <div className="w-2 h-2 rounded-full bg-purple-400 shrink-0" />
                            ) : (
                              <Lock className="w-3 h-3 text-slate-600 shrink-0" />
                            )}
                            <span className={lvl.unlocked ? "text-slate-200" : "text-slate-500"}>
                              L{lvl.index}: {lvl.title}
                            </span>
                          </div>
                          <span className="font-mono text-[11px] text-purple-400 shrink-0">
                            +{lvl.xp_reward} XP
                          </span>
                        </div>
                      ))}
                    </div>
                  )}

                  {isUnlocked ? (
                    <Link
                      href={`/tracks/${track.slug}`}
                      className="inline-flex items-center justify-center gap-2 w-full py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold transition shadow-md shadow-purple-600/20"
                    >
                      <span>Explore Track Levels</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  ) : (
                    <div className="text-center py-2 rounded-xl bg-slate-900 border border-slate-800/80 text-xs font-mono text-slate-500">
                      Requires {track.required_xp} Total XP to unlock
                    </div>
                  )}
                </div>
              </div>

              {/* Center Timeline Node */}
              <div
                className={`absolute left-7 md:left-1/2 -translate-x-1/2 w-12 h-12 rounded-2xl border-2 flex items-center justify-center shadow-lg transition-transform ${
                  isCompleted
                    ? "bg-emerald-950 border-emerald-500 text-emerald-400"
                    : isUnlocked
                    ? "bg-[#121528] border-purple-500 text-purple-300 shadow-purple-500/20"
                    : "bg-[#090b14] border-slate-800 text-slate-600"
                }`}
              >
                {getTrackIcon(track.slug)}
              </div>

              {/* Spacer for other side */}
              <div className="hidden md:block w-full md:w-[calc(50%-2rem)]" />
            </div>
          );
        })}
      </div>
    </div>
  );
}
