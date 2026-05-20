import { createBrowserRouter } from 'react-router-dom'
import { AppLayout } from '../layouts/AppLayout'
import { AuditoriaPage } from '../pages/AuditoriaPage'
import { FacultadesPage } from '../pages/FacultadesPage'
import { HomePage } from '../pages/HomePage'
import { ReservasPage } from '../pages/ReservasPage'
import { SalasPage } from '../pages/SalasPage'
import { UsuariosPage } from '../pages/UsuariosPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'facultades', element: <FacultadesPage /> },
      { path: 'usuarios', element: <UsuariosPage /> },
      { path: 'salas', element: <SalasPage /> },
      { path: 'reservas', element: <ReservasPage /> },
      { path: 'auditoria', element: <AuditoriaPage /> },
    ],
  },
])
