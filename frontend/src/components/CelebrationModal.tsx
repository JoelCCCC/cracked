"use client";

import React, { useEffect } from "react";
import confetti from "canvas-confetti";
import { Award, Flame, Sparkles, CheckCircle2, ArrowRight } from "lucide-react";
import { SubmitResult } from "@/types";

interface CelebrationModalProps {
  result: SubmitResult | null;
  onClose: () => void;
  onNext?: () => void;
  hasNext?: boolean;
}

export function triggerConfetti() {
  confetti({
    particleCount: 80,
    spread: 70,
    origin: { y: 0.6 },
    colors: ["#7c5cff", "#00e5ff", "#10b981", "#f59e0b", "#ec4899"],
  });
}

export function CelebrationModal({
  result,
  onClose,
  onNext,
  hasNext,
}: CelebrationModalProps) {
  useEffect(() => {
    if (result && result.correct) {
      triggerConfetti();
    }
  }, [result]);

  if (!result || !result.correct) return null;

  const isLevelCleared = result.level_completed;
  const isTrackCleared = result.track_completed;
  const rankEvent = result.events.find((e) => e.type === "rank");
  const trackUnlockedEvent = result.events.find((e) => e.type === "track_unlocked");

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-md rounded-2xl border border-purple-500/40 bg-[#0f1224] p-6 shadow-2xl text-center glow-purple">
        {/* Glow orb */}
        <div className="absolute -top-12 left-1/2 -translate-x-1/2 w-24 h-24 rounded-full bg-purple-500/20 blur-2xl pointer-events-none" />

        {/* Icon */}
        <div className="mx-auto w-16 h-16 rounded-2xl bg-gradient-to-tr from-purple-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-purple-500/30 mb-4 animate-bounce">
          {isLevelCleared ? (
            <Award className="w-9 h-9 text-white" />
          ) : (
            <CheckCircle2 className="w-9 h-9 text-white" />
          )}
        </div>

        {/* Title */}
        <h3 className="text-xl font-bold text-white tracking-wide">
          {isTrackCleared
            ? "Track Mastered!"
            : isLevelCleared
            ? "Level Cleared!"
            : "Challenge Solved!"}
        </h3>

        <p className="mt-1 text-xs text-slate-300">
          {result.already_solved
            ? "Already solved previously. No extra XP awarded."
            : `You earned +${result.xp_awarded} XP!`}
        </p>

        {/* Badges / Events */}
        <div className="mt-4 flex flex-col gap-2">
          {rankEvent && (
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-purple-950/60 border border-purple-500/50 text-xs text-purple-200">
              <span className="flex items-center gap-1.5 font-semibold">
                <Sparkles className="w-4 h-4 text-purple-400" />
                Rank Up!
              </span>
              <span className="px-2 py-0.5 rounded bg-purple-500/30 font-mono font-bold text-purple-100">
                {rankEvent.label}
              </span>
            </div>
          )}

          {trackUnlockedEvent && (
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-cyan-950/60 border border-cyan-500/50 text-xs text-cyan-200">
              <span className="flex items-center gap-1.5 font-semibold">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                New Discipline Unlocked!
              </span>
              <span className="font-semibold text-cyan-300">
                {trackUnlockedEvent.label}
              </span>
            </div>
          )}

          <div className="grid grid-cols-2 gap-2 mt-1">
            <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs flex items-center justify-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-purple-400" />
              <span className="text-slate-400">Total XP:</span>
              <span className="font-mono font-bold text-white">{result.total_xp}</span>
            </div>

            <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs flex items-center justify-center gap-1.5">
              <Flame className="w-3.5 h-3.5 text-amber-400" />
              <span className="text-slate-400">Streak:</span>
              <span className="font-mono font-bold text-amber-300">{result.streak}d</span>
            </div>
          </div>
        </div>

        {/* Explanation if any */}
        {result.explanation && (
          <div className="mt-4 p-3 rounded-lg bg-slate-950/90 border border-slate-800/80 text-left text-xs text-slate-300">
            <div className="font-semibold text-purple-400 mb-1 flex items-center gap-1">
              <span>Why this works</span>
            </div>
            <p className="text-slate-300 leading-relaxed">{result.explanation}</p>
          </div>
        )}

        {/* Action buttons */}
        <div className="mt-6 flex items-center justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded-lg border border-slate-700 bg-slate-800/60 hover:bg-slate-800 text-slate-300 hover:text-white text-xs font-medium transition cursor-pointer"
          >
            Review Solution
          </button>

          {hasNext && onNext ? (
            <button
              type="button"
              onClick={() => {
                onClose();
                onNext();
              }}
              className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-medium transition shadow-lg shadow-purple-600/25 cursor-pointer"
            >
              <span>Next Challenge</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-medium transition shadow-lg shadow-purple-600/25 cursor-pointer"
            >
              Continue
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
