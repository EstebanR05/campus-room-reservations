import { BaseService } from './baseService'

class AuditoriaService extends BaseService {
  constructor() {
    super('/auditoria')
  }

  list(params) {
    return this.request('', { query: params })
  }
}

export const auditoriaService = new AuditoriaService()
