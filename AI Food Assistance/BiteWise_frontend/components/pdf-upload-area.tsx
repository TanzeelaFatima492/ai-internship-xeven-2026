'use client'

import { useState, useRef } from 'react'
import { Upload, File, X, CheckCircle, AlertCircle } from 'lucide-react'

interface UploadedFile {
  id: string
  name: string
  size: number
  status: 'uploading' | 'success' | 'error'
  progress: number
}

interface PDFUploadAreaProps {
  onUploadComplete: () => void
}

export default function PDFUploadArea({ onUploadComplete }: PDFUploadAreaProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [files, setFiles] = useState<UploadedFile[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const processFiles = (fileList: FileList | null) => {
    if (!fileList) return

    Array.from(fileList).forEach((file) => {
      if (file.type === 'application/pdf') {
        const newFile: UploadedFile = {
          id: `${Date.now()}-${Math.random()}`,
          name: file.name,
          size: file.size,
          status: 'uploading',
          progress: 0,
        }
        setFiles((prev) => [...prev, newFile])

        // Simulate upload progress
        const progressInterval = setInterval(() => {
          setFiles((prev) =>
            prev.map((f) =>
              f.id === newFile.id
                ? {
                    ...f,
                    progress: Math.min(f.progress + Math.random() * 40, 90),
                  }
                : f
            )
          )
        }, 300)

        // Simulate upload completion
        setTimeout(() => {
          clearInterval(progressInterval)
          setFiles((prev) =>
            prev.map((f) =>
              f.id === newFile.id
                ? { ...f, progress: 100, status: 'success' }
                : f
            )
          )
          onUploadComplete()
        }, 2000)
      }
    })
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    processFiles(e.dataTransfer.files)
  }

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    processFiles(e.target.files)
  }

  const handleRemoveFile = (id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id))
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
  }

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`relative border-2 border-dashed rounded-xl p-12 transition-all duration-200 cursor-pointer ${
          isDragging
            ? 'border-primary bg-primary/5'
            : 'border-border bg-muted/20 hover:border-primary/50'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf"
          onChange={handleFileInputChange}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />

        <div className="text-center">
          <div className="bg-gradient-to-br from-primary/20 to-accent/20 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Upload className="w-8 h-8 text-primary" />
          </div>
          <h3 className="text-lg font-semibold text-foreground mb-2">
            Drag & drop your PDF files here
          </h3>
          <p className="text-muted-foreground mb-4">
            or click to browse your computer
          </p>
          <p className="text-xs text-muted-foreground">
            Supports PDF files up to 50MB each
          </p>
        </div>
      </div>

      {/* Uploaded Files List */}
      {files.length > 0 && (
        <div className="bg-card border border-border rounded-xl overflow-hidden">
          <div className="p-6 border-b border-border">
            <h3 className="text-lg font-semibold text-foreground">
              Uploaded Files ({files.length})
            </h3>
          </div>

          <div className="divide-y divide-border">
            {files.map((file) => (
              <div key={file.id} className="p-6 hover:bg-muted/20 transition-colors">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start gap-4 flex-1">
                    <div className="bg-primary/10 rounded-lg p-3 mt-1">
                      <File className="w-5 h-5 text-primary" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-foreground truncate">{file.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {formatFileSize(file.size)}
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={() => handleRemoveFile(file.id)}
                    className="p-2 hover:bg-muted rounded-lg transition-colors text-muted-foreground hover:text-foreground"
                  >
                    <X size={20} />
                  </button>
                </div>

                {/* Progress Bar */}
                {file.status === 'uploading' && (
                  <div className="space-y-2">
                    <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-primary to-accent transition-all duration-300"
                        style={{ width: `${file.progress}%` }}
                      />
                    </div>
                    <p className="text-xs text-muted-foreground text-right">
                      {Math.round(file.progress)}%
                    </p>
                  </div>
                )}

                {/* Status */}
                {file.status === 'success' && (
                  <div className="flex items-center gap-2 text-sm text-green-500">
                    <CheckCircle size={16} />
                    Upload completed successfully
                  </div>
                )}

                {file.status === 'error' && (
                  <div className="flex items-center gap-2 text-sm text-destructive">
                    <AlertCircle size={16} />
                    Upload failed. Please try again.
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Upload Info */}
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-gradient-to-br from-primary/5 to-accent/5 border border-primary/20 rounded-xl p-4">
          <h4 className="font-semibold text-foreground mb-2">Supported Formats</h4>
          <ul className="text-sm text-muted-foreground space-y-1">
            <li>• PDF documents</li>
            <li>• Menu files</li>
            <li>• Policy documents</li>
          </ul>
        </div>
        <div className="bg-gradient-to-br from-secondary/5 to-accent/5 border border-secondary/20 rounded-xl p-4">
          <h4 className="font-semibold text-foreground mb-2">Best Practices</h4>
          <ul className="text-sm text-muted-foreground space-y-1">
            <li>• Clear, readable PDF scans</li>
            <li>• Organize by category</li>
            <li>• Update regularly</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
