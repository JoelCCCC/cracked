export interface VisualizerStep {
  title: string;
  description: string;
  codeSnippet?: string;
  highlightIndices?: number[];
  customState?: Record<string, unknown>;
}

export interface ConceptVisualizerProps {
  trackSlug: string;
  levelIndex: number;
  lessonTitle?: string;
  onClose?: () => void;
  isModal?: boolean;
}
