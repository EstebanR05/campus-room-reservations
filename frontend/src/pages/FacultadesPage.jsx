import { useEffect, useState } from 'react'
import { Card } from '../components/Card'
import { PageTitle } from '../components/PageTitle'
import { Table } from '../components/Table'
import { facultadesService } from '../services/facultadesService'

export function FacultadesPage() {
  const [facultades, setFacultades] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    facultadesService
      .list()
      .then(setFacultades)
      .catch((err) => setError(err.message))
  }, [])

  return (
    <>
      <PageTitle title="Facultades" subtitle="Listado de facultades registradas" />
      <Card>
        {error ? <p className="mb-3 text-sm text-red-600">{error}</p> : null}
        <Table
          columns={[
            { key: 'id', label: 'ID' },
            { key: 'nombre', label: 'Nombre' },
            { key: 'descripcion', label: 'Descripcion' },
          ]}
          rows={facultades}
        />
      </Card>
    </>
  )
}
