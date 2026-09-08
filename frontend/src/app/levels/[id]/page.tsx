"use client";

import React, { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import { LevelDetail, Challenge, SubmitResult } from "@/types";
import { MarkdownRenderer } from "@/components/MarkdownRenderer";
import { CodeEditor } from "@/components/CodeEditor";
import { CelebrationModal, triggerConfetti } from "@/components/CelebrationModal";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  HelpCircle,
  Sparkles,
  Loader2,
  RotateCcw,
  AlertCircle,
  Play,
  Award,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

export default function LevelArenaPage() {
  const params = useParams();
  const router = useRouter();
  const levelId = Number(params.id);
  const { user, refreshUser } = useAuth();

  const [level, setLevel] = useState<LevelDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Selected challenge index
  const [activeChallengeIdx, setActiveChallengeIdx] = useState(0);

  // Lessons accordion open state
  const [showLessons, setShowLessons] = useState(true);
  const [activeLessonIdx, setActiveLessonIdx] = useState(0);

  // Hint open state
  const [showHint, setShowHint] = useState(false);

  // Challenge submission state
  const [codeSource, setCodeSource] = useState("");
  const [selectedMcq, setSelectedMcq] = useState<number | null>(null);
  const [selectedMulti, setSelectedMulti] = useState<number[]>([]);
  const [shortText, setShortText] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // Results state
  const [lastResult, setLastResult] = useState<SubmitResult | null>(null);
  const [showCelebration, setShowCelebration] = useState(false);

  const loadLevel = useCallback(async () => {
    try {
      const res = await api.curriculum.getLevel(levelId);
      setLevel(res);

      // Find first unsolved challenge, or default to 0
      const firstUnsolved = res.challenges.findIndex((c) => !c.solved);
      const initialIdx = firstUnsolved !== -1 ? firstUnsolved : 0;
      setActiveChallengeIdx(initialIdx);

      // Setup initial challenge state
      const initialCh = res.challenges[initialIdx];
      if (initialCh) {
        if (initialCh.kind === "code") {
          setCodeSource(initialCh.config.starter || "");
        }
      }
    } catch (err: any) {
      if (err.status === 403) {
        setError("This level is locked. You must complete the previous level first.");
      } else {
        setError(err.message || "Failed to load level.");
      }
    } finally {
      setLoading(false);
    }
  }, [levelId]);

  useEffect(() => {
    loadLevel();
  }, [loadLevel]);

  // When changing challenge, update editor/input state
  const handleSelectChallenge = (idx: number) => {
    if (!level) return;
    setActiveChallengeIdx(idx);
    setShowHint(false);
    setLastResult(null);

    const ch = level.challenges[idx];
    if (ch) {
      if (ch.kind === "code") {
        setCodeSource(ch.config.starter || "");
      } else if (ch.kind === "mcq") {
        setSelectedMcq(null);
      } else if (ch.kind === "multi") {
        setSelectedMulti([]);
      } else if (ch.kind === "short") {
        setShortText("");
      }
    }
  };

  const handleResetCode = () => {
    if (!level) return;
    const ch = level.challenges[activeChallengeIdx];
    if (ch && ch.kind === "code") {
      setCodeSource(ch.config.starter || "");
    }
  };

  const handleSubmit = async () => {
    if (!level) return;
    const ch = level.challenges[activeChallengeIdx];
    if (!ch) return;

    let payload: Record<string, unknown> = {};
    if (ch.kind === "code") {
      if (!codeSource.trim()) return;
      payload = { source: codeSource };
    } else if (ch.kind === "mcq") {
      if (selectedMcq === null) return;
      payload = { choice: selectedMcq };
    } else if (ch.kind === "multi") {
      if (selectedMulti.length === 0) return;
      payload = { choices: selectedMulti };
    } else if (ch.kind === "short") {
      if (!shortText.trim()) return;
      payload = { text: shortText };
    }

    setSubmitting(true);
    try {
      const res = await api.progress.submitChallenge(ch.id, payload);
      setLastResult(res);

      if (res.correct) {
        // Mark as solved locally
        setLevel((prev) => {
          if (!prev) return prev;
          const nextChallenges = [...prev.challenges];
          nextChallenges[activeChallengeIdx] = {
            ...nextChallenges[activeChallengeIdx],
            solved: true,
          };
          return { ...prev, challenges: nextChallenges };
        });

        // Update auth state (XP, streak, rank)
        refreshUser();

        // Show celebration
        setShowCelebration(true);
      }
    } catch (err: any) {
      setLastResult({
        correct: false,
        detail: { error: err.message || "Submission failed" },
        xp_awarded: 0,
        total_xp: user?.total_xp || 0,
        rank: user?.rank || "Script Kiddie",
        streak: user?.current_streak || 0,
        already_solved: false,
        level_completed: false,
        track_completed: false,
        events: [],
      });
    } finally {
      setSubmitting(false);
    }
  };

  const handleResetLevel = async () => {
    if (!level) return;
    if (!window.confirm(`Reset practice progress for Level ${level.index}?`)) return;
    try {
      await api.progress.resetLevel(levelId);
      await loadLevel();
      await refreshUser();
    } catch (err: any) {
      alert(err.message || "Failed to reset level");
    }
  };

  if (loading) {
    return (
      <div className="min-h-[75vh] flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
        <span className="text-xs text-slate-400 font-mono">Entering arena...</span>
      </div>
    );
  }

  if (error || !level) {
    return (
      <div className="max-w-md mx-auto py-20 px-4 text-center">
        <div className="w-12 h-12 rounded-2xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400 mx-auto mb-4">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-white mb-2">Access Denied</h2>
        <p className="text-xs text-slate-400 mb-6 leading-relaxed">
          {error || "Level could not be loaded."}
        </p>
        <Link
          href="/tracks"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to Curriculum Roadmap</span>
        </Link>
      </div>
    );
  }

  const currentChallenge = level.challenges[activeChallengeIdx];
  const solvedCount = level.challenges.filter((c) => c.solved).length;
  const isLevelComplete = solvedCount === level.challenges.length;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Top Breadcrumb & Progress Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-800/80">
        <div className="flex items-center gap-2 text-xs font-mono">
          <Link
            href={`/tracks/${level.track.slug}`}
            className="text-slate-400 hover:text-white flex items-center gap-1 transition"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>{level.track.name}</span>
          </Link>
          <span className="text-slate-600">/</span>
          <span className="text-purple-400 font-bold">
            Level 0{level.index}: {level.title}
          </span>
        </div>

        <div className="flex items-center gap-4">
          {/* Progress gauge */}
          <div className="flex items-center gap-2 text-xs font-mono">
            <span className="text-slate-400">Progress:</span>
            <span className="text-white font-bold">
              {solvedCount} / {level.challenges.length}
            </span>
            <div className="w-24 h-2 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-purple-500 to-emerald-400 rounded-full transition-all"
                style={{
                  width: `${Math.round(
                    (solvedCount / Math.max(1, level.challenges.length)) * 100
                  )}%`,
                }}
              />
            </div>
          </div>

          <div className="px-2.5 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-mono flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-purple-400" />
            <span>+{level.xp_reward} XP Level Bonus</span>
          </div>

          {solvedCount > 0 && (
            <button
              type="button"
              onClick={handleResetLevel}
              title="Reset solved state in this level to practice again"
              className="flex items-center gap-1 px-2.5 py-1 rounded-lg border border-slate-800 hover:border-slate-700 bg-slate-900/60 text-slate-400 hover:text-slate-200 text-xs font-mono transition cursor-pointer"
            >
              <RotateCcw className="w-3 h-3" />
              <span>Reset Practice</span>
            </button>
          )}
        </div>
      </div>

      {/* Main Split Grid: Left = Knowledge & Prompt, Right = Submission Arena */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column (5 cols): Lessons Drawer & Challenge Prompt */}
        <div className="lg:col-span-5 space-y-5">
          {/* Lessons Accordion Card */}
          {level.lessons && level.lessons.length > 0 && (
            <div className="rounded-2xl border border-slate-800 bg-[#0e1122] overflow-hidden shadow-lg">
              <button
                type="button"
                onClick={() => setShowLessons(!showLessons)}
                className="w-full flex items-center justify-between px-5 py-3.5 bg-slate-900/60 hover:bg-slate-900 transition text-left cursor-pointer border-b border-slate-800/80"
              >
                <div className="flex items-center gap-2 text-xs font-bold text-slate-200">
                  <BookOpen className="w-4 h-4 text-purple-400" />
                  <span>Theory & Concepts ({level.lessons.length} Lessons)</span>
                </div>
                {showLessons ? (
                  <ChevronUp className="w-4 h-4 text-slate-400" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-slate-400" />
                )}
              </button>

              {showLessons && (
                <div className="p-5">
                  {/* Lesson tabs */}
                  {level.lessons.length > 1 && (
                    <div className="flex gap-2 mb-4 overflow-x-auto pb-1">
                      {level.lessons.map((lesson, idx) => (
                        <button
                          key={lesson.id}
                          type="button"
                          onClick={() => setActiveLessonIdx(idx)}
                          className={`px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition cursor-pointer ${
                            activeLessonIdx === idx
                              ? "bg-purple-600 text-white shadow-sm"
                              : "bg-slate-800/70 text-slate-400 hover:text-white"
                          }`}
                        >
                          {lesson.title}
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Active Lesson Content */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-bold text-sm text-white">
                        {level.lessons[activeLessonIdx].title}
                      </h4>
                      <span className="text-[11px] font-mono text-slate-500">
                        {level.lessons[activeLessonIdx].minutes} min read
                      </span>
                    </div>
                    <div className="max-h-[360px] overflow-y-auto pr-2">
                      <MarkdownRenderer
                        content={level.lessons[activeLessonIdx].body}
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Challenges Selector Tabs */}
          <div className="rounded-2xl border border-slate-800 bg-[#0e1122] p-5 shadow-lg">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400">
                Challenges in Level {level.index}
              </span>
              <span className="text-xs font-mono text-purple-400">
                {activeChallengeIdx + 1} of {level.challenges.length}
              </span>
            </div>

            <div className="grid grid-cols-4 gap-2 mb-5">
              {level.challenges.map((ch, idx) => (
                <button
                  key={ch.id}
                  type="button"
                  onClick={() => handleSelectChallenge(idx)}
                  className={`flex flex-col items-center justify-center p-2.5 rounded-xl border text-xs font-mono font-medium transition cursor-pointer ${
                    activeChallengeIdx === idx
                      ? "border-purple-500 bg-purple-950/40 text-purple-200 shadow-md shadow-purple-500/20"
                      : ch.solved
                      ? "border-emerald-500/40 bg-emerald-950/20 text-emerald-300"
                      : "border-slate-800 bg-slate-900/60 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  <div className="flex items-center gap-1">
                    <span>Q{idx + 1}</span>
                    {ch.solved && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                  </div>
                  <span className="text-[10px] text-slate-500 uppercase mt-0.5">
                    {ch.kind}
                  </span>
                </button>
              ))}
            </div>

            {/* Current Challenge Prompt */}
            {currentChallenge && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-mono uppercase font-bold ${
                        currentChallenge.difficulty === "easy"
                          ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30"
                          : currentChallenge.difficulty === "medium"
                          ? "bg-amber-500/15 text-amber-400 border border-amber-500/30"
                          : "bg-rose-500/15 text-rose-400 border border-rose-500/30"
                      }`}
                    >
                      {currentChallenge.difficulty}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-[10px] font-mono text-slate-300 uppercase">
                      {currentChallenge.kind}
                    </span>
                  </div>

                  <span className="text-xs font-mono text-purple-300 font-bold">
                    +{currentChallenge.xp} XP
                  </span>
                </div>

                <h3 className="text-base font-bold text-white leading-snug">
                  {currentChallenge.title}
                </h3>

                <div className="rounded-xl bg-slate-950/60 border border-slate-800/80 p-4">
                  <MarkdownRenderer content={currentChallenge.prompt} />
                </div>

                {/* Hint accordion */}
                {currentChallenge.hint && (
                  <div className="rounded-xl border border-slate-800 bg-slate-950/40 overflow-hidden">
                    <button
                      type="button"
                      onClick={() => setShowHint(!showHint)}
                      className="w-full flex items-center justify-between px-3.5 py-2.5 text-xs text-slate-400 hover:text-slate-200 transition cursor-pointer"
                    >
                      <div className="flex items-center gap-1.5 font-medium">
                        <HelpCircle className="w-3.5 h-3.5 text-amber-400" />
                        <span>Need a hint?</span>
                      </div>
                      <span className="text-[11px] font-mono text-purple-400">
                        {showHint ? "Hide hint" : "Reveal hint"}
                      </span>
                    </button>
                    {showHint && (
                      <div className="px-3.5 py-3 border-t border-slate-800 text-xs text-slate-300 bg-slate-900/40">
                        {currentChallenge.hint}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Column (7 cols): Challenge Solver Arena */}
        <div className="lg:col-span-7 space-y-5">
          {currentChallenge && (
            <div className="rounded-2xl border border-slate-800 bg-[#0e1122] p-5 shadow-2xl">
              {/* Challenge Kind Renderer */}
              {currentChallenge.kind === "code" && (
                <div className="space-y-4">
                  <CodeEditor
                    value={codeSource}
                    onChange={setCodeSource}
                    onSubmit={handleSubmit}
                    onReset={handleResetCode}
                    submitting={submitting}
                    language={currentChallenge.config.language || "python"}
                  />
                </div>
              )}

              {currentChallenge.kind === "mcq" && (
                <div className="space-y-4">
                  <div className="text-xs font-mono text-slate-400 uppercase tracking-wider mb-2">
                    Select the single correct answer:
                  </div>

                  <div className="space-y-2.5">
                    {(currentChallenge.config.options || []).map((opt, i) => (
                      <button
                        key={i}
                        type="button"
                        onClick={() => setSelectedMcq(i)}
                        className={`w-full text-left p-4 rounded-xl border transition-all cursor-pointer flex items-center gap-3 text-xs leading-relaxed ${
                          selectedMcq === i
                            ? "bg-purple-950/50 border-purple-500 text-white shadow-md shadow-purple-500/20"
                            : "bg-slate-950/60 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white"
                        }`}
                      >
                        <span
                          className={`w-6 h-6 rounded-lg font-mono text-xs flex items-center justify-center font-bold shrink-0 ${
                            selectedMcq === i
                              ? "bg-purple-600 text-white"
                              : "bg-slate-800 text-slate-400"
                          }`}
                        >
                          {String.fromCharCode(65 + i)}
                        </span>
                        <span>{opt}</span>
                      </button>
                    ))}
                  </div>

                  <div className="pt-3 flex justify-end">
                    <button
                      type="button"
                      disabled={submitting || selectedMcq === null}
                      onClick={handleSubmit}
                      className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold transition disabled:opacity-50 cursor-pointer shadow-lg shadow-purple-600/30"
                    >
                      {submitting ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <Play className="w-3.5 h-3.5 fill-current" />
                      )}
                      <span>Submit Answer</span>
                    </button>
                  </div>
                </div>
              )}

              {currentChallenge.kind === "multi" && (
                <div className="space-y-4">
                  <div className="text-xs font-mono text-slate-400 uppercase tracking-wider mb-2">
                    Select all correct answers that apply:
                  </div>

                  <div className="space-y-2.5">
                    {(currentChallenge.config.options || []).map((opt, i) => {
                      const isSelected = selectedMulti.includes(i);
                      return (
                        <button
                          key={i}
                          type="button"
                          onClick={() => {
                            setSelectedMulti((prev) =>
                              isSelected
                                ? prev.filter((x) => x !== i)
                                : [...prev, i]
                            );
                          }}
                          className={`w-full text-left p-4 rounded-xl border transition-all cursor-pointer flex items-center gap-3 text-xs leading-relaxed ${
                            isSelected
                              ? "bg-purple-950/50 border-purple-500 text-white shadow-md shadow-purple-500/20"
                              : "bg-slate-950/60 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white"
                          }`}
                        >
                          <div
                            className={`w-5 h-5 rounded border flex items-center justify-center shrink-0 ${
                              isSelected
                                ? "bg-purple-600 border-purple-500 text-white"
                                : "border-slate-700 bg-slate-800"
                            }`}
                          >
                            {isSelected && <CheckCircle2 className="w-3.5 h-3.5" />}
                          </div>
                          <span>{opt}</span>
                        </button>
                      );
                    })}
                  </div>

                  <div className="pt-3 flex justify-end">
                    <button
                      type="button"
                      disabled={submitting || selectedMulti.length === 0}
                      onClick={handleSubmit}
                      className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold transition disabled:opacity-50 cursor-pointer shadow-lg shadow-purple-600/30"
                    >
                      {submitting ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <Play className="w-3.5 h-3.5 fill-current" />
                      )}
                      <span>Submit Selections</span>
                    </button>
                  </div>
                </div>
              )}

              {currentChallenge.kind === "short" && (
                <div className="space-y-4">
                  <div className="text-xs font-mono text-slate-400 uppercase tracking-wider mb-1">
                    Short Answer:
                  </div>

                  <div className="relative">
                    <span className="absolute left-3.5 top-1/2 -translate-y-1/2 font-mono text-purple-400 text-sm">
                      &gt;
                    </span>
                    <input
                      type="text"
                      value={shortText}
                      onChange={(e) => setShortText(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          e.preventDefault();
                          handleSubmit();
                        }
                      }}
                      placeholder={
                        currentChallenge.config.placeholder ||
                        "Type your concise answer here..."
                      }
                      className="w-full pl-8 pr-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-white font-mono text-xs focus:outline-none focus:border-purple-500 transition"
                    />
                  </div>

                  <div className="pt-2 flex justify-end">
                    <button
                      type="button"
                      disabled={submitting || !shortText.trim()}
                      onClick={handleSubmit}
                      className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold transition disabled:opacity-50 cursor-pointer shadow-lg shadow-purple-600/30"
                    >
                      {submitting ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <Play className="w-3.5 h-3.5 fill-current" />
                      )}
                      <span>Verify Answer</span>
                    </button>
                  </div>
                </div>
              )}

              {/* Feedback / Test Results Console */}
              {lastResult && (
                <div className="mt-5 pt-4 border-t border-slate-800 space-y-3">
                  {lastResult.correct ? (
                    <div className="p-4 rounded-xl bg-emerald-950/40 border border-emerald-500/50 text-xs">
                      <div className="flex items-center justify-between mb-2">
                        <span className="flex items-center gap-1.5 font-bold text-emerald-400">
                          <CheckCircle2 className="w-4 h-4" />
                          <span>Challenge Solved!</span>
                        </span>
                        <span className="font-mono font-bold text-emerald-300">
                          +{lastResult.xp_awarded} XP
                        </span>
                      </div>
                      {lastResult.explanation && (
                        <p className="text-slate-300 leading-relaxed mt-2 pt-2 border-t border-emerald-500/20">
                          {lastResult.explanation}
                        </p>
                      )}
                    </div>
                  ) : (
                    <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-500/50 text-xs">
                      <div className="flex items-center gap-1.5 font-bold text-rose-400 mb-1">
                        <AlertCircle className="w-4 h-4" />
                        <span>Incorrect submission</span>
                      </div>
                      <p className="text-slate-300">
                        {lastResult.detail?.error ||
                          "Review the requirements or hint and try again."}
                      </p>
                    </div>
                  )}

                  {/* Code Test Cases Breakdown */}
                  {lastResult.detail?.cases && lastResult.detail.cases.length > 0 && (
                    <div className="space-y-2 mt-3">
                      <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                        <span>Automated Test Cases:</span>
                        <span>
                          {lastResult.detail.passed_count} of{" "}
                          {lastResult.detail.total_count} passed
                        </span>
                      </div>

                      <div className="space-y-1.5">
                        {lastResult.detail.cases.map((c, i) => (
                          <div
                            key={i}
                            className={`p-2.5 rounded-lg font-mono text-xs border ${
                              c.passed
                                ? "bg-emerald-950/20 border-emerald-500/30 text-emerald-300"
                                : "bg-rose-950/20 border-rose-500/30 text-rose-300"
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <span>Case #{i + 1}</span>
                              <span>{c.passed ? "PASSED ✓" : "FAILED ✗"}</span>
                            </div>
                            <div className="text-[11px] text-slate-400 mt-1">
                              args: {JSON.stringify(c.args)} | expected:{" "}
                              {JSON.stringify(c.expect)} | got: {JSON.stringify(c.got)}
                            </div>
                            {c.error && (
                              <div className="mt-1 text-[11px] text-rose-400">
                                {c.error}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Next Challenge Navigation Action */}
                  <div className="flex items-center justify-between pt-2">
                    <button
                      type="button"
                      disabled={activeChallengeIdx === 0}
                      onClick={() => handleSelectChallenge(activeChallengeIdx - 1)}
                      className="px-3 py-1.5 rounded-lg border border-slate-800 text-xs text-slate-400 hover:text-white disabled:opacity-30 cursor-pointer"
                    >
                      ← Previous
                    </button>

                    {activeChallengeIdx < level.challenges.length - 1 ? (
                      <button
                        type="button"
                        onClick={() => handleSelectChallenge(activeChallengeIdx + 1)}
                        className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold cursor-pointer shadow-md shadow-purple-600/20"
                      >
                        <span>Next Challenge</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    ) : level.next_level_id ? (
                      <Link
                        href={`/levels/${level.next_level_id}`}
                        className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-md shadow-emerald-600/20"
                      >
                        <span>Advance to Level {level.index + 1}</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    ) : (
                      <Link
                        href="/tracks"
                        className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold"
                      >
                        <span>Return to Roadmap</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Celebration Modal when challenge/level is solved */}
      <CelebrationModal
        result={lastResult}
        onClose={() => setShowCelebration(false)}
        onNext={() => {
          setShowCelebration(false);
          if (activeChallengeIdx < level.challenges.length - 1) {
            handleSelectChallenge(activeChallengeIdx + 1);
          } else if (level.next_level_id) {
            router.push(`/levels/${level.next_level_id}`);
          }
        }}
        hasNext={
          activeChallengeIdx < level.challenges.length - 1 ||
          Boolean(level.next_level_id)
        }
      />
    </div>
  );
}
