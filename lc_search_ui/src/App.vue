<template>
  <div id="app">
    <header class="app-header">
      <h1>LeetCode Search</h1>
      <p>Find and filter LeetCode problems by difficulty, tags, patterns, and companies</p>
    </header>
    
    <main class="app-main">
      <div class="controls-section">
        <button 
          @click="showDataManager = !showDataManager"
          class="toggle-data-manager"
        >
          {{ showDataManager ? 'Hide' : 'Show' }} Database Manager
        </button>
        
        <DataManager
          v-if="showDataManager"
          :current-problem-count="problems.length"
          @data-updated="handleDataUpdate"
        />
      </div>
      
      <SearchBar 
        @search="handleSearch" 
        @filter="handleFilter"
        @sort="handleSort"
      />
      <ProblemList 
        :problems="filteredProblems"
        :loading="loading"
      />
    </main>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import SearchBar from './components/SearchBar.vue'
import ProblemList from './components/ProblemList.vue'
import DataManager from './components/DataManager.vue'

export default {
  name: 'App',
  components: {
    SearchBar,
    ProblemList,
    DataManager
  },
  setup() {
    const problems = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const showDataManager = ref(false)
    const filters = ref({
      difficulty: '',
      tags: [],
      patterns: [],
      companies: [],
      sortBy: 'recency' // recency, difficulty, title
    })

    const sortProblems = (problems, sortBy) => {
      const sorted = [...problems]
      
      switch (sortBy) {
        case 'recency':
          return sorted.sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded))
        case 'difficulty': {
          const difficultyOrder = { 'Easy': 1, 'Medium': 2, 'Hard': 3 }
          return sorted.sort((a, b) => difficultyOrder[a.difficulty] - difficultyOrder[b.difficulty])
        }
        case 'title':
          return sorted.sort((a, b) => a.title.localeCompare(b.title))
        case 'id':
          return sorted.sort((a, b) => a.id - b.id)
        default:
          return sorted.sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded))
      }
    }

    const loadProblems = async () => {
      try {
        // First try to load from localStorage (user uploaded data)
        const savedData = localStorage.getItem('lc-search-problems')
        if (savedData) {
          problems.value = JSON.parse(savedData)
          loading.value = false
          return
        }

        // Fallback to default data file
        const response = await fetch('/data/problems.json')
        problems.value = await response.json()
      } catch (error) {
        console.error('Failed to load problems:', error)
      } finally {
        loading.value = false
      }
    }

    const filteredProblems = computed(() => {
      let filtered = problems.value

      // Text search - search in title, description, and tags
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase().trim()
        
        filtered = filtered.filter(problem => {
          const titleMatch = problem.title.toLowerCase().includes(query)
          const descMatch = problem.description?.toLowerCase().includes(query) || false
          const tagMatch = problem.tags.some(tag => tag.toLowerCase().includes(query))
          const patternMatch = problem.patterns.some(pattern => pattern.toLowerCase().includes(query))
          const companyMatch = problem.companies.some(company => company.toLowerCase().includes(query))
          
          return titleMatch || descMatch || tagMatch || patternMatch || companyMatch
        })
      }

      // Difficulty filter
      if (filters.value.difficulty) {
        filtered = filtered.filter(problem => 
          problem.difficulty === filters.value.difficulty
        )
      }

      // Tags filter (OR logic - match any selected tag)
      if (filters.value.tags.length > 0) {
        filtered = filtered.filter(problem => 
          filters.value.tags.some(tag => problem.tags.includes(tag))
        )
      }

      // Patterns filter (OR logic - match any selected pattern)
      if (filters.value.patterns.length > 0) {
        filtered = filtered.filter(problem => 
          filters.value.patterns.some(pattern => problem.patterns.includes(pattern))
        )
      }

      // Companies filter (OR logic - match any selected company)
      if (filters.value.companies.length > 0) {
        filtered = filtered.filter(problem => 
          filters.value.companies.some(company => problem.companies.includes(company))
        )
      }

      // Apply sorting
      return sortProblems(filtered, filters.value.sortBy)
    })

    const handleSearch = (query) => {
      searchQuery.value = query
    }

    const handleFilter = (newFilters) => {
      filters.value = { ...filters.value, ...newFilters }
    }

    const handleSort = (sortBy) => {
      filters.value.sortBy = sortBy
    }

    const handleDataUpdate = (newData) => {
      problems.value = newData
      // Reset filters when data changes
      searchQuery.value = ''
      filters.value = {
        difficulty: '',
        tags: [],
        patterns: [],
        companies: [],
        sortBy: 'recency'
      }
    }

    onMounted(loadProblems)

    return {
      problems,
      filteredProblems,
      loading,
      showDataManager,
      handleSearch,
      handleFilter,
      handleSort,
      handleDataUpdate
    }
  }
}
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  position: relative;
}

#app::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 219, 226, 0.1) 0%, transparent 50%);
  z-index: -1;
}

.app-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.app-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 3rem;
  font-weight: 700;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  background: linear-gradient(135deg, #1f2937 0%, #374151 50%, #1f2937 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}

.app-header p {
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-size: 1.2rem;
  font-weight: 400;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-main {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.controls-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.toggle-data-manager {
  align-self: flex-end;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 14px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.toggle-data-manager:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .toggle-data-manager {
    align-self: stretch;
  }
}
</style>
