"use client"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"

export function PreviewStep() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Resumen del Contenido</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label>Título</Label>
            <p className="text-sm text-muted-foreground">
              10 Estrategias SEO para 2024
            </p>
          </div>

          <div className="space-y-2">
            <Label>Descripción</Label>
            <p className="text-sm text-muted-foreground">
              Guía completa de estrategias SEO actualizadas para mejorar el
              posicionamiento en 2024.
            </p>
          </div>

          <div className="space-y-2">
            <Label>Keywords</Label>
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary">SEO</Badge>
              <Badge variant="secondary">Estrategias</Badge>
              <Badge variant="secondary">2024</Badge>
              <Badge variant="secondary">Posicionamiento</Badge>
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label>Categoría</Label>
              <p className="text-sm text-muted-foreground">SEO</p>
            </div>
            <div className="space-y-2">
              <Label>Tipo de Contenido</Label>
              <p className="text-sm text-muted-foreground">Guía</p>
            </div>
          </div>

          <div className="space-y-2">
            <Label>Tono de Voz</Label>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Formalidad</span>
                  <span className="text-muted-foreground">70%</span>
                </div>
                <div className="h-2 rounded-full bg-muted">
                  <div
                    className="h-full rounded-full bg-primary"
                    style={{ width: "70%" }}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Tecnicidad</span>
                  <span className="text-muted-foreground">60%</span>
                </div>
                <div className="h-2 rounded-full bg-muted">
                  <div
                    className="h-full rounded-full bg-primary"
                    style={{ width: "60%" }}
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <Label>Referencias</Label>
            <div className="space-y-2">
              <div className="rounded-lg border p-3">
                <p className="text-sm font-medium">https://example.com/seo-2024</p>
                <p className="mt-1 text-sm text-muted-foreground">
                  Estadísticas y tendencias SEO para 2024
                </p>
              </div>
              <div className="rounded-lg border p-3">
                <p className="text-sm font-medium">
                  https://example.com/google-updates
                </p>
                <p className="mt-1 text-sm text-muted-foreground">
                  Últimas actualizaciones del algoritmo de Google
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
} 