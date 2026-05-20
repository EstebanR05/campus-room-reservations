import { useEffect, useState } from 'react'
import { Card } from '../components/Card'
import { PageTitle } from '../components/PageTitle'
import { Table } from '../components/Table'
import { facultadesService } from '../services/facultadesService'
import { usuariosService } from '../services/usuariosService'

const initialForm = {
  codigoUsuario: '',
  nombreCompleto: '',
  email: '',
  rol: 'Docente',
  estado: 'Activo',
  idFacultad: '',
}

export function UsuariosPage() {
  const [usuarios, setUsuarios] = useState([])
  const [facultades, setFacultades] = useState([])
  const [form, setForm] = useState(initialForm)
  const [status, setStatus] = useState('')

  const loadData = async () => {
    const [usuariosData, facultadesData] = await Promise.all([
      usuariosService.list(),
      facultadesService.list(),
    ])
    setUsuarios(usuariosData)
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
      await usuariosService.create(form)
      setForm((prev) => ({ ...initialForm, idFacultad: prev.idFacultad }))
      await loadData()
      setStatus('Usuario creado correctamente')
    } catch (err) {
      setStatus(err.message)
    }
  }

  const onToggleEstado = async (usuario) => {
    const nextEstado = usuario.estado === 'Activo' ? 'Inactivo' : 'Activo'
    try {
      await usuariosService.updateEstado(usuario._id, nextEstado)
      await loadData()
      setStatus(`Estado actualizado para ${usuario.nombreCompleto}`)
    } catch (err) {
      setStatus(err.message)
    }
  }

  return (
    <>
      <PageTitle title="Usuarios" subtitle="Gestion de docentes y secretarias" />
      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <h2 className="mb-3 text-base font-semibold">Crear Usuario</h2>
          <form className="space-y-3" onSubmit={onCreate}>
            {Object.entries(form).map(([key, value]) => {
              if (key === 'rol') {
                return (
                  <select key={key} className="w-full rounded-md border border-slate-300 px-3 py-2" value={value} onChange={(e) => setForm({ ...form, rol: e.target.value })}>
                    <option>Docente</option>
                    <option>Secretaria</option>
                  </select>
                )
              }
              if (key === 'estado') {
                return (
                  <select key={key} className="w-full rounded-md border border-slate-300 px-3 py-2" value={value} onChange={(e) => setForm({ ...form, estado: e.target.value })}>
                    <option>Activo</option>
                    <option>Inactivo</option>
                  </select>
                )
              }
              if (key === 'idFacultad') {
                return (
                  <select key={key} className="w-full rounded-md border border-slate-300 px-3 py-2" value={value} onChange={(e) => setForm({ ...form, idFacultad: e.target.value })}>
                    {facultades.map((facultad) => (
                      <option key={facultad.id} value={facultad.id}>
                        {facultad.nombre}
                      </option>
                    ))}
                  </select>
                )
              }
              return (
                <input
                  key={key}
                  required
                  value={value}
                  onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                  placeholder={key}
                  className="w-full rounded-md border border-slate-300 px-3 py-2"
                />
              )
            })}
            <button className="w-full rounded-md bg-teal-600 px-3 py-2 font-medium text-white hover:bg-teal-700" type="submit">
              Guardar
            </button>
          </form>
          {status ? <p className="mt-3 text-sm text-slate-700">{status}</p> : null}
        </Card>

        <Card className="lg:col-span-2">
          <Table
            columns={[
              { key: 'codigoUsuario', label: 'Codigo' },
              { key: 'nombreCompleto', label: 'Nombre' },
              { key: 'email', label: 'Email' },
              { key: 'rol', label: 'Rol' },
              { key: 'estado', label: 'Estado' },
              {
                key: 'accion',
                label: 'Accion',
                render: (row) => (
                  <button className="rounded bg-slate-200 px-2 py-1 text-xs hover:bg-slate-300" onClick={() => onToggleEstado(row)}>
                    Cambiar
                  </button>
                ),
              },
            ]}
            rows={usuarios}
          />
        </Card>
      </div>
    </>
  )
}
