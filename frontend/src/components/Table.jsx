export function Table({ columns, rows, emptyText = 'Sin datos' }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-left text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-slate-600">
            {columns.map((column) => (
              <th key={column.key} className="px-3 py-2 font-semibold">
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td className="px-3 py-4 text-slate-500" colSpan={columns.length}>
                {emptyText}
              </td>
            </tr>
          ) : (
            rows.map((row, idx) => (
              <tr key={row.id || idx} className="border-b border-slate-100 align-top">
                {columns.map((column) => (
                  <td key={column.key} className="px-3 py-2 text-slate-800">
                    {column.render ? column.render(row) : row[column.key]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
