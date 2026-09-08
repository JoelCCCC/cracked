"use client";

import React, { useState } from "react";
import {
  VariablesVisualizer,
  ConditionalsVisualizer,
  LoopsVisualizer,
  CollectionsVisualizer,
  FunctionsVisualizer,
} from "./CodingVisualizers";
import {
  BigOVisualizer,
  TwoPointersVisualizer,
  BinarySearchVisualizer,
  SlidingWindowVisualizer,
  DynamicProgrammingVisualizer,
} from "./AlgorithmsVisualizers";
import {
  HttpLifecycleVisualizer,
  DomTreeVisualizer,
  EventLoopVisualizer,
  RenderingVisualizer,
  WebSecurityVisualizer,
} from "./WebVisualizers";
import {
  RelationalTableVisualizer,
  SqlPipelineVisualizer,
  JoinsVisualizer,
  BTreeVisualizer,
  AcidVisualizer,
} from "./DatabaseVisualizers";
import {
  LinuxPipesVisualizer,
  GitTreesVisualizer,
  DockerVisualizer,
  DeploymentVisualizer,
  ObservabilityVisualizer,
} from "./DevOpsVisualizers";
import {
  NeuralNetVisualizer,
  EmbeddingVisualizer,
  AutoregressiveVisualizer,
  ChainOfThoughtVisualizer,
  RagVisualizer,
} from "./AIVisualizers";
import { ConceptVisualizerProps } from "./types";
import { X, Sparkles, Layers } from "lucide-react";

export function ConceptVisualizer({
  trackSlug,
  levelIndex,
  onClose,
  isModal = false,
}: ConceptVisualizerProps) {
  // Allow user to switch between level concepts if they want
  const [selectedLevel, setSelectedLevel] = useState<number>(levelIndex);

  function renderVisualizer() {
    switch (trackSlug) {
      case "coding":
        switch (selectedLevel) {
          case 1:
            return <VariablesVisualizer />;
          case 2:
            return <ConditionalsVisualizer />;
          case 3:
            return <LoopsVisualizer />;
          case 4:
            return <CollectionsVisualizer />;
          case 5:
            return <FunctionsVisualizer />;
          default:
            return <VariablesVisualizer />;
        }

      case "algorithms":
        switch (selectedLevel) {
          case 1:
            return <BigOVisualizer />;
          case 2:
            return <TwoPointersVisualizer />;
          case 3:
            return <BinarySearchVisualizer />;
          case 4:
            return <SlidingWindowVisualizer />;
          case 5:
            return <DynamicProgrammingVisualizer />;
          default:
            return <BigOVisualizer />;
        }

      case "web":
        switch (selectedLevel) {
          case 1:
            return <HttpLifecycleVisualizer />;
          case 2:
            return <DomTreeVisualizer />;
          case 3:
            return <EventLoopVisualizer />;
          case 4:
            return <RenderingVisualizer />;
          case 5:
            return <WebSecurityVisualizer />;
          default:
            return <HttpLifecycleVisualizer />;
        }

      case "databases":
        switch (selectedLevel) {
          case 1:
            return <RelationalTableVisualizer />;
          case 2:
            return <SqlPipelineVisualizer />;
          case 3:
            return <JoinsVisualizer />;
          case 4:
            return <BTreeVisualizer />;
          case 5:
            return <AcidVisualizer />;
          default:
            return <RelationalTableVisualizer />;
        }

      case "devops":
        switch (selectedLevel) {
          case 1:
            return <LinuxPipesVisualizer />;
          case 2:
            return <GitTreesVisualizer />;
          case 3:
            return <DockerVisualizer />;
          case 4:
            return <DeploymentVisualizer />;
          case 5:
            return <ObservabilityVisualizer />;
          default:
            return <LinuxPipesVisualizer />;
        }

      case "ai":
        switch (selectedLevel) {
          case 1:
            return <NeuralNetVisualizer />;
          case 2:
            return <EmbeddingVisualizer />;
          case 3:
            return <AutoregressiveVisualizer />;
          case 4:
            return <ChainOfThoughtVisualizer />;
          case 5:
            return <RagVisualizer />;
          default:
            return <NeuralNetVisualizer />;
        }

      default:
        return <VariablesVisualizer />;
    }
  }

  const content = (
    <div className="space-y-3">
      {/* Concept Level Selector bar */}
      <div className="flex items-center justify-between px-1 pb-1 overflow-x-auto gap-2">
        <div className="flex items-center gap-1.5 text-xs font-mono text-slate-400">
          <Layers className="w-3.5 h-3.5 text-purple-400" />
          <span>Interactive Animation Stages:</span>
        </div>
        <div className="flex items-center gap-1">
          {[1, 2, 3, 4, 5].map((lvl) => (
            <button
              key={lvl}
              type="button"
              onClick={() => setSelectedLevel(lvl)}
              className={`px-2.5 py-1 rounded-lg text-xs font-mono font-bold transition cursor-pointer ${
                selectedLevel === lvl
                  ? "bg-purple-600 text-white shadow-sm shadow-purple-500/30"
                  : "bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              Level {lvl}
            </button>
          ))}
        </div>
      </div>

      {renderVisualizer()}
    </div>
  );

  if (isModal) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
        <div className="relative w-full max-w-3xl">
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="absolute -top-10 right-0 p-2 text-slate-400 hover:text-white rounded-lg transition cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          )}
          {content}
        </div>
      </div>
    );
  }

  return content;
}
