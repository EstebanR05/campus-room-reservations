import { useEffect, useState } from 'react'
import { Card } from '../components/Card'
import { PageTitle } from '../components/PageTitle'
import { Table } from '../components/Table'
import { formatDate } from '../lib/format'
import { reservasService } from '../services/reservasService'
import { salasService } from '../services/salasService'

const initialForm = {
  idSala: '',
  fechaInicio: '',
  fechaFin: '',
  tipoEvento: 'Academica',
  descripcion: '',
}

export function ReservasPage() {
  const [reservas, setReservas] = useState([])
  const [salas, setSalas] = useState([])
  const [actorId, setActorId] = useState('665100000000000000000006')
  const [form, setForm] = useState(initialForm)
  const [status, setStatus] = useState('')

  const loadData = async () => {
    const [reservasData, salasData] = await Promise.all([reservasService.list(), salasService.list()])
    setReservas(reservasData)
    setSalas(salasData)
    if (!form.idSala && salasData.length > 0) {
      setForm((prev) => ({ ...prev, idSala: salasData[0]._id }))
    }
  }

  useEffect(() => {
    loadData().catch((err) => setStatus(err.message))
  }, [])

  const onCreate = async (event) => {
    event.preventDefault()
    setStatus('')
    try {
      const payload = {
        ...form,
        fechaInicio: new Date(form.fechaInicio).toISOString(),
        fechaFin: new Date(form.fechaFin).toISOString(),
      }
      await reservasService.create(payload, actorId)
      setForm((prev) => ({ ...initialForm, idSala: prev.idSala }))
      await loadData()
      setStatus('Reserva creada correctamente')
    } catch (err) {
      setStatus(err.message)
    }
  }

  const onCancelar = async (id) => {
    try {
      await reservasService.cancelar(id, 'Cancelacion desde frontend', actorId)
      await loadData()
      setStatus('Reserva cancelada')
    } catch (err) {
      setStatus(err.message)
    }
  }

  return (
    <>
      <PageTitle title="Reservas" subtitle="Creacion, cancelacion y visualizacion de reservas" />
      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <h2 className="mb-3 text-base font-semibold">Crear Reserva</h2>
          <form className="space-y-3" onSubmit={onCreate}>
            <select className="w-full rounded-md border border-slate-300 px-3 py-2" value={form.idSala} onChange={(e) => setForm({ ...form, idSala: e.target.value })}>
              {salas.map((sala) => (
                <option key={sala._id} value={sala._id}>
                  {sala.codigoSala} - {sala.nombre}
                </option>
              ))}
            </select>
            <input required type="datetime-local" className="w-full rounded-md border border-slate-300 px-3 py-2" value={form.fechaInicio} onChange={(e) => setForm({ ...form, fechaInicio: e.target.value })} />
            <input required type="datetime-local" className="w-full rounded-md border border-slate-300 px-3 py-2" value={form.fechaFin} onChange={(e) => setForm({ ...form, fechaFin: e.target.value })} />
            <select className="w-full rounded-md border border-slate-300 px-3 py-2" value={form.tipoEvento} onChange={(e) => setForm({ ...form, tipoEvento: e.target.value })}>
              <option>Academica</option>
              <option>Administrativa</option>
            </select>
            <textarea required className="w-full rounded-md border border-slate-300 px-3 py-2" placeholder="descripcion" value={form.descripcion} onChange={(e) => setForm({ ...form, descripcion: e.target.value })} />
            <input className="w-full rounded-md border border-slate-300 px-3 py-2" value={actorId} onChange={(e) => setActorId(e.target.value)} placeholder="X-User-Id" />
            <button className="w-full rounded-md bg-teal-600 px-3 py-2 font-medium text-white hover:bg-teal-700" type="submit">
              Guardar
            </button>
          </form>
          {status ? <p className="mt-3 text-sm text-slate-700">{status}</p> : null}
        </Card>

        <Card className="lg:col-span-2">
          <Table
            columns={[
              { key: '_id', label: 'ID' },
              { key: 'estado', label: 'Estado' },
              { key: 'tipoEvento', label: 'Tipo' },
              { key: 'fechaInicio', label: 'Inicio', render: (row) => formatDate(row.fechaInicio) },
              { key: 'fechaFin', label: 'Fin', render: (row) => formatDate(row.fechaFin) },
              {
                key: 'accion',
                label: 'Accion',
                render: (row) => (
                  <button className="rounded bg-rose-100 px-2 py-1 text-xs text-rose-700 hover:bg-rose-200" onClick={() => onCancelar(row._id)}>
                    Cancelar
                  </button>
                ),
              },
            ]}
            rows={reservas}
          />
        </Card>
      </div>
    </>
  )
}
