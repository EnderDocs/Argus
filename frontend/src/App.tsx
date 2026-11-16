import { ShieldCheck, Activity, Database, CheckCircle2 } from 'lucide-react';

export function App() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-br from-[#0a0f1d] via-[#0f172a] to-[#1e1e38]">
      <div className="glass-panel p-8 md:p-12 rounded-2xl max-w-2xl w-full shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-48 h-48 bg-argus-blue-500/10 rounded-full blur-3xl -z-10" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-argus-orange-500/10 rounded-full blur-3xl -z-10" />

        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-argus-blue-600/20 border border-argus-blue-500/30 rounded-xl text-argus-blue-500">
            <Activity className="w-8 h-8 text-argus-orange-500 animate-pulse" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-2">
              Argus <span className="text-xs px-2.5 py-0.5 rounded-full bg-argus-orange-500/20 text-argus-orange-400 border border-argus-orange-500/30 font-medium">ModSI</span>
            </h1>
            <p className="text-sm text-slate-400">Plataforma de Datasets de Sensores de Robótica</p>
          </div>
        </div>

        <div className="space-y-4 mb-8 text-slate-300 text-sm leading-relaxed">
          <p>
            O ambiente e as dependências foram inicializados com sucesso! A estrutura modular e a stack tecnológica estão prontas para desenvolvimento.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex items-center gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span className="text-xs font-medium text-slate-200">React + Vite + Tailwind CSS</span>
            </div>
            <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex items-center gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span className="text-xs font-medium text-slate-200">Django Ninja API (/api/v1/)</span>
            </div>
            <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex items-center gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span className="text-xs font-medium text-slate-200">MySQL 8 & Migrações</span>
            </div>
            <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex items-center gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span className="text-xs font-medium text-slate-200">Docker / Podman Compose</span>
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400">
          <span className="flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Infraestrutura G0 Pronta
          </span>
          <span className="flex items-center gap-1.5">
            <Database className="w-4 h-4 text-argus-blue-500" />
            Porta MySQL 3306
          </span>
        </div>
      </div>
    </main>
  );
}

export default App;
