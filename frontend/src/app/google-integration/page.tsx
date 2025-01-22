"use client"

import { GoogleAuthButton } from "@/components/google/auth-button"
import { DocPicker } from "@/components/google/doc-picker"
import { ExportToDocs } from "@/components/google/export-to-docs"
import { DriveManager } from "@/components/google/drive-manager"

export default function GoogleIntegrationPage() {
  return (
    <div className="container space-y-8">
      <h1>Integración con Google</h1>
      <GoogleAuthButton />
      <div className="grid gap-8">
        <DocPicker />
        <ExportToDocs />
        <DriveManager />
      </div>
    </div>
  )
} 