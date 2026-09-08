"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import {
  Flame,
  Zap,
  Archive,
  Compass,
  LayoutDashboard,
  User as UserIcon,
  LogOut,
  ChevronDown,
  Sparkles,
} from "lucide-react";

export function Navbar() {
  const { user, logout, quickDemoLogin } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [demoLoading, setDemoLoading] = useState(false);

  const handleDemo = async () => {
    setDemoLoading(true);
    try {
      await quickDemoLogin();
      router.push("/dashboard");
    } catch (e) {
      console.error(e);
    } finally {
      setDemoLoading(false);
    }
  };

  return (
    <nav className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-[#080911]/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-600 to-cyan-500 flex items-center justify-center shadow-md shadow-purple-600/30 group-hover:scale-105 transition-transform">
              <Zap className="w-4.5 h-4.5 text-white fill-white" />
            </div>
            <div className="flex flex-col">
              <span className="font-extrabold tracking-wider text-base text-white font-mono flex items-center gap-1">
                CRACKED<span className="text-cyan-400">.</span>
              </span>
              <span className="text-[9px] uppercase tracking-widest text-slate-500 font-mono -mt-1">
                Zero to Architect
              </span>
            </div>
          </Link>

          {/* Nav Links */}
          <div className="hidden md:flex items-center gap-1 text-sm font-medium">
            <Link
              href="/dashboard"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-colors ${
                pathname === "/dashboard"
                  ? "text-purple-400 bg-purple-950/40 border border-purple-500/20"
                  : "text-slate-300 hover:text-white hover:bg-slate-800/50"
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              <span>Dashboard</span>
            </Link>

            <Link
              href="/tracks"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-colors ${
                pathname.startsWith("/tracks") || pathname.startsWith("/levels")
                  ? "text-purple-400 bg-purple-950/40 border border-purple-500/20"
                  : "text-slate-300 hover:text-white hover:bg-slate-800/50"
              }`}
            >
              <Compass className="w-4 h-4" />
              <span>Disciplines</span>
            </Link>

            <Link
              href="/history"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-colors ${
                pathname === "/history"
                  ? "text-purple-400 bg-purple-950/40 border border-purple-500/20"
                  : "text-slate-300 hover:text-white hover:bg-slate-800/50"
              }`}
            >
              <Archive className="w-4 h-4 text-cyan-400" />
              <span>Solution Vault</span>
            </Link>
          </div>
        </div>

        {/* Right side widgets */}
        <div className="flex items-center gap-3">
          {user ? (
            <div className="flex items-center gap-3">
              {/* Streak */}
              <div
                title={`${user.current_streak}-day streak`}
                className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold"
              >
                <Flame className="w-3.5 h-3.5 fill-amber-400" />
                <span>{user.current_streak}</span>
              </div>

              {/* XP Pill */}
              <div className="hidden sm:flex items-center gap-1 px-2.5 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs font-semibold font-mono">
                <Sparkles className="w-3 h-3 text-purple-400" />
                <span>{user.total_xp} XP</span>
              </div>

              {/* Rank Badge */}
              <div className="hidden lg:block px-2 py-0.5 rounded bg-slate-800 text-[11px] font-mono text-cyan-300 border border-slate-700">
                {user.rank}
              </div>

              {/* User Dropdown */}
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="flex items-center gap-2 pl-2 pr-1.5 py-1 rounded-lg hover:bg-slate-800/80 border border-slate-700/60 transition cursor-pointer text-xs text-slate-200"
                >
                  <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-purple-500 to-cyan-500 flex items-center justify-center font-bold text-[11px] text-white">
                    {user.name.charAt(0).toUpperCase()}
                  </div>
                  <span className="max-w-[100px] truncate font-medium text-slate-200">
                    {user.name}
                  </span>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                </button>

                {dropdownOpen && (
                  <div
                    onClick={() => setDropdownOpen(false)}
                    className="absolute right-0 mt-2 w-48 rounded-xl border border-slate-800 bg-[#0f111f] p-1.5 shadow-2xl z-50 text-xs font-medium"
                  >
                    <div className="px-3 py-2 border-b border-slate-800 mb-1">
                      <div className="font-semibold text-slate-200 truncate">{user.name}</div>
                      <div className="text-[11px] text-slate-400 font-mono">@{user.username}</div>
                      <div className="mt-1 text-[10px] text-purple-400 font-mono uppercase">{user.rank}</div>
                    </div>

                    <Link
                      href="/dashboard"
                      className="flex items-center gap-2 px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/60"
                    >
                      <LayoutDashboard className="w-3.5 h-3.5" />
                      <span>Dashboard</span>
                    </Link>

                    <Link
                      href="/profile"
                      className="flex items-center gap-2 px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/60"
                    >
                      <UserIcon className="w-3.5 h-3.5" />
                      <span>Profile & Ranks</span>
                    </Link>

                    <button
                      type="button"
                      onClick={() => {
                        logout();
                        router.push("/");
                      }}
                      className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-rose-400 hover:text-rose-300 hover:bg-rose-950/40 text-left cursor-pointer"
                    >
                      <LogOut className="w-3.5 h-3.5" />
                      <span>Log Out</span>
                    </button>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-2 text-xs">
              <button
                type="button"
                onClick={handleDemo}
                disabled={demoLoading}
                className="hidden sm:flex items-center gap-1 px-3 py-1.5 rounded-lg border border-cyan-500/40 bg-cyan-950/30 text-cyan-300 hover:bg-cyan-950/60 transition cursor-pointer font-medium"
              >
                <Zap className="w-3.5 h-3.5" />
                <span>{demoLoading ? "Logging in..." : "Demo Mode"}</span>
              </button>

              <Link
                href="/login"
                className="px-3 py-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/60 transition"
              >
                Sign In
              </Link>

              <Link
                href="/login?tab=register"
                className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium shadow-md shadow-purple-600/20 transition"
              >
                Get Cracked
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
