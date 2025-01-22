"use client"

import { ResourceLibrary } from "@/components/resource/library"
import { ResourceUploader } from "@/components/resource/uploader"
import { ReferenceManager } from "@/components/resource/reference-manager"
import { NicheOrganizer } from "@/components/resource/niche-organizer"

export default function ResourceManagementPage() {
  return (
    <div className="container space-y-8">
      <h1>Gestión de Recursos</h1>
      <div className="grid gap-8">
        <ResourceLibrary />
        <ResourceUploader />
        <ReferenceManager />
        <NicheOrganizer />
      </div>
    </div>
  )
} 