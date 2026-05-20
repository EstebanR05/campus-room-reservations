import { BaseService } from './baseService'

class UsuariosService extends BaseService {
  constructor() {
    super('/usuarios')
  }

  list(params) {
    return this.request('', { query: params })
  }

  create(payload) {
    return this.request('', { method: 'POST', body: payload })
  }

  updateEstado(usuarioId, estado) {
    return this.request(`/${usuarioId}/estado`, {
      method: 'PATCH',
      body: { estado },
    })
  }
}

export const usuariosService = new UsuariosService()
