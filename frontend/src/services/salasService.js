import { BaseService } from './baseService'

class SalasService extends BaseService {
  constructor() {
    super('/salas')
  }

  list(params) {
    return this.request('', { query: params })
  }

  create(payload) {
    return this.request('', { method: 'POST', body: payload })
  }

  updateEstado(salaId, estado, descripcion, actorId) {
    return this.request(`/${salaId}/estado`, {
      method: 'PATCH',
      body: { estado, descripcion },
      headers: { 'X-User-Id': actorId },
    })
  }
}

export const salasService = new SalasService()
