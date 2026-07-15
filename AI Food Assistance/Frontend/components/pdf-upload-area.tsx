'use client'

import { useState, useRef, useEffect } from 'react'
import { Upload, File, Trash2, Eye } from 'lucide-react'

interface Doc {
  id: number
  filename: string
  file_type: string
  uploaded_at: string
}

export default function PDFUploadArea({ onUploadComplete }: { onUploadComplete: () => void }) {
  const [isDragging, setIsDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [documents, setDocuments] = useState<Doc[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => { fetchDocs() }, [])

  const fetchDocs = async () => {
    const token = localStorage.getItem('bitewise_auth_token')
    try {
      const res = await fetch('http://localhost:8000/rag/admin/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (res.ok) {
        const data = await res.json()
        setDocuments(Array.isArray(data) ? data : [])
      }
    } catch (err) { console.error('Fetch docs failed:', err) }
  }

  const uploadFile = async (file: File) => {
    const token = localStorage.getItem('bitewise_auth_token')
    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)
    try {
      const res = await fetch('http://localhost:8000/rag/admin/upload', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      })
      if (res.ok) { onUploadComplete(); fetchDocs() }
    } catch (err) { console.error('Upload failed:', err) }
    finally { setUploading(false) }
  }

  const deleteDoc = async (id: number) => {
    const token = localStorage.getItem('bitewise_auth_token')
    await fetch(`http://localhost:8000/rag/admin/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchDocs()
  }

  const viewPDF = (filename: string) => {
    window.open(`http://localhost:8000/rag/admin/view/${filename}`, '_blank')
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault(); setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file?.type === 'application/pdf') uploadFile(file)
  }

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
          isDragging ? 'border-orange-500 bg-orange-50' : 'border-gray-300 hover:border-orange-300'
        }`}
      >
        <input ref={fileInputRef} type="file" accept=".pdf" onChange={(e) => { const f = e.target.files?.[0]; if (f) uploadFile(f) }} className="hidden" />
        <div onClick={() => fileInputRef.current?.click()}>
          <Upload className="w-12 h-12 text-orange-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {uploading ? 'Uploading...' : 'Drag & drop PDF or click to browse'}
          </h3>
          <p className="text-sm text-gray-500">PDF files only</p>
        </div>
      </div>

      {/* Document List */}
      {documents.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <div className="p-4 border-b border-gray-200 bg-gray-50">
            <h3 className="font-semibold text-gray-900">Uploaded Documents ({documents.length})</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {documents.map((doc) => (
              <div key={doc.id} className="p-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
                <div className="flex items-center gap-3">
                  <File className="w-8 h-8 text-orange-500" />
                  <div>
                    <p className="font-medium text-gray-900">{doc.filename}</p>
                    <p className="text-xs text-gray-500">{new Date(doc.uploaded_at).toLocaleDateString()}</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => viewPDF(doc.filename)} className="p-2 hover:bg-gray-100 text-orange-500 rounded-lg" title="View PDF">
                    <Eye size={18} />
                  </button>
                  <button onClick={() => deleteDoc(doc.id)} className="p-2 hover:bg-red-50 text-red-500 rounded-lg" title="Delete">
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}