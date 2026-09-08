"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import { TrackSummary } from "@/types";
import {
  Zap,
  Lock,
  CheckCircle2,
  Play,
  ArrowLeft,
  Sparkles,
  Loader2,
  Code2,
  Layers,
  Terminal,
  Database,
  Server,
  Cpu,
} from "lucide-react";

export default function TrackDetailPage() {
  const params = useParams();
  const router = useRouter();
  const slug = params.slug as string;
  const { user } = useAuth();
  const [track, setTrack] = useState<TrackSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      // If not logged in, fetch public list and find this track
      api.curriculum
        .getPublicTracks()
        .then((tracks) => {
          const found = tracks.find((t) => t.slug === slug);
          if (found) setTrack(found);
          setLoading(false);
        })
        .catch(() => setLoading(false));
      return;
    }

    api.curriculum
      .getTrack(slug)
      .then((res) => {
        setTrack(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [slug, user]);

  const getTrackIcon = (slug: string) => {
    switch (slug) {
      case "coding":
        return <Code2 className="w-6 h-6 text-purple-400" />;
      case "algorithms":
        return <Layers className="w-6 h-6 text-cyan-400" />;
      case "web":
        return <Terminal className="w-6 h-6 text-emerald-400" />;
      case "databases":
        return <Database className="w-6 h-6 text-amber-400" />;
      case "devops":
        return <Server className="w-6 h-6 text-rose-400" />;
      case "ai":
        return <Cpu className="w-6 h-6 text-fuchsia-400" />;
      default:
        return <Zap className="w-6 h-6 text-purple-400" />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
        <span className="text-xs text-slate-400 font-mono">Loading discipline details...</span>
      </div>
    );
  }

  if (!track) {
    return (
      <div className="max-w-md mx-auto py-20 text-center text-xs">
        <div className="text-lg font-bold text-white mb-2">Track Not Found</div>
        <Link href="/tracks" className="text-purple-400 hover:underline">
          Return to roadmap
        </Link>
      </div>
    );
  }

  const isUnlocked = track.unlocked !== undefined ? track.unlocked : track.required_xp === 0;

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Back link */}
      <Link
        href="/tracks"
        className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition mb-6"
      >
        <ArrowLeft className="w-3.5 h-3.5" />
        <span>Back to Curriculum Roadmap</span>
      </Link>

      {/* Track Header Card */}
      <div className="rounded-2xl border border-slate-800 bg-[#0e1122] p-6 sm:p-8 mb-10 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-80 h-80 bg-purple-600/10 blur-3xl rounded-full pointer-events-none" />

        <div className="flex flex-col sm:flex-row sm:items-center gap-5 relative z-10">
          <div className="w-14 h-14 rounded-2xl bg-slate-800/90 border border-slate-700/80 flex items-center justify-center shrink-0 shadow-lg">
            {getTrackIcon(track.slug)}
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1.5">
              <span className="text-xs font-mono font-bold text-purple-400 uppercase tracking-wider">
                Discipline
              </span>
              {track.completed ? (
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-semibold flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Track Complete
                </span>
              ) : isUnlocked ? (
                <span className="px-2.5 py-0.5 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-300 text-xs font-mono font-semibold">
                  Active
                </span>
              ) : (
                <span className="px-2.5 py-0.5 rounded-full bg-slate-900 border border-slate-800 text-slate-400 text-xs font-mono flex items-center gap-1">
                  <Lock className="w-3 h-3" />
                  Locked • {track.required_xp} XP Required
                </span>
              )}
            </div>

            <h1 className="text-2xl sm:text-3xl font-black text-white">{track.name}</h1>
            <p className="mt-2 text-xs sm:text-sm text-slate-300 leading-relaxed max-w-2xl">
              {track.description || track.tagline}
            </p>
          </div>
        </div>

        {/* Progress summary bar */}
        {track.levels && (
          <div className="mt-6 pt-5 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-4 text-xs font-mono text-slate-400">
            <div className="flex items-center gap-4">
              <span>Levels: {track.levels_completed || 0} / {track.level_count || track.levels.length} Cleared</span>
              <span>•</span>
              <span>Challenges: {track.solved_count || 0} / {track.challenge_count || 12} Solved</span>
            </div>
            {track.required_xp > 0 && (
              <span className="text-slate-500">Unlocks at {track.required_xp} Total XP</span>
            )}
          </div>
        )}
      </div>

      {/* Levels list */}
      <div className="space-y-6">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>Sequential Level Progression</span>
        </h2>

        <div className="grid grid-cols-1 gap-4">
          {track.levels ? (
            track.levels.map((lvl) => {
              const isLvlDone = lvl.completed;
              const isLvlUnlocked = lvl.unlocked;

              return (
                <div
                  key={lvl.id}
                  className={`rounded-2xl border p-6 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-6 ${
                    isLvlDone
                      ? "bg-[#0c1322] border-emerald-500/30"
                      : isLvlUnlocked
                      ? "bg-[#0e1122] border-slate-800 hover:border-purple-500/50 shadow-md"
                      : "bg-[#090a14]/60 border-slate-800/40 opacity-70"
                  }`}
                >
                  <div className="space-y-1.5 max-w-xl">
                    <div className="flex items-center gap-2 text-xs font-mono">
                      <span className="font-bold text-purple-400">LEVEL 0{lvl.index}</span>
                      <span>•</span>
                      <span className="flex items-center gap-1 text-purple-300">
                        <Sparkles className="w-3 h-3 text-purple-400" />
                        +{lvl.xp_reward} Bonus XP
                      </span>
                    </div>

                    <h3 className="text-lg font-bold text-white">{lvl.title}</h3>
                    <p className="text-xs text-slate-400 leading-relaxed">{lvl.summary}</p>

                    <div className="pt-2 flex items-center gap-4 text-[11px] font-mono text-slate-500">
                      <span>
                        Challenges: {lvl.solved_count} / {lvl.challenge_count} solved
                      </span>
                    </div>
                  </div>

                  <div className="shrink-0 flex items-center">
                    {isLvlDone ? (
                      <Link
                        href={`/levels/${lvl.id}`}
                        className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-emerald-950/60 border border-emerald-500/40 text-emerald-300 hover:bg-emerald-950 text-xs font-semibold transition"
                      >
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        <span>Completed (Review)</span>
                      </Link>
                    ) : isLvlUnlocked ? (
                      <Link
                        href={`/levels/${lvl.id}`}
                        className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold transition shadow-lg shadow-purple-600/30"
                      >
                        <Play className="w-3.5 h-3.5 fill-current" />
                        <span>Enter Level {lvl.index}</span>
                      </Link>
                    ) : (
                      <div className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-500 text-xs font-mono">
                        <Lock className="w-3.5 h-3.5" />
                        <span>Complete Level {lvl.index - 1} First</span>
                      </div>
                    )}
                  </div>
                </div>
              );
            })
          ) : (
            <div className="text-center py-10 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-400">
              Please sign in to view and play levels for this track.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
