import { Link } from 'react-router-dom'
import { Card } from '../components/Card'
import { PageTitle } from '../components/PageTitle'

const cards = [
  { to: '/facultades', title: 'Facultades', text: 'Consulta facultades disponibles.' },
  { to: '/usuarios', title: 'Usuarios', text: 'Gestiona docentes y secretarias.' },
  { to: '/salas', title: 'Salas', text: 'Administra estado y recursos de salas.' },
  { to: '/reservas', title: 'Reservas', text: 'Crea, cancela y ajusta reservas.' },
  { to: '/auditoria', title: 'Auditoria', text: 'Revisa trazabilidad de cambios.' },
]

export function HomePage() {
  return (
    <>
      <PageTitle title="Panel del Sistema" subtitle="Frontend React + Tailwind consumiendo API FastAPI" />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {cards.map((card) => (
          <Link key={card.to} to={card.to}>
            <Card className="h-full transition hover:-translate-y-0.5 hover:border-teal-400 hover:shadow-md">
              <h2 className="text-lg font-semibold text-slate-900">{card.title}</h2>
              <p className="mt-1 text-sm text-slate-600">{card.text}</p>
            </Card>
          </Link>
        ))}
      </div>
    </>
  )
}
