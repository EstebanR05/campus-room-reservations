import { BaseService } from './baseService'

class FacultadesService extends BaseService {
  constructor() {
    super('/facultades')
  }

  list() {
    return this.request()
  }
}

export const facultadesService = new FacultadesService()
