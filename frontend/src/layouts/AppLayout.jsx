import { NavLink, Outlet } from 'react-router-dom'

const links = [
  { to: '/', label: 'Inicio' },
  { to: '/facultades', label: 'Facultades' },
  { to: '/usuarios', label: 'Usuarios' },
  { to: '/salas', label: 'Salas' },
  { to: '/reservas', label: 'Reservas' },
  { to: '/auditoria', label: 'Auditoria' },
]

export function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-3">
          <h1 className="text-lg font-semibold">Campus Room Reservations</h1>
          <nav className="flex flex-wrap gap-2">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `rounded-md px-3 py-1.5 text-sm font-medium transition ${
                    isActive ? 'bg-teal-600 text-white' : 'text-slate-700 hover:bg-slate-200'
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}
