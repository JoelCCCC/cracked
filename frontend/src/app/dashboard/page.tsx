"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import { DashboardData } from "@/types";
import {
  Zap,
  Flame,
  Archive,
  CheckCircle2,
  Lock,
  ArrowRight,
  Sparkles,
  Layers,
  Code2,
  Terminal,
  Database,
  Server,
  Cpu,
  Loader2,
  Play,
  TrendingUp,
} from "lucide-react";

const RANKS = [
  { xp: 0, title: "Script Kiddie" },
  { xp: 250, title: "Junior" },
  { xp: 750, title: "Builder" },
  { xp: 1500, title: "Engineer" },
  { xp: 3000, title: "Senior" },
  { xp: 5000, title: "Architect" },
  { xp: 8000, title: "Cracked" },
];

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
      return;
    }

    if (user) {
      api.progress
        .getDashboard()
        .then((res) => {
          setData(res);
          setLoading(false);
        })
        .catch((err) => {
          console.error(err);
          setLoading(false);
        });
    }
  }, [user, authLoading, router]);

  if (authLoading || loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
        <span className="text-xs text-slate-400 font-mono">Loading telemetry...</span>
      </div>
    );
  }

  if (!data) return null;

  // Calculate next rank progress
  const currentXP = data.user.total_xp;
  let nextRank = RANKS[RANKS.length - 1];
  let currentRankFloor = RANKS[0].xp;

  for (let i = 0; i < RANKS.length; i++) {
    if (currentXP < RANKS[i].xp) {
      nextRank = RANKS[i];
      currentRankFloor = i > 0 ? RANKS[i - 1].xp : 0;
      break;
    }
  }

  const xpInTier = Math.max(0, currentXP - currentRankFloor);
  const xpNeededInTier = Math.max(1, nextRank.xp - currentRankFloor);
  const rankProgressPercent = Math.min(
    100,
    Math.round((xpInTier / xpNeededInTier) * 100)
  );

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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Top Banner: User info & Rank Progress */}
      <div className="rounded-2xl border border-slate-800 bg-[#0e1122] p-6 mb-8 relative overflow-hidden shadow-2xl">
        <div className="absolute top-0 right-0 w-80 h-80 bg-purple-600/10 blur-3xl rounded-full pointer-events-none" />

        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-purple-600 to-cyan-500 flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-purple-600/30">
              {data.user.name.charAt(0).toUpperCase()}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl sm:text-2xl font-black text-white">
                  {data.user.name}
                </h1>
                <span className="px-2.5 py-0.5 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-300 font-mono text-xs font-semibold">
                  {data.user.rank}
                </span>
              </div>
              <div className="flex items-center gap-3 text-xs text-slate-400 mt-1 font-mono">
                <span>@{data.user.username}</span>
                <span>•</span>
                <span className="flex items-center gap-1 text-amber-400 font-semibold">
                  <Flame className="w-3.5 h-3.5 fill-current" />
                  {data.user.current_streak} Day Streak
                </span>
                <span>•</span>
                <span className="flex items-center gap-1 text-purple-300 font-semibold">
                  <Sparkles className="w-3.5 h-3.5" />
                  {data.user.total_xp} Total XP
                </span>
              </div>
            </div>
          </div>

          {/* Rank Meter */}
          <div className="lg:w-80 p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 text-xs">
            <div className="flex items-center justify-between mb-1.5 font-mono">
              <span className="text-slate-400">Next Rank:</span>
              <span className="text-cyan-300 font-bold">{nextRank.title}</span>
            </div>
            <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-purple-500 to-cyan-400 rounded-full transition-all duration-500"
                style={{ width: `${rankProgressPercent}%` }}
              />
            </div>
            <div className="flex items-center justify-between mt-1.5 text-[11px] font-mono text-slate-500">
              <span>{currentXP} XP</span>
              <span>{nextRank.xp} XP ({Math.max(0, nextRank.xp - currentXP)} XP left)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="p-4 rounded-xl bg-[#0f1120] border border-slate-800">
          <div className="text-xs text-slate-400 font-medium">Challenges Solved</div>
          <div className="text-2xl font-bold font-mono text-white mt-1">
            {data.stats.solved}
            <span className="text-xs font-normal text-slate-500 ml-1">
              / {data.stats.total_challenges}
            </span>
          </div>
          <div className="text-[11px] text-purple-400 font-mono mt-1">
            {Math.round((data.stats.solved / Math.max(1, data.stats.total_challenges)) * 100)}% complete
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#0f1120] border border-slate-800">
          <div className="text-xs text-slate-400 font-medium">Levels Cleared</div>
          <div className="text-2xl font-bold font-mono text-white mt-1">
            {data.stats.levels_completed}
            <span className="text-xs font-normal text-slate-500 ml-1">
              / {data.stats.total_levels}
            </span>
          </div>
          <div className="text-[11px] text-cyan-400 font-mono mt-1">
            18 levels across 6 tracks
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#0f1120] border border-slate-800">
          <div className="text-xs text-slate-400 font-medium">Attempt Accuracy</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
            {data.stats.accuracy}%
          </div>
          <div className="text-[11px] text-slate-500 font-mono mt-1">
            {data.stats.attempts} total attempts
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#0f1120] border border-slate-800">
          <div className="text-xs text-slate-400 font-medium">Longest Streak</div>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-1 flex items-center gap-1">
            <Flame className="w-5 h-5 fill-current" />
            {data.user.longest_streak}d
          </div>
          <div className="text-[11px] text-slate-500 font-mono mt-1">
            Keep coding daily!
          </div>
        </div>
      </div>

      {/* Recommended Next Quest Card */}
      {data.next_level && (
        <div className="mb-10 rounded-2xl border border-purple-500/40 bg-gradient-to-r from-purple-950/40 via-[#101222] to-[#0d0f1c] p-6 shadow-xl relative overflow-hidden">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 text-xs font-mono text-purple-400 uppercase tracking-wider mb-1">
                <TrendingUp className="w-3.5 h-3.5" />
                <span>Next Recommended Quest</span>
              </div>
              <h2 className="text-xl font-bold text-white">
                {data.next_level.track_name}: Level {data.next_level.index} - {data.next_level.title}
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Pick up where you left off to earn bonus XP and unlock subsequent levels.
              </p>
            </div>

            <Link
              href={`/levels/${data.next_level.id}`}
              className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs transition shadow-lg shadow-purple-600/30 whitespace-nowrap"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>Launch Level {data.next_level.index}</span>
            </Link>
          </div>
        </div>
      )}

      {/* The 6 Disciplines Progression Grid */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-purple-400" />
            <span>Curriculum Progression Matrix</span>
          </h2>
          <div className="flex items-center gap-3">
            <Link
              href="/history"
              className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1"
            >
              <Archive className="w-3.5 h-3.5" />
              <span>Solution Vault</span>
            </Link>
            <span className="text-slate-700">•</span>
            <Link
              href="/tracks"
              className="text-xs text-purple-400 hover:text-purple-300 font-semibold flex items-center gap-1"
            >
              <span>View Full Map</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {data.tracks.map((track) => {
            const isUnlocked = track.unlocked;
            const isDone = track.completed;

            return (
              <div
                key={track.slug}
                className={`rounded-2xl border p-5 flex flex-col justify-between transition-all ${
                  isUnlocked
                    ? "bg-[#0e1120] border-slate-800 hover:border-purple-500/50 hover:shadow-lg"
                    : "bg-[#090b14]/70 border-slate-800/50 opacity-70"
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div className="w-9 h-9 rounded-xl bg-slate-800/80 border border-slate-700/60 flex items-center justify-center">
                      {getTrackIcon(track.slug)}
                    </div>
                    {isDone ? (
                      <span className="px-2 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-[11px] font-mono font-semibold flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" />
                        Completed
                      </span>
                    ) : isUnlocked ? (
                      <span className="px-2 py-0.5 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-300 text-[11px] font-mono font-semibold">
                        Unlocked
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded-full bg-slate-800 border border-slate-700 text-slate-400 text-[11px] font-mono flex items-center gap-1">
                        <Lock className="w-3 h-3" />
                        {track.required_xp} XP needed
                      </span>
                    )}
                  </div>

                  <h3 className="text-base font-bold text-white">{track.name}</h3>
                  <p className="text-xs text-slate-400 mt-1 line-clamp-2">
                    {track.description || track.tagline}
                  </p>
                </div>

                <div className="mt-5 pt-3 border-t border-slate-800/80">
                  {/* Progress bar */}
                  <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 mb-1.5">
                    <span>
                      {track.solved_count || 0} / {track.challenge_count || 12} solved
                    </span>
                    <span>
                      {Math.round(
                        ((track.solved_count || 0) /
                          Math.max(1, track.challenge_count || 12)) *
                          100
                      )}
                      %
                    </span>
                  </div>
                  <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden mb-3">
                    <div
                      className="h-full bg-gradient-to-r from-purple-500 to-cyan-400 rounded-full"
                      style={{
                        width: `${Math.min(
                          100,
                          Math.round(
                            ((track.solved_count || 0) /
                              Math.max(1, track.challenge_count || 12)) *
                              100
                          )
                        )}%`,
                      }}
                    />
                  </div>

                  {isUnlocked ? (
                    <Link
                      href={`/tracks/${track.slug}`}
                      className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center justify-center gap-1.5 transition"
                    >
                      <span>Open Track Levels</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  ) : (
                    <div className="w-full py-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-500 text-xs font-mono text-center">
                      Locked • Earn {track.xp_to_unlock} more XP
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Solves Feed */}
      {data.recent_solves && data.recent_solves.length > 0 && (
        <div>
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <span>Recent Activity</span>
          </h2>
          <div className="rounded-2xl border border-slate-800 bg-[#0e1120] divide-y divide-slate-800/70 overflow-hidden text-xs">
            {data.recent_solves.map((solve, i) => (
              <div
                key={i}
                className="flex items-center justify-between px-5 py-3 hover:bg-slate-800/30 transition"
              >
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-emerald-400" />
                  <div>
                    <div className="font-semibold text-slate-200">{solve.title}</div>
                    <div className="text-[11px] text-slate-500 font-mono">
                      {solve.track}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3 font-mono">
                  <span className="text-emerald-400 font-semibold">+{solve.xp} XP</span>
                  <span className="text-slate-500 text-[11px]">
                    {new Date(solve.solved_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
