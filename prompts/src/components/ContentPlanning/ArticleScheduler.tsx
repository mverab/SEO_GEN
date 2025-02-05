'use client'

import { useState } from 'react'
import { Card } from '@/components/ui/card'
import { Calendar } from '@/components/ui/calendar'
import { Button } from '@/components/ui/button'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'

interface Article {
  title: string
  keyword: string
  secondary_keywords?: string
  plannedDate?: Date
  status: 'pending' | 'scheduled' | 'completed'
}

export function ArticleScheduler({ articles }: { articles: Article[] }) {
  const [scheduledArticles, setScheduledArticles] = useState(articles)
  const [selectedDate, setSelectedDate] = useState<Date>()
  const [selectedArticle, setSelectedArticle] = useState<string | null>(null)

  const handleArticleClick = (title: string) => {
    setSelectedArticle(title)
  }

  const handleDateSelect = (date: Date | undefined) => {
    if (!selectedArticle || !date) return

    setScheduledArticles(articles.map(article => 
      article.title === selectedArticle 
        ? { ...article, plannedDate: date, status: 'scheduled' }
        : article
    ))
    setSelectedArticle(null)
    setSelectedDate(undefined)
  }

  return (
    <div className="grid grid-cols-12 gap-4">
      <div className="col-span-8">
        <div className="space-y-2">
          {scheduledArticles.map((article) => (
            <Card
              key={article.title}
              className={`p-4 cursor-pointer transition-colors ${
                selectedArticle === article.title ? 'ring-2 ring-primary' : ''
              }`}
              onClick={() => handleArticleClick(article.title)}
            >
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="font-medium">{article.title}</h3>
                  <p className="text-sm text-gray-500">{article.keyword}</p>
                  {article.plannedDate && (
                    <p className="text-sm text-blue-500 mt-1">
                      {format(article.plannedDate, "d 'de' MMMM, yyyy", { locale: es })}
                    </p>
                  )}
                </div>
                <span className={`px-2 py-1 rounded text-sm ${
                  article.status === 'completed' ? 'bg-green-100 text-green-800' :
                  article.status === 'scheduled' ? 'bg-blue-100 text-blue-800' :
                  'bg-gray-100'
                }`}>
                  {article.status}
                </span>
              </div>
            </Card>
          ))}
        </div>
      </div>

      <div className="col-span-4">
        <Card className="p-4">
          <h3 className="font-medium mb-4">
            {selectedArticle ? 'Selecciona una fecha' : 'Selecciona un artículo'}
          </h3>
          <Calendar
            mode="single"
            selected={selectedDate}
            onSelect={handleDateSelect}
            className="rounded-md border"
            disabled={(date) => date < new Date()}
          />
          {selectedArticle && (
            <Button 
              className="w-full mt-4"
              variant="outline"
              onClick={() => setSelectedArticle(null)}
            >
              Cancelar
            </Button>
          )}
        </Card>
      </div>
    </div>
  )
} 