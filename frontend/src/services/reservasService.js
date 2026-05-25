import { BaseService } from './baseService'

class ReservasService extends BaseService {
  constructor() {
    super('/reservas')
  }

  list(params) {
    return this.request('', { query: params })
  }

  create(payload, actorId) {
    return this.request('', {
      method: 'POST',
      body: payload,
      headers: { 'X-User-Id': actorId },
    })
  }

  cancelar(reservaId, motivo, actorId) {
    return this.request(`/${reservaId}/cancelar`, {
      method: 'PATCH',
      body: { motivo },
      headers: { 'X-User-Id': actorId },
    })
  }

  ajustar(reservaId, payload, actorId) {
    return this.request(`/${reservaId}/ajustar`, {
      method: 'PATCH',
      body: payload,
      headers: { 'X-User-Id': actorId },
    })
  }
}

export const reservasService = new ReservasService()
