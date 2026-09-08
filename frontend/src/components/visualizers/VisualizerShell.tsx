"use client";

import React, { useState, useEffect } from "react";
import {
  Play,
  Pause,
  RotateCcw,
  ChevronRight,
  ChevronLeft,
  Sparkles,
  Zap,
  Gauge,
  X,
  Maximize2,
  Minimize2,
} from "lucide-react";
import { VisualizerStep } from "./types";

interface VisualizerShellProps {
  title: string;
  subtitle: string;
  tag: string;
  accentColor?: string;
  steps: VisualizerStep[];
  currentStep: number;
  onStepChange: (step: number) => void;
  children: React.ReactNode;
  onClose?: () => void;
  isModal?: boolean;
}

export function VisualizerShell({
  title,
  subtitle,
  tag,
  accentColor = "#7c5cff",
  steps,
  currentStep,
  onStepChange,
  children,
  onClose,
  isModal = false,
}: VisualizerShellProps) {
  const [isPlaying, setIsPlaying] = useState<boolean>(true);
  const [speed, setSpeed] = useState<number>(1); // 1x, 1.5x, 2x

  // Auto-play timer
  useEffect(() => {
    if (!isPlaying) return;

    const intervalMs = 2800 / speed;
    const timer = setInterval(() => {
      onStepChange((currentStep + 1) % steps.length);
    }, intervalMs);

    return () => clearInterval(timer);
  }, [isPlaying, currentStep, steps.length, speed, onStepChange]);

  const activeStep = steps[currentStep] || steps[0];

  return (
    <div
      className={`rounded-2xl border border-slate-800 bg-[#0a0c16] shadow-2xl overflow-hidden transition-all duration-300 ${
        isModal ? "w-full max-w-4xl" : "w-full"
      }`}
    >
      {/* Visualizer Top Bar */}
      <div className="flex items-center justify-between px-5 py-3.5 bg-gradient-to-r from-slate-900/90 via-[#0e1224] to-slate-900/90 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center text-white shadow-md font-mono text-sm"
            style={{ backgroundColor: accentColor }}
          >
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-sm font-bold text-white tracking-wide">
                {title}
              </h3>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-purple-950/70 border border-purple-800/60 text-purple-300">
                {tag}
              </span>
            </div>
            <p className="text-xs text-slate-400">{subtitle}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-slate-400 bg-slate-800/80 px-2.5 py-1 rounded-md border border-slate-700/50">
            Step <span className="text-white font-bold">{currentStep + 1}</span> /{" "}
            {steps.length}
          </span>
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Progress Bar with clickable checkpoints */}
      <div className="w-full bg-slate-900/80 h-1.5 relative flex">
        {steps.map((_, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => {
              onStepChange(idx);
              setIsPlaying(false);
            }}
            className="flex-1 h-full relative cursor-pointer group"
          >
            <div
              className={`h-full transition-all duration-300 ${
                idx <= currentStep
                  ? "bg-gradient-to-r from-purple-500 to-cyan-400"
                  : "bg-slate-800 group-hover:bg-slate-700"
              }`}
            />
          </button>
        ))}
      </div>

      {/* Animation Stage / Canvas */}
      <div className="p-5 sm:p-6 bg-radial from-slate-900/40 to-[#070913] min-h-[280px] flex items-center justify-center relative overflow-hidden">
        {/* Subtle decorative grid lines */}
        <div className="absolute inset-0 bg-grid-pattern opacity-10 pointer-events-none" />
        <div className="relative z-10 w-full">{children}</div>
      </div>

      {/* Step Explanation Banner */}
      <div className="px-5 py-4 bg-slate-900/90 border-t border-slate-800/80 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div className="space-y-1 max-w-2xl">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-300 font-mono">
              {activeStep.title}
            </h4>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            {activeStep.description}
          </p>
          {activeStep.codeSnippet && (
            <code className="inline-block mt-1 text-[11px] font-mono bg-slate-950 px-2 py-0.5 rounded text-purple-300 border border-slate-800">
              {activeStep.codeSnippet}
            </code>
          )}
        </div>

        {/* Player Controls Bar */}
        <div className="flex items-center gap-1.5 self-end sm:self-center bg-slate-950/80 p-1 rounded-xl border border-slate-800">
          <button
            type="button"
            title="Reset"
            onClick={() => {
              onStepChange(0);
              setIsPlaying(false);
            }}
            className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800/80 transition cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>

          <button
            type="button"
            title="Previous step"
            onClick={() => {
              onStepChange((currentStep - 1 + steps.length) % steps.length);
              setIsPlaying(false);
            }}
            className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800/80 transition cursor-pointer"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
          </button>

          <button
            type="button"
            title={isPlaying ? "Pause animation" : "Play animation"}
            onClick={() => setIsPlaying(!isPlaying)}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition cursor-pointer ${
              isPlaying
                ? "bg-purple-600 text-white shadow-sm shadow-purple-500/30"
                : "bg-slate-800 text-slate-200 hover:bg-slate-700"
            }`}
          >
            {isPlaying ? (
              <>
                <Pause className="w-3.5 h-3.5" />
                <span>Pause</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Play</span>
              </>
            )}
          </button>

          <button
            type="button"
            title="Next step"
            onClick={() => {
              onStepChange((currentStep + 1) % steps.length);
              setIsPlaying(false);
            }}
            className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800/80 transition cursor-pointer"
          >
            <ChevronRight className="w-3.5 h-3.5" />
          </button>

          <div className="h-4 w-px bg-slate-800 mx-1" />

          {/* Speed Toggle */}
          <button
            type="button"
            onClick={() => {
              const speeds = [1, 1.5, 2];
              const nextIdx = (speeds.indexOf(speed) + 1) % speeds.length;
              setSpeed(speeds[nextIdx]);
            }}
            className="px-2 py-1 text-[10px] font-mono font-bold text-cyan-400 hover:bg-slate-800/80 rounded transition cursor-pointer"
            title="Toggle playback speed"
          >
            {speed}x
          </button>
        </div>
      </div>
    </div>
  );
}
