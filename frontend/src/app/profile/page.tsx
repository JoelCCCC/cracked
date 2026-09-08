"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import {
  User as UserIcon,
  Flame,
  Sparkles,
  Shield,
  CheckCircle2,
  Lock,
  Save,
  Loader2,
  Calendar,
  Mail,
} from "lucide-react";

const RANKS = [
  { xp: 0, title: "Script Kiddie", desc: "Starting the journey, learning syntax & core constructs" },
  { xp: 250, title: "Junior", desc: "Writing clean loops, avoiding anti-patterns, basic recursion" },
  { xp: 750, title: "Builder", desc: "Building full-stack features, mastering state, writing clean APIs" },
  { xp: 1500, title: "Engineer", desc: "Understanding DB normalization, indexing, concurrency & caching" },
  { xp: 3000, title: "Senior", desc: "Designing robust distributed systems, CI/CD, and Docker orchestration" },
  { xp: 5000, title: "Architect", desc: "Large scale infrastructure, reliability, high-throughput pipelines" },
  { xp: 8000, title: "Cracked", desc: "Master of algorithms, systems, devops, and generative AI engineering" },
];

export default function ProfilePage() {
  const { user, refreshUser } = useAuth();
  const router = useRouter();

  const [displayName, setDisplayName] = useState(user?.display_name || "");
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);

  if (!user) {
    return (
      <div className="max-w-md mx-auto py-20 text-center text-xs">
        <p className="text-slate-400 mb-4">Please log in to view your profile.</p>
        <button
          type="button"
          onClick={() => router.push("/login")}
          className="px-4 py-2 rounded-xl bg-purple-600 text-white font-medium"
        >
          Sign In
        </button>
      </div>
    );
  }

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSuccess(false);

    try {
      await api.auth.updateProfile({ display_name: displayName });
      await refreshUser();
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Profile Header */}
      <div className="rounded-2xl border border-slate-800 bg-[#0e1122] p-6 sm:p-8 mb-8 shadow-2xl relative overflow-hidden">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-purple-600 to-cyan-500 flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-purple-600/30">
              {user.name.charAt(0).toUpperCase()}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-black text-white">{user.name}</h1>
                <span className="px-2.5 py-0.5 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-300 font-mono text-xs font-semibold">
                  {user.rank}
                </span>
              </div>
              <div className="flex items-center gap-3 text-xs text-slate-400 mt-1 font-mono">
                <span>@{user.username}</span>
                <span>•</span>
                <span className="flex items-center gap-1">
                  <Mail className="w-3.5 h-3.5" />
                  {user.email}
                </span>
                <span>•</span>
                <span className="flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5" />
                  Joined {new Date(user.date_joined).toLocaleDateString()}
                </span>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="flex items-center gap-3 font-mono text-xs">
            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-center">
              <div className="text-purple-400 font-bold text-base">{user.total_xp}</div>
              <div className="text-[10px] text-slate-500">TOTAL XP</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-center">
              <div className="text-amber-400 font-bold text-base flex items-center justify-center gap-1">
                <Flame className="w-4 h-4 fill-current" />
                {user.current_streak}d
              </div>
              <div className="text-[10px] text-slate-500">STREAK</div>
            </div>
          </div>
        </div>
      </div>

      {/* Edit Profile Form */}
      <div className="rounded-2xl border border-slate-800 bg-[#0e1122] p-6 mb-10 shadow-lg">
        <h2 className="text-base font-bold text-white mb-4 flex items-center gap-2">
          <UserIcon className="w-4 h-4 text-purple-400" />
          <span>Profile Settings</span>
        </h2>

        <form onSubmit={handleUpdate} className="space-y-4 text-xs">
          <div>
            <label className="block text-slate-400 font-medium mb-1">Display Name</label>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              placeholder="e.g. John Doe"
              className="w-full sm:w-80 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-xs focus:outline-none focus:border-purple-500"
            />
          </div>

          <div className="flex items-center gap-3 pt-1">
            <button
              type="submit"
              disabled={saving}
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold transition cursor-pointer shadow-md shadow-purple-600/20 disabled:opacity-50"
            >
              {saving ? (
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <Save className="w-3.5 h-3.5" />
              )}
              <span>Save Changes</span>
            </button>

            {success && (
              <span className="text-emerald-400 font-medium flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Profile updated!</span>
              </span>
            )}
          </div>
        </form>
      </div>

      {/* Rank Ladder Progression Map */}
      <div className="rounded-2xl border border-slate-800 bg-[#0e1122] p-6 shadow-xl">
        <h2 className="text-base font-bold text-white mb-1 flex items-center gap-2">
          <Shield className="w-4 h-4 text-cyan-400" />
          <span>The 7 Tiers of Mastery</span>
        </h2>
        <p className="text-xs text-slate-400 mb-6">
          Every challenge and level completed grants XP towards higher engineer titles.
        </p>

        <div className="space-y-3">
          {RANKS.map((r, i) => {
            const isCurrent = user.rank === r.title;
            const isUnlocked = user.total_xp >= r.xp;

            return (
              <div
                key={r.title}
                className={`p-4 rounded-xl border transition-all flex items-center justify-between gap-4 ${
                  isCurrent
                    ? "bg-purple-950/40 border-purple-500 shadow-md shadow-purple-500/10"
                    : isUnlocked
                    ? "bg-slate-950/60 border-slate-800/80"
                    : "bg-slate-950/30 border-slate-800/40 opacity-60"
                }`}
              >
                <div className="flex items-center gap-3.5">
                  <div
                    className={`w-8 h-8 rounded-xl font-mono text-xs font-bold flex items-center justify-center shrink-0 ${
                      isCurrent
                        ? "bg-purple-600 text-white"
                        : isUnlocked
                        ? "bg-emerald-950/80 text-emerald-400 border border-emerald-500/40"
                        : "bg-slate-900 text-slate-600 border border-slate-800"
                    }`}
                  >
                    0{i + 1}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-sm text-white">{r.title}</span>
                      {isCurrent && (
                        <span className="px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 font-mono text-[10px] font-semibold">
                          Current Rank
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5">{r.desc}</p>
                  </div>
                </div>

                <div className="font-mono text-xs text-right shrink-0">
                  <span className={isUnlocked ? "text-purple-300 font-bold" : "text-slate-500"}>
                    {r.xp} XP
                  </span>
                  <div className="text-[10px] text-slate-500">
                    {isUnlocked ? "Unlocked" : `Locked`}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
