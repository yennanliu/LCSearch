<template>
  <div class="data-manager">
    <div class="data-manager-header">
      <h3>Database Management</h3>
      <p>Upload a new JSON or CSV file to update the problems database</p>
    </div>

    <div class="upload-section">
      <div class="file-input-container">
        <input
          ref="fileInput"
          type="file"
          accept=".json,.csv"
          @change="handleFileSelect"
          class="file-input"
          id="file-upload"
        />
        <label for="file-upload" class="file-label">
          <span class="file-icon">📁</span>
          Choose JSON or CSV file
        </label>
      </div>
      
      <div v-if="selectedFile" class="file-info">
        <p><strong>Selected:</strong> {{ selectedFile.name }} ({{ formatFileSize(selectedFile.size) }})</p>
        <div class="file-actions">
          <button @click="uploadFile" :disabled="uploading" class="upload-btn">
            {{ uploading ? 'Processing...' : 'Upload & Update Database' }}
          </button>
          <button @click="clearSelection" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>

    <div v-if="uploadStatus" class="status-message" :class="uploadStatus.type">
      <p>{{ uploadStatus.message }}</p>
      <div v-if="uploadStatus.details" class="status-details">
        <small>{{ uploadStatus.details }}</small>
      </div>
    </div>

    <div class="current-data-info">
      <h4>Current Database</h4>
      <p><strong>Problems loaded:</strong> {{ currentProblemCount }}</p>
      <p><strong>Last updated:</strong> {{ lastUpdated || 'Unknown' }}</p>
      
      <div class="data-actions">
        <button @click="downloadSample" class="download-btn">
          Download Sample JSON
        </button>
        <button @click="downloadCsvTemplate" class="download-btn">
          Download CSV Template
        </button>
      </div>
    </div>

    <div class="format-guide">
      <details>
        <summary>Data Format Guide</summary>
        <div class="format-content">
          <h5>JSON Format:</h5>
          <pre><code>[
  {
    "id": 1,
    "title": "Two Sum",
    "difficulty": "Easy",
    "url": "https://leetcode.com/problems/two-sum/",
    "tags": ["Array", "Hash Table"],
    "patterns": ["Two Pointers", "Hash Map"],
    "companies": ["Google", "Amazon"],
    "dateAdded": "2023-01-01",
    "description": "Problem description..."
  }
]</code></pre>

          <h5>CSV Format:</h5>
          <p>CSV should have columns: id, title, difficulty, url, tags, patterns, companies, dateAdded, description</p>
          <p>Use semicolons (;) to separate multiple tags, patterns, or companies in a single field.</p>
        </div>
      </details>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'DataManager',
  props: {
    currentProblemCount: {
      type: Number,
      default: 0
    }
  },
  emits: ['data-updated'],
  setup(props, { emit }) {
    const fileInput = ref(null)
    const selectedFile = ref(null)
    const uploading = ref(false)
    const uploadStatus = ref(null)
    const lastUpdated = ref(localStorage.getItem('lc-search-last-updated'))

    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedFile.value = file
        uploadStatus.value = null
      }
    }

    const clearSelection = () => {
      selectedFile.value = null
      if (fileInput.value) {
        fileInput.value.value = ''
      }
      uploadStatus.value = null
    }

    const validateJsonData = (data) => {
      if (!Array.isArray(data)) {
        throw new Error('Data must be an array of problems')
      }

      const requiredFields = ['id', 'title', 'difficulty', 'url', 'tags', 'patterns', 'companies', 'dateAdded']
      
      data.forEach((problem, index) => {
        requiredFields.forEach(field => {
          if (!(field in problem)) {
            throw new Error(`Missing required field "${field}" in problem at index ${index}`)
          }
        })
        
        if (!['Easy', 'Medium', 'Hard'].includes(problem.difficulty)) {
          throw new Error(`Invalid difficulty "${problem.difficulty}" in problem at index ${index}. Must be Easy, Medium, or Hard.`)
        }
      })

      return data
    }

    const parseCsvData = (csvText) => {
      const lines = csvText.trim().split('\n')
      if (lines.length < 2) {
        throw new Error('CSV must have a header row and at least one data row')
      }

      const headers = lines[0].split(',').map(h => h.trim())
      const requiredHeaders = ['id', 'title', 'difficulty', 'url', 'tags', 'patterns', 'companies', 'dateAdded']
      
      const missingHeaders = requiredHeaders.filter(h => !headers.includes(h))
      if (missingHeaders.length > 0) {
        throw new Error(`Missing required CSV headers: ${missingHeaders.join(', ')}`)
      }

      const problems = []
      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim())
        const problem = {}
        
        headers.forEach((header, index) => {
          let value = values[index] || ''
          
          if (header === 'id') {
            value = parseInt(value)
          } else if (['tags', 'patterns', 'companies'].includes(header)) {
            value = value.split(';').map(item => item.trim()).filter(item => item.length > 0)
          }
          
          problem[header] = value
        })
        
        problems.push(problem)
      }

      return validateJsonData(problems)
    }

    const uploadFile = async () => {
      if (!selectedFile.value) return

      uploading.value = true
      uploadStatus.value = null

      try {
        const fileText = await selectedFile.value.text()
        let problemsData

        if (selectedFile.value.name.endsWith('.json')) {
          problemsData = validateJsonData(JSON.parse(fileText))
        } else if (selectedFile.value.name.endsWith('.csv')) {
          problemsData = parseCsvData(fileText)
        } else {
          throw new Error('Unsupported file format. Please use JSON or CSV.')
        }

        // Store in localStorage as backup
        localStorage.setItem('lc-search-problems', JSON.stringify(problemsData))
        localStorage.setItem('lc-search-last-updated', new Date().toISOString())
        lastUpdated.value = new Date().toLocaleString()

        uploadStatus.value = {
          type: 'success',
          message: 'Database updated successfully!',
          details: `Loaded ${problemsData.length} problems from ${selectedFile.value.name}`
        }

        emit('data-updated', problemsData)
        clearSelection()

      } catch (error) {
        uploadStatus.value = {
          type: 'error',
          message: 'Failed to update database',
          details: error.message
        }
      } finally {
        uploading.value = false
      }
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const downloadSample = () => {
      const sampleData = [
        {
          id: 1,
          title: "Two Sum",
          difficulty: "Easy",
          url: "https://leetcode.com/problems/two-sum/",
          tags: ["Array", "Hash Table"],
          patterns: ["Two Pointers", "Hash Map"],
          companies: ["Google", "Amazon", "Microsoft"],
          dateAdded: "2023-01-01",
          description: "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
        }
      ]

      const blob = new Blob([JSON.stringify(sampleData, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'leetcode-problems-sample.json'
      a.click()
      URL.revokeObjectURL(url)
    }

    const downloadCsvTemplate = () => {
      const csvContent = `id,title,difficulty,url,tags,patterns,companies,dateAdded,description
1,Two Sum,Easy,https://leetcode.com/problems/two-sum/,Array;Hash Table,Two Pointers;Hash Map,Google;Amazon;Microsoft,2023-01-01,Given an array of integers nums and an integer target return indices of the two numbers such that they add up to target.`

      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'leetcode-problems-template.csv'
      a.click()
      URL.revokeObjectURL(url)
    }

    return {
      fileInput,
      selectedFile,
      uploading,
      uploadStatus,
      lastUpdated,
      handleFileSelect,
      clearSelection,
      uploadFile,
      formatFileSize,
      downloadSample,
      downloadCsvTemplate
    }
  }
}
</script>

<style scoped>
.data-manager {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
  margin-bottom: 2rem;
}

.data-manager-header {
  margin-bottom: 1.5rem;
  text-align: center;
}

.data-manager-header h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.data-manager-header p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.upload-section {
  margin-bottom: 1.5rem;
  padding: 1rem;
  border: 2px dashed #ddd;
  border-radius: 8px;
  text-align: center;
  transition: border-color 0.2s ease;
}

.upload-section:hover {
  border-color: #1976d2;
}

.file-input-container {
  margin-bottom: 1rem;
}

.file-input {
  display: none;
}

.file-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 12px 24px;
  background: #1976d2;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.file-label:hover {
  background: #1565c0;
}

.file-icon {
  font-size: 1.2rem;
}

.file-info {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 1rem;
  margin-top: 1rem;
}

.file-info p {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 0.9rem;
}

.file-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.upload-btn {
  padding: 8px 16px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s ease;
}

.upload-btn:hover:not(:disabled) {
  background: #218838;
}

.upload-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.cancel-btn {
  padding: 8px 16px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s ease;
}

.cancel-btn:hover {
  background: #c82333;
}

.status-message {
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.status-message.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status-message.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.status-message p {
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.status-details {
  font-size: 0.8rem;
  opacity: 0.9;
}

.current-data-info {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.current-data-info h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.current-data-info p {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #666;
}

.data-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.download-btn {
  padding: 6px 12px;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background-color 0.2s ease;
}

.download-btn:hover {
  background: #5a6268;
}

.format-guide {
  border-top: 1px solid #eee;
  padding-top: 1rem;
}

.format-guide summary {
  cursor: pointer;
  font-weight: 500;
  color: #333;
  margin-bottom: 0.5rem;
}

.format-content h5 {
  margin: 1rem 0 0.5rem 0;
  color: #333;
  font-size: 0.9rem;
}

.format-content pre {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 0.75rem;
  font-size: 0.8rem;
  overflow-x: auto;
}

.format-content p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: #666;
}

@media (max-width: 768px) {
  .data-manager {
    padding: 1rem;
  }
  
  .file-actions,
  .data-actions {
    flex-direction: column;
  }
  
  .file-label {
    display: flex;
    justify-content: center;
  }
}
</style>