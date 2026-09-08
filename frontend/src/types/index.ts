export interface User {
  id: number;
  username: string;
  email: string;
  name: string;
  display_name: string;
  total_xp: number;
  rank: string;
  current_streak: number;
  longest_streak: number;
  date_joined: string;
}

export interface LevelSummary {
  id: number;
  index: number;
  title: string;
  summary: string;
  xp_reward: number;
  challenge_count: number;
  solved_count: number;
  completed: boolean;
  unlocked: boolean;
}

export interface TrackSummary {
  id: number;
  slug: string;
  name: string;
  tagline: string;
  description: string;
  icon: string;
  accent: string;
  order: number;
  required_xp: number;
  unlocked?: boolean;
  xp_to_unlock?: number;
  level_count?: number;
  levels_completed?: number;
  challenge_count?: number;
  solved_count?: number;
  completed?: boolean;
  levels?: LevelSummary[];
}

export interface Lesson {
  id: number;
  order: number;
  title: string;
  body: string;
  minutes: number;
}

export type ChallengeKind = "mcq" | "multi" | "short" | "code";
export type ChallengeDifficulty = "easy" | "medium" | "hard";

export interface ChallengeConfig {
  options?: string[];
  placeholder?: string;
  language?: string;
  starter?: string;
  signature?: string;
}

export interface Challenge {
  id: number;
  order: number;
  kind: ChallengeKind;
  difficulty: ChallengeDifficulty;
  title: string;
  prompt: string;
  hint: string;
  xp: number;
  config: ChallengeConfig;
  solved: boolean;
}

export interface LevelDetail {
  id: number;
  index: number;
  title: string;
  summary: string;
  xp_reward: number;
  track: {
    slug: string;
    name: string;
    accent: string;
    icon: string;
  };
  lessons: Lesson[];
  challenges: Challenge[];
  next_level_id: number | null;
}

export interface TestCaseResult {
  args: unknown[];
  expect: unknown;
  got: unknown;
  passed: boolean;
  error?: string;
}

export interface SubmitResult {
  correct: boolean;
  detail: {
    error?: string;
    cases?: TestCaseResult[];
    passed_count?: number;
    total_count?: number;
  };
  xp_awarded: number;
  total_xp: number;
  rank: string;
  streak: number;
  already_solved: boolean;
  level_completed: boolean;
  track_completed: boolean;
  events: Array<{
    type: "challenge" | "level" | "track" | "rank" | "streak" | "track_unlocked";
    label: string;
    xp: number;
  }>;
  explanation?: string;
}

export interface DashboardData {
  user: User;
  tracks: TrackSummary[];
  stats: {
    solved: number;
    total_challenges: number;
    attempts: number;
    accuracy: number;
    levels_completed: number;
    total_levels: number;
  };
  next_level: {
    id: number;
    title: string;
    index: number;
    track_name: string;
    track_slug: string;
    accent: string;
  } | null;
  recent_solves: Array<{
    title: string;
    track: string;
    accent: string;
    xp: number;
    solved_at: string;
  }>;
}

export interface VaultItem {
  challenge_id: number;
  title: string;
  kind: ChallengeKind;
  difficulty: ChallengeDifficulty;
  xp: number;
  track_name: string;
  track_slug: string;
  track_accent: string;
  level_index: number;
  level_title: string;
  submission: {
    source?: string;
    choice?: number;
    choices?: number[];
    text?: string;
  };
  solved_at: string;
}

export interface HistoryData {
  vault: VaultItem[];
  total_solved: number;
  total_attempts: number;
}
