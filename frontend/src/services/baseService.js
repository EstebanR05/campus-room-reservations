export class BaseService {
  constructor(resourcePath) {
    this.resourcePath = resourcePath
    this.baseUrl = import.meta.env.VITE_API_BASE_URL
    if (!this.baseUrl) {
      throw new Error('VITE_API_BASE_URL no esta configurada')
    }
  }

  async request(path = '', { method = 'GET', query, body, headers } = {}) {
    const url = new URL(`${this.baseUrl}${this.resourcePath}${path}`)

    if (query) {
      Object.entries(query).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          url.searchParams.set(key, String(value))
        }
      })
    }

    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    })

    const isJson = response.headers.get('content-type')?.includes('application/json')
    const data = isJson ? await response.json() : null

    if (!response.ok) {
      const detail = data?.detail || `Error HTTP ${response.status}`
      throw new Error(detail)
    }

    return data
  }
}
