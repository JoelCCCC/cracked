"use client";

import React, { useEffect, useRef } from "react";
import { Play, RotateCcw, Loader2 } from "lucide-react";

interface CodeEditorProps {
  value: string;
  onChange: (val: string) => void;
  onSubmit: () => void;
  onReset?: () => void;
  submitting?: boolean;
  language?: string;
}

export function CodeEditor({
  value,
  onChange,
  onSubmit,
  onReset,
  submitting = false,
  language = "python",
}: CodeEditorProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const gutterRef = useRef<HTMLDivElement>(null);

  const lines = value.split("\n");
  const lineCount = Math.max(lines.length, 12);

  const handleScroll = () => {
    if (textareaRef.current && gutterRef.current) {
      gutterRef.current.scrollTop = textareaRef.current.scrollTop;
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Ctrl+Enter or Cmd+Enter to run
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      if (!submitting) {
        onSubmit();
      }
      return;
    }

    // Tab key handling
    if (e.key === "Tab") {
      e.preventDefault();
      const textarea = textareaRef.current;
      if (!textarea) return;

      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;

      if (!e.shiftKey) {
        // Insert 4 spaces
        const nextValue = value.substring(0, start) + "    " + value.substring(end);
        onChange(nextValue);
        setTimeout(() => {
          textarea.selectionStart = textarea.selectionEnd = start + 4;
        }, 0);
      } else {
        // Remove up to 4 spaces before cursor
        const lineStart = value.lastIndexOf("\n", start - 1) + 1;
        const leading = value.substring(lineStart, start);
        const match = leading.match(/^ {1,4}/);
        if (match) {
          const count = match[0].length;
          const nextValue =
            value.substring(0, lineStart) + value.substring(lineStart + count);
          onChange(nextValue);
          setTimeout(() => {
            textarea.selectionStart = textarea.selectionEnd = Math.max(lineStart, start - count);
          }, 0);
        }
      }
    }
  };

  return (
    <div className="flex flex-col h-full rounded-xl border border-slate-800 bg-[#090b14] overflow-hidden shadow-2xl">
      {/* Editor Header Bar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-[#0e1120] border-b border-slate-800 text-xs text-slate-400">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5 mr-2">
            <div className="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
            <div className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
          </div>
          <span className="font-mono uppercase font-semibold text-slate-300">
            solution.{language === "javascript" ? "js" : "py"}
          </span>
          <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 font-mono text-[11px] border border-purple-500/20">
            {language}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {onReset && (
            <button
              type="button"
              onClick={onReset}
              title="Reset to starter code"
              className="flex items-center gap-1 text-slate-400 hover:text-slate-200 px-2 py-1 rounded hover:bg-slate-800 transition text-xs cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          )}

          <button
            type="button"
            disabled={submitting}
            onClick={onSubmit}
            className="flex items-center gap-1.5 px-3 py-1 rounded bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs transition shadow hover:shadow-purple-500/20 cursor-pointer disabled:opacity-50"
          >
            {submitting ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Running...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Run Code <kbd className="opacity-60 text-[10px] ml-1 font-sans">Ctrl+↵</kbd></span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Editor Body */}
      <div className="relative flex flex-1 min-h-[320px] font-mono text-sm leading-6">
        {/* Line Numbers Gutter */}
        <div
          ref={gutterRef}
          className="w-12 py-3 select-none text-right pr-3 text-slate-600 bg-[#090b14] border-r border-slate-800/80 overflow-hidden text-xs"
        >
          {Array.from({ length: lineCount }).map((_, i) => (
            <div key={i} className="leading-6">
              {i + 1}
            </div>
          ))}
        </div>

        {/* Code Textarea */}
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          onScroll={handleScroll}
          spellCheck={false}
          autoCapitalize="off"
          autoCorrect="off"
          className="flex-1 p-3 bg-transparent text-slate-100 resize-none outline-none font-mono text-xs leading-6 selection:bg-purple-600/40 selection:text-white"
          placeholder="# Write your solution here..."
        />
      </div>
    </div>
  );
}
