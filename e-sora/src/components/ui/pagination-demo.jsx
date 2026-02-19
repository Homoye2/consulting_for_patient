import { useState } from 'react'
import { Pagination } from './pagination'
import { Card, CardContent, CardHeader, CardTitle } from './card'

/**
 * Démo de pagination pour tester le composant
 */
export const PaginationDemo = () => {
  const [currentPage, setCurrentPage] = useState(1)
  const totalItems = 150
  const itemsPerPage = 15
  const totalPages = Math.ceil(totalItems / itemsPerPage)

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle>🧪 Test de Pagination</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="text-sm text-muted-foreground">
            Simulation avec {totalItems} éléments, {itemsPerPage} par page
          </div>
          
          <div className="border rounded p-4">
            <h3 className="font-medium mb-2">Page {currentPage}</h3>
            <div className="grid grid-cols-3 gap-2">
              {Array.from({ length: itemsPerPage }, (_, i) => {
                const itemNumber = (currentPage - 1) * itemsPerPage + i + 1
                return itemNumber <= totalItems ? (
                  <div key={i} className="p-2 bg-muted rounded text-sm">
                    Élément #{itemNumber}
                  </div>
                ) : null
              })}
            </div>
          </div>
          
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            totalItems={totalItems}
            itemsPerPage={itemsPerPage}
            onPageChange={setCurrentPage}
            showInfo={true}
          />
          
          <div className="text-xs text-muted-foreground">
            État: Page {currentPage}/{totalPages} | Total: {totalItems} éléments
          </div>
        </div>
      </CardContent>
    </Card>
  )
}