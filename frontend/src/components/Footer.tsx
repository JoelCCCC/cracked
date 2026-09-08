import React from "react";
import Link from "next/link";
import { Zap, Terminal, Shield, Cpu, Code2 } from "lucide-react";

export function Footer() {
  return (
    <footer className="w-full border-t border-slate-800/80 bg-[#080910] text-slate-400 py-10 mt-20 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded bg-gradient-to-tr from-purple-600 to-cyan-500 flex items-center justify-center text-white">
                <Zap className="w-3.5 h-3.5 fill-white" />
              </div>
              <span className="font-bold text-white font-mono tracking-wider">CRACKED</span>
            </div>
            <p className="text-slate-400 leading-relaxed text-[11px]">
              The uncompromising progression system to master software engineering from fundamental syntax to production AI systems.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-slate-200 uppercase tracking-wider text-[11px] mb-3">
              The 6 Disciplines
            </h4>
            <ul className="space-y-2 text-[11px]">
              <li><Link href="/tracks/coding" className="hover:text-purple-400 transition">1. Coding Foundations</Link></li>
              <li><Link href="/tracks/algorithms" className="hover:text-purple-400 transition">2. Algorithms & Data Structures</Link></li>
              <li><Link href="/tracks/web" className="hover:text-purple-400 transition">3. Web Development</Link></li>
              <li><Link href="/tracks/databases" className="hover:text-purple-400 transition">4. Database Design</Link></li>
              <li><Link href="/tracks/devops" className="hover:text-purple-400 transition">5. DevOps & Infrastructure</Link></li>
              <li><Link href="/tracks/ai" className="hover:text-purple-400 transition">6. AI Engineering</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-slate-200 uppercase tracking-wider text-[11px] mb-3">
              Rank Ladder
            </h4>
            <ul className="space-y-1.5 text-[11px] font-mono">
              <li className="text-slate-500">0 XP: Script Kiddie</li>
              <li className="text-slate-400">250 XP: Junior</li>
              <li className="text-blue-400">750 XP: Builder</li>
              <li className="text-emerald-400">1500 XP: Engineer</li>
              <li className="text-amber-400">3000 XP: Senior</li>
              <li className="text-purple-400">5000 XP: Architect</li>
              <li className="text-cyan-400 font-bold">8000+ XP: Cracked</li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-slate-200 uppercase tracking-wider text-[11px] mb-3">
              Architecture
            </h4>
            <div className="space-y-2 text-[11px] text-slate-400">
              <div className="flex items-center gap-2">
                <Code2 className="w-3.5 h-3.5 text-cyan-400" />
                <span>Next.js 16 + React 19 Frontend</span>
              </div>
              <div className="flex items-center gap-2">
                <Terminal className="w-3.5 h-3.5 text-purple-400" />
                <span>Django REST Framework</span>
              </div>
              <div className="flex items-center gap-2">
                <Shield className="w-3.5 h-3.5 text-emerald-400" />
                <span>PostgreSQL 17 Database</span>
              </div>
              <div className="flex items-center gap-2">
                <Cpu className="w-3.5 h-3.5 text-rose-400" />
                <span>Sandboxed Code Execution Engine</span>
              </div>
            </div>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-500">
          <div>Built for developers aiming to be in the top 1%.</div>
          <div className="flex items-center gap-2 mt-2 sm:mt-0 font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Systems Operational</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
