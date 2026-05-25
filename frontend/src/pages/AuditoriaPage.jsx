import { useEffect, useState } from 'react'
import { Card } from '../components/Card'
import { PageTitle } from '../components/PageTitle'
import { Table } from '../components/Table'
import { formatDate } from '../lib/format'
import { auditoriaService } from '../services/auditoriaService'

export function AuditoriaPage() {
  const [logs, setLogs] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    auditoriaService
      .list()
      .then(setLogs)
      .catch((err) => setError(err.message))
  }, [])

  return (
    <>
      <PageTitle title="Auditoria" subtitle="Trazabilidad de eventos del sistema" />
      <Card>
        {error ? <p className="mb-3 text-sm text-red-600">{error}</p> : null}
        <Table
          columns={[
            { key: 'tipo', label: 'Tipo' },
            { key: 'coleccion', label: 'Coleccion' },
            { key: 'descripcion', label: 'Descripcion' },
            { key: 'fecha', label: 'Fecha', render: (row) => formatDate(row.fecha) },
            { key: 'idUsuario', label: 'Usuario' },
          ]}
          rows={logs}
        />
      </Card>
    </>
  )
}
