"use client";
import React, { useState, useEffect } from "react";

function Typewriter({ text, speed = 100 }: { text: string; speed?: number }) {
  const [displayed, setDisplayed] = useState("");
  const [done, setDone] = useState(false);

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      i++;
      setDisplayed(text.slice(0, i));
      if (i >= text.length) {
        clearInterval(interval);
        setDone(true);
      }
    }, speed);
    return () => clearInterval(interval);
  }, [text, speed]);

  return (
    <>
      {displayed}
      <span
        className={`inline-block w-[2px] h-[0.9em] bg-purple-500 align-middle ml-0.5 ${done ? "animate-blink" : ""}`}
        aria-hidden="true"
      />
    </>
  );
}

const installText = `1. Clone \`https://github.com/compound-life-ai/longClaw\` to a stable local path.
2. Change into the cloned repository.
3. Run \`python3 scripts/install_bundle.py\`.
4. Run \`python3 scripts/install_bundle.py --verify\`.
5. Confirm that \`~/.openclaw/openclaw.json\` includes the installed bundle \`skills/\` path inside \`skills.load.extraDirs\`.
6. Tell the user to start a new OpenClaw session.
7. Tell the user to verify that \`/snap\`, \`/health\`, \`/news\`, and \`/insights\` are available and usable.
8. Tell the user to verify that \`daily-coach\` is loaded with \`openclaw skills info daily-coach\`.
9. If needed, tell the user to configure the cron templates from the installed \`cron/\` directory with their Telegram DM chat id, including \`cron/daily-health-coach.example.json\` for proactive daily coaching.`;

function CopyButton() {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={() => {
        navigator.clipboard.writeText(installText);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }}
      className="flex items-center gap-1.5 px-3 py-1.5 bg-[#1a1525] hover:bg-[#2a2040] text-gray-400 hover:text-white text-xs font-mono rounded border border-purple-500/20 transition-all duration-200"
    >
      {copied ? (
        <>
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-purple-400"><polyline points="20 6 9 17 4 12"/></svg>
          copied
        </>
      ) : (
        <>
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          copy
        </>
      )}
    </button>
  );
}


export default function VersionOne() {
  return (
    <main
      className="flex flex-col min-h-screen text-white relative overflow-hidden"
      style={{ backgroundColor: "#0e0c14" }}
    >
      {/* Hero reflection glow — SurrealDB style */}
      <div className="pointer-events-none absolute inset-x-0 top-0 z-0 flex justify-center overflow-hidden">
        <img
          src="/hero-reflection.jpg"
          alt=""
          className="w-[200vw] max-w-none -mt-[10%]"
          style={{ mixBlendMode: "lighten" }}
        />
      </div>

      {/* ============ NAVBAR ============ */}
      <nav className="relative z-20 flex items-center justify-between px-6 md:px-10 py-5 max-w-7xl mx-auto w-full">
        <div className="flex items-center gap-2">
          <img src="/logo-light.svg" alt="Longevity OS" className="h-8 w-8 rounded-lg" />
          <span className="text-lg font-bold tracking-tight">Longevity OS</span>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm text-gray-400">
          <a href="#features" className="hover:text-white transition-colors">Features</a>
          <a href="#install" className="hover:text-white transition-colors">Install</a>
          <a href="https://github.com/compound-life-ai/longClaw" target="_blank" rel="noreferrer" className="hover:text-white transition-colors flex items-center gap-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            GitHub
          </a>
        </div>
        <a
          href="#install"
          className="rounded-full bg-gradient-to-r from-purple-600 to-purple-500 text-white px-5 py-2 text-sm font-medium transition-all duration-200 hover:shadow-[0_0_24px_rgba(168,85,247,0.4)] hover:from-purple-500 hover:to-purple-400"
        >
          Get started
        </a>
      </nav>

      {/* ============ HERO ============ */}
      <section className="relative z-10 px-6 pt-36 pb-32 md:pt-52 md:pb-44 max-w-5xl mx-auto w-full text-center">
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-semibold tracking-tight mb-6 leading-tight text-white">
          Your longevity agent
        </h1>

        <p className="text-lg md:text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed mt-6">
          The AI health companion where nutrition, wearables, and coaching are one conversation.
        </p>

        <div className="mt-10 flex justify-center gap-4 flex-wrap">
          <a
            href="#install"
            className="rounded-full bg-gradient-to-r from-[#a855f7] to-[#c084fc] text-white px-8 py-3.5 text-base font-medium transition-all duration-200 hover:shadow-[0_0_30px_rgba(168,85,247,0.5)] hover:brightness-110"
          >
            Start building
          </a>
          <a
            href="https://github.com/compound-life-ai/longClaw"
            target="_blank"
            rel="noreferrer"
            className="rounded-full bg-transparent text-white border border-white/20 px-8 py-3.5 text-base font-medium transition-all duration-200 hover:bg-white/5 hover:border-white/30"
          >
            View source
          </a>
        </div>
      </section>

      {/* ============ LOGO STRIP ============ */}
      <section className="relative z-10 border-t border-white/5 py-10">
        <div className="max-w-5xl mx-auto px-6">
          <p className="text-center text-xs uppercase tracking-widest text-gray-600 mb-6">Built for</p>
          <div className="flex items-center justify-center gap-12 flex-wrap text-gray-600">
            <span className="text-lg font-bold tracking-wider">OpenClaw</span>
            <span className="text-lg font-bold tracking-wider">Telegram</span>
            <span className="text-lg font-bold tracking-wider">Apple Health</span>
            <span className="text-lg font-bold tracking-wider">Oura</span>
            <span className="text-lg font-bold tracking-wider">Whoop</span>
          </div>
        </div>
      </section>

      {/* ============ FEATURES - STAGGERED CARDS ============ */}
      <section id="features" className="relative z-10 px-6 py-24">
        {/* Subtle purple glow behind features */}
        <div
          className="pointer-events-none absolute left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2 w-[1000px] h-[600px] opacity-20 blur-3xl"
          style={{
            background: "radial-gradient(ellipse at center, rgba(168,85,247,0.3) 0%, transparent 70%)",
          }}
        />

        <div className="max-w-6xl mx-auto relative">
          <div className="text-center mb-16">
            <p className="text-sm font-mono uppercase tracking-widest text-purple-400 mb-3">Capabilities</p>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Talk naturally. Get quantified.
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              No buttons, no slash commands. Just say what you ate, ask about your sleep, or let it coach you proactively.
            </p>
          </div>

          {/* SurrealDB-style pillar cards — 3 staggered with 3D illustrations */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-5">
            {/* Card 1 — Nutrition */}
            <div className="relative overflow-hidden rounded-xl border border-white/5 bg-[#13111a] p-6 pb-8 min-h-[340px]">
              <p className="text-xs font-bold uppercase tracking-widest text-purple-400 mb-2">Nutrition</p>
              <h3 className="text-xl font-bold text-white mb-3">Meal Snap</h3>
              <p className="text-sm text-gray-400 leading-relaxed max-w-[70%]">
                Send a food photo or describe what you ate. Full micronutrient breakdown in seconds.
              </p>
              <button className="mt-6 h-10 w-10 rounded-full border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:border-white/30 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 18l6-6-6-6"/></svg>
              </button>
              <img src="/card-memory.png" alt="" className="absolute -right-8 -bottom-4 w-[280px] h-[280px] object-contain pointer-events-none" />
            </div>

            {/* Card 2 — Wearables */}
            <div className="relative overflow-hidden rounded-xl border border-white/5 bg-[#13111a] p-6 pb-8 min-h-[340px]">
              <p className="text-xs font-bold uppercase tracking-widest text-purple-400 mb-2">Wearables</p>
              <h3 className="text-xl font-bold text-white mb-3">Pattern Insights</h3>
              <p className="text-sm text-gray-400 leading-relaxed max-w-[70%]">
                Cross-references sleep, HRV, nutrition, and activity to surface hidden correlations.
              </p>
              <button className="mt-6 h-10 w-10 rounded-full border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:border-white/30 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 18l6-6-6-6"/></svg>
              </button>
              <img src="/card-context.png" alt="" className="absolute -right-8 -bottom-4 w-[280px] h-[280px] object-contain pointer-events-none" />
            </div>

            {/* Card 3 — Coaching */}
            <div className="relative overflow-hidden rounded-xl border border-white/5 bg-[#13111a] p-6 pb-8 min-h-[340px]">
              <p className="text-xs font-bold uppercase tracking-widest text-purple-400 mb-2">Coaching</p>
              <h3 className="text-xl font-bold text-white mb-3">Daily Coach</h3>
              <p className="text-sm text-gray-400 leading-relaxed max-w-[70%]">
                Morning briefing with overnight sleep, nutrition gaps, active experiments, and longevity news.
              </p>
              <button className="mt-6 h-10 w-10 rounded-full border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:border-white/30 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 18l6-6-6-6"/></svg>
              </button>
              <img src="/card-storage.png" alt="" className="absolute -right-8 -bottom-4 w-[280px] h-[280px] object-contain pointer-events-none" />
            </div>
          </div>

          {/* Purple glow strip beneath cards (like SurrealDB) */}
          <div
            className="pointer-events-none h-24 -mt-4 relative z-0"
            style={{
              background: "linear-gradient(180deg, transparent 0%, rgba(168,85,247,0.15) 40%, rgba(168,85,247,0.25) 60%, transparent 100%)",
            }}
          />
        </div>
      </section>

      {/* ============ INSTALLATION ============ */}
      <section id="install" className="relative z-10 px-6 py-24">
        {/* Subtle glow behind section */}
        <div
          className="pointer-events-none absolute left-1/2 -translate-x-1/2 bottom-0 w-[800px] h-[400px] opacity-15 blur-3xl"
          style={{
            background: "radial-gradient(ellipse at center, rgba(168,85,247,0.4) 0%, transparent 70%)",
          }}
        />

        <div className="max-w-4xl mx-auto relative">
          <div className="text-center mb-10">
            <p className="text-sm font-mono uppercase tracking-widest text-purple-400 mb-3">Get Started</p>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Install in one prompt
            </h2>
            <p className="text-gray-400">
              Ask your OpenClaw agent to install this bundle using the prompt below.
            </p>
          </div>

          <div className="bg-[#0a0615] border border-purple-500/10 rounded-xl overflow-hidden">
            <div className="px-5 py-3 bg-[#12091f] border-b border-purple-500/10 flex justify-between items-center">
              <div className="flex items-center gap-3">
                <div className="flex gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-red-500/60" />
                  <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/60" />
                  <span className="w-2.5 h-2.5 rounded-full bg-green-500/60" />
                </div>
                <span className="text-xs font-mono text-gray-500">installation_prompt.md</span>
              </div>
              <CopyButton />
            </div>
            <div className="p-6 overflow-x-auto">
              <pre className="text-sm font-mono text-gray-400 whitespace-pre-wrap leading-relaxed">
{installText}
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* ============ LOCAL-FIRST ============ */}
      <section className="relative z-10 px-6 py-24 border-t border-white/5">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-sm font-mono uppercase tracking-widest text-purple-400 mb-3">Architecture</p>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Local-first. No cloud required.
          </h2>
          <p className="text-gray-400 mb-10 max-w-2xl mx-auto">
            All health metrics, meal logs, and experiments stay on your machine inside{" "}
            <code className="bg-purple-500/10 border border-purple-500/20 px-2 py-0.5 rounded text-xs font-mono text-purple-300">longevityOS-data/</code>.
            No telemetry. No subscriptions.
          </p>
          <div className="text-left bg-[#0a0615] rounded-xl p-6 border border-purple-500/10 font-mono text-sm overflow-x-auto">
            <div className="text-gray-600 mb-3 text-xs">$ tree longevityOS-data/</div>
            <pre className="text-gray-400 leading-relaxed">
{`longevityOS-data/
├── nutrition/
│   └── meals.csv        `}<span className="text-gray-600"># deterministic macros</span>{`
├── health/
│   └── profile.json     `}<span className="text-gray-600"># Apple Health aggregation</span>{`
├── insights/
│   ├── experiments.json `}<span className="text-gray-600"># hypotheses & interventions</span>{`
│   └── checkins.json    `}<span className="text-gray-600"># daily compliance logs</span>{`
└── news/
    └── cache.json       `}<span className="text-gray-600"># off-grid reading cache</span>
            </pre>
          </div>
        </div>
      </section>

      {/* ============ FOOTER ============ */}
      <footer className="relative z-10 border-t border-white/5 py-12 px-6">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <img src="/logo-light.svg" alt="Longevity OS" className="h-6 w-6 rounded-md" />
            <span className="text-sm font-bold">Longevity OS</span>
          </div>
          <p className="text-xs text-gray-600">
            {new Date().getFullYear()} &middot; Built with Next.js + Tailwind
          </p>
          <div className="flex items-center gap-6 text-sm text-gray-500">
            <a href="https://github.com/compound-life-ai/longClaw" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">GitHub</a>
            <a href="#install" className="hover:text-white transition-colors">Install</a>
          </div>
        </div>
      </footer>
    </main>
  );
}
