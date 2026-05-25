import { useEffect, useState } from 'react'
import { Card } from '../components/Card'
import { PageTitle } from '../components/PageTitle'
import { Table } from '../components/Table'
import { facultadesService } from '../services/facultadesService'
import { salasService } from '../services/salasService'

const initialForm = {
  codigoSala: '',
  nombre: '',
  estado: 'Habilitada',
  observaciones: '',
  idFacultad: '',
  recursos: [],
}

export function SalasPage() {
  const [salas, setSalas] = useState([])
  const [facultades, setFacultades] = useState([])
  const [form, setForm] = useState(initialForm)
  const [actorId, setActorId] = useState('665100000000000000000001')
  const [status, setStatus] = useState('')

  const loadData = async () => {
    const [salasData, facultadesData] = await Promise.all([salasService.list(), facultadesService.list()])
    setSalas(salasData)
    setFacultades(facultadesData)
    if (!form.idFacultad && facultadesData.length > 0) {
      setForm((prev) => ({ ...prev, idFacultad: facultadesData[0].id }))
    }
  }

  useEffect(() => {
    loadData().catch((err) => setStatus(err.message))
  }, [])

  const onCreate = async (event) => {
    event.preventDefault()
    setStatus('')
    try {
      await salasService.create(form)
      setForm((prev) => ({ ...initialForm, idFacultad: prev.idFacultad }))
      await loadData()
      setStatus('Sala creada correctamente')
    } catch (err) {
      setStatus(err.message)
    }
  }

  const onToggleEstado = async (sala) => {
    const nextEstado = sala.estado === 'Habilitada' ? 'Deshabilitada' : 'Habilitada'
    try {
      await salasService.updateEstado(sala._id, nextEstado, 'Cambio desde frontend', actorId)
      await loadData()
      setStatus(`Estado actualizado en ${sala.codigoSala}`)
    } catch (err) {
      setStatus(err.message)
    }
  }

  return (
    <>
      <PageTitle title="Salas" subtitle="Gestion de salas, estado y facultad" />
      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <h2 className="mb-3 text-base font-semibold">Crear Sala</h2>
          <form className="space-y-3" onSubmit={onCreate}>
            <input required className="w-full rounded-md border border-slate-300 px-3 py-2" placeholder="codigoSala" value={form.codigoSala} onChange={(e) => setForm({ ...form, codigoSala: e.target.value })} />
            <input required className="w-full rounded-md border border-slate-300 px-3 py-2" placeholder="nombre" value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} />
            <select className="w-full rounded-md border border-slate-300 px-3 py-2" value={form.estado} onChange={(e) => setForm({ ...form, estado: e.target.value })}>
              <option>Habilitada</option>
              <option>Deshabilitada</option>
            </select>
            <textarea className="w-full rounded-md border border-slate-300 px-3 py-2" placeholder="observaciones" value={form.observaciones} onChange={(e) => setForm({ ...form, observaciones: e.target.value })} />
            <select className="w-full rounded-md border border-slate-300 px-3 py-2" value={form.idFacultad} onChange={(e) => setForm({ ...form, idFacultad: e.target.value })}>
              {facultades.map((facultad) => (
                <option key={facultad.id} value={facultad.id}>
                  {facultad.nombre}
                </option>
              ))}
            </select>
            <button className="w-full rounded-md bg-teal-600 px-3 py-2 font-medium text-white hover:bg-teal-700" type="submit">
              Guardar
            </button>
          </form>

          <div className="mt-4 border-t border-slate-200 pt-4">
            <label className="mb-1 block text-xs font-medium text-slate-600">Actor para cambio de estado (X-User-Id)</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2" value={actorId} onChange={(e) => setActorId(e.target.value)} />
          </div>

          {status ? <p className="mt-3 text-sm text-slate-700">{status}</p> : null}
        </Card>

        <Card className="lg:col-span-2">
          <Table
            columns={[
              { key: 'codigoSala', label: 'Codigo' },
              { key: 'nombre', label: 'Nombre' },
              { key: 'estado', label: 'Estado' },
              { key: 'observaciones', label: 'Observaciones' },
              {
                key: 'recursos',
                label: 'Recursos',
                render: (row) => `${row.recursos?.length || 0}`,
              },
              {
                key: 'accion',
                label: 'Accion',
                render: (row) => (
                  <button className="rounded bg-slate-200 px-2 py-1 text-xs hover:bg-slate-300" onClick={() => onToggleEstado(row)}>
                    Cambiar estado
                  </button>
                ),
              },
            ]}
            rows={salas}
          />
        </Card>
      </div>
    </>
  )
}
